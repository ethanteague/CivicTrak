#!/usr/bin/env python3
"""
Government Contact Database Compiler
Scrapes public municipal data from various sources to build a contacts database
"""

import requests
import csv
import json
import time
from bs4 import BeautifulSoup
from dataclasses import dataclass, asdict
from typing import List, Dict, Optional
import sqlite3
import re
from urllib.parse import urljoin, urlparse
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@dataclass
class GovernmentContact:
    """Structure for government contact information"""
    municipality: str
    state: str
    population: Optional[int] = None
    contact_name: Optional[str] = None
    title: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    website: Optional[str] = None
    address: Optional[str] = None
    source: Optional[str] = None
    last_updated: Optional[str] = None

class GovernmentContactScraper:
    """Main scraper class for collecting government contacts"""
    
    def __init__(self, db_path: str = "government_contacts.db"):
        self.db_path = db_path
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        self.init_database()
    
    def init_database(self):
        """Initialize SQLite database for storing contacts"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS government_contacts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                municipality TEXT NOT NULL,
                state TEXT NOT NULL,
                population INTEGER,
                contact_name TEXT,
                title TEXT,
                email TEXT,
                phone TEXT,
                website TEXT,
                address TEXT,
                source TEXT,
                last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(municipality, state, email)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def save_contact(self, contact: GovernmentContact):
        """Save contact to database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT OR REPLACE INTO government_contacts
                (municipality, state, population, contact_name, title, email, phone, website, address, source)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                contact.municipality, contact.state, contact.population,
                contact.contact_name, contact.title, contact.email,
                contact.phone, contact.website, contact.address, contact.source
            ))
            conn.commit()
            logger.info(f"Saved contact: {contact.municipality}, {contact.state}")
        except sqlite3.Error as e:
            logger.error(f"Database error: {e}")
        finally:
            conn.close()
    
    def scrape_state_municipal_leagues(self) -> List[GovernmentContact]:
        """Scrape state municipal league directories"""
        contacts = []
        
        # State municipal leagues with known directory structures
        state_leagues = {
            'Texas': 'https://directory.tml.org/',
            'North Carolina': 'https://www.nclm.org/people-directory',
            'California': 'https://www.calcities.org/members',
            'Florida': 'https://www.flcities.com/directory',
            'Alabama': 'https://almonline.org/directory'
        }
        
        for state, url in state_leagues.items():
            try:
                logger.info(f"Scraping {state} municipal league...")
                response = self.session.get(url, timeout=30)
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Extract contacts based on common patterns
                contacts.extend(self.extract_contacts_from_directory(soup, state, url))
                time.sleep(2)  # Be respectful
                
            except Exception as e:
                logger.error(f"Error scraping {state}: {e}")
        
        return contacts
    
    def extract_contacts_from_directory(self, soup: BeautifulSoup, state: str, source: str) -> List[GovernmentContact]:
        """Extract contacts from directory HTML"""
        contacts = []
        
        # Common patterns for municipal directories
        contact_selectors = [
            '.city-listing', '.municipality', '.member-listing',
            '.directory-entry', '.contact-card', '.official-listing'
        ]
        
        for selector in contact_selectors:
            entries = soup.select(selector)
            if entries:
                for entry in entries:
                    contact = self.parse_directory_entry(entry, state, source)
                    if contact:
                        contacts.append(contact)
                break
        
        return contacts
    
    def parse_directory_entry(self, entry, state: str, source: str) -> Optional[GovernmentContact]:
        """Parse individual directory entry"""
        try:
            # Extract municipality name
            municipality = self.extract_text(entry, ['h1', 'h2', 'h3', '.city-name', '.municipality-name'])
            if not municipality:
                return None
            
            # Extract contact information
            contact_name = self.extract_text(entry, ['.contact-name', '.official-name', '.name'])
            title = self.extract_text(entry, ['.title', '.position', '.role'])
            email = self.extract_email(entry)
            phone = self.extract_phone(entry)
            website = self.extract_website(entry)
            address = self.extract_text(entry, ['.address', '.location'])
            
            return GovernmentContact(
                municipality=municipality,
                state=state,
                contact_name=contact_name,
                title=title,
                email=email,
                phone=phone,
                website=website,
                address=address,
                source=source
            )
        except Exception as e:
            logger.error(f"Error parsing entry: {e}")
            return None
    
    def extract_text(self, element, selectors: List[str]) -> Optional[str]:
        """Extract text using multiple selector strategies"""
        for selector in selectors:
            found = element.select_one(selector)
            if found and found.get_text(strip=True):
                return found.get_text(strip=True)
        return None
    
    def extract_email(self, element) -> Optional[str]:
        """Extract email address from element"""
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        text = element.get_text()
        matches = re.findall(email_pattern, text)
        return matches[0] if matches else None
    
    def extract_phone(self, element) -> Optional[str]:
        """Extract phone number from element"""
        phone_pattern = r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b'
        text = element.get_text()
        matches = re.findall(phone_pattern, text)
        return matches[0] if matches else None
    
    def extract_website(self, element) -> Optional[str]:
        """Extract website URL from element"""
        links = element.find_all('a', href=True)
        for link in links:
            href = link['href']
            if href.startswith('http') and any(domain in href for domain in ['.gov', '.org', '.com']):
                return href
        return None
    
    def scrape_census_data(self) -> List[GovernmentContact]:
        """Get municipality data from Census API"""
        contacts = []
        
        try:
            # Census API for places (municipalities)
            url = "https://api.census.gov/data/2020/dec/pl"
            params = {
                "get": "NAME,P1_001N",  # Name and total population
                "for": "place:*",
                "in": "state:*"
            }
            
            response = self.session.get(url, params=params, timeout=30)
            data = response.json()
            
            # Skip header row
            for row in data[1:]:
                name, population, state_code, place_code = row
                
                # Filter for smaller municipalities (under 50k population)
                if int(population) < 50000:
                    contact = GovernmentContact(
                        municipality=name,
                        state=self.get_state_name(state_code),
                        population=int(population),
                        source="US Census API"
                    )
                    contacts.append(contact)
            
            logger.info(f"Retrieved {len(contacts)} municipalities from Census")
            
        except Exception as e:
            logger.error(f"Error scraping Census data: {e}")
        
        return contacts
    
    def get_state_name(self, state_code: str) -> str:
        """Convert state FIPS code to state name"""
        state_codes = {
            "01": "Alabama", "02": "Alaska", "04": "Arizona", "05": "Arkansas",
            "06": "California", "08": "Colorado", "09": "Connecticut", "10": "Delaware",
            "12": "Florida", "13": "Georgia", "15": "Hawaii", "16": "Idaho",
            "17": "Illinois", "18": "Indiana", "19": "Iowa", "20": "Kansas",
            "21": "Kentucky", "22": "Louisiana", "23": "Maine", "24": "Maryland",
            "25": "Massachusetts", "26": "Michigan", "27": "Minnesota", "28": "Mississippi",
            "29": "Missouri", "30": "Montana", "31": "Nebraska", "32": "Nevada",
            "33": "New Hampshire", "34": "New Jersey", "35": "New Mexico", "36": "New York",
            "37": "North Carolina", "38": "North Dakota", "39": "Ohio", "40": "Oklahoma",
            "41": "Oregon", "42": "Pennsylvania", "44": "Rhode Island", "45": "South Carolina",
            "46": "South Dakota", "47": "Tennessee", "48": "Texas", "49": "Utah",
            "50": "Vermont", "51": "Virginia", "53": "Washington", "54": "West Virginia",
            "55": "Wisconsin", "56": "Wyoming"
        }
        return state_codes.get(state_code, f"State-{state_code}")
    
    def export_to_csv(self, filename: str = "government_contacts.csv"):
        """Export database to CSV"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM government_contacts ORDER BY state, municipality")
        rows = cursor.fetchall()
        
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([
                'Municipality', 'State', 'Population', 'Contact Name', 'Title',
                'Email', 'Phone', 'Website', 'Address', 'Source', 'Last Updated'
            ])
            
            for row in rows:
                writer.writerow(row[1:])  # Skip ID column
        
        logger.info(f"Exported {len(rows)} contacts to {filename}")
        conn.close()
    
    def get_stats(self) -> Dict:
        """Get database statistics"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        stats = {}
        cursor.execute("SELECT COUNT(*) FROM government_contacts")
        stats['total_contacts'] = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM government_contacts WHERE email IS NOT NULL")
        stats['contacts_with_email'] = cursor.fetchone()[0]
        
        cursor.execute("SELECT state, COUNT(*) FROM government_contacts GROUP BY state ORDER BY COUNT(*) DESC LIMIT 10")
        stats['top_states'] = cursor.fetchall()
        
        conn.close()
        return stats

def main():
    """Main execution function"""
    scraper = GovernmentContactScraper()
    
    print("🏛️  Government Contact Database Compiler")
    print("=" * 50)
    
    # Scrape Census data for municipality list
    print("\n📊 Scraping Census data for municipalities...")
    census_contacts = scraper.scrape_census_data()
    for contact in census_contacts:
        scraper.save_contact(contact)
    
    # Scrape state municipal leagues
    print("\n🏛️  Scraping state municipal league directories...")
    league_contacts = scraper.scrape_state_municipal_leagues()
    for contact in league_contacts:
        scraper.save_contact(contact)
    
    # Export results
    print("\n📄 Exporting to CSV...")
    scraper.export_to_csv()
    
    # Show statistics
    print("\n📈 Database Statistics:")
    stats = scraper.get_stats()
    print(f"Total contacts: {stats['total_contacts']}")
    print(f"Contacts with email: {stats['contacts_with_email']}")
    print("\nTop states by contact count:")
    for state, count in stats['top_states']:
        print(f"  {state}: {count}")
    
    print(f"\n✅ Complete! Database saved to: government_contacts.db")
    print(f"📄 CSV export saved to: government_contacts.csv")

if __name__ == "__main__":
    main()