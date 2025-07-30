#!/usr/bin/env python3
"""
Government Contact Enrichment Tool
Enriches basic municipality data with detailed contact information
"""

import requests
import sqlite3
import time
import logging
from typing import Optional, Dict, List
import re
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import json

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ContactEnricher:
    """Enriches government contacts with additional information"""
    
    def __init__(self, db_path: str = "government_contacts.db"):
        self.db_path = db_path
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def find_municipality_website(self, municipality: str, state: str) -> Optional[str]:
        """Find official municipality website"""
        search_queries = [
            f"{municipality} {state} city government official website",
            f"{municipality} {state} town hall contact",
            f"{municipality} {state} city clerk"
        ]
        
        for query in search_queries:
            try:
                # Use DuckDuckGo for search (no API key required)
                url = f"https://api.duckduckgo.com/?q={query}&format=json&no_redirect=1"
                response = self.session.get(url, timeout=10)
                data = response.json()
                
                # Look for .gov domains in results
                for result in data.get('Results', []):
                    url = result.get('FirstURL', '')
                    if '.gov' in url and municipality.lower() in url.lower():
                        return url
                
                time.sleep(1)  # Rate limiting
                
            except Exception as e:
                logger.error(f"Search error for {municipality}, {state}: {e}")
        
        return None
    
    def scrape_municipality_contacts(self, website: str, municipality: str, state: str) -> Dict:
        """Scrape contact information from municipality website"""
        contacts = {
            'emails': [],
            'phones': [],
            'officials': []
        }
        
        try:
            response = self.session.get(website, timeout=30)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Common pages to check for contacts
            contact_links = self.find_contact_pages(soup, website)
            
            for link in contact_links[:3]:  # Limit to 3 pages
                try:
                    page_response = self.session.get(link, timeout=20)
                    page_soup = BeautifulSoup(page_response.content, 'html.parser')
                    
                    # Extract contact information
                    contacts['emails'].extend(self.extract_emails(page_soup))
                    contacts['phones'].extend(self.extract_phones(page_soup))
                    contacts['officials'].extend(self.extract_officials(page_soup))
                    
                    time.sleep(2)  # Be respectful
                    
                except Exception as e:
                    logger.error(f"Error scraping page {link}: {e}")
            
            # Remove duplicates
            contacts['emails'] = list(set(contacts['emails']))
            contacts['phones'] = list(set(contacts['phones']))
            
        except Exception as e:
            logger.error(f"Error scraping {website}: {e}")
        
        return contacts
    
    def find_contact_pages(self, soup: BeautifulSoup, base_url: str) -> List[str]:
        """Find contact and staff pages on the website"""
        contact_keywords = [
            'contact', 'staff', 'directory', 'city-clerk', 'city-manager',
            'mayor', 'council', 'departments', 'phone', 'email'
        ]
        
        contact_links = []
        
        for link in soup.find_all('a', href=True):
            href = link['href'].lower()
            text = link.get_text().lower()
            
            if any(keyword in href or keyword in text for keyword in contact_keywords):
                full_url = urljoin(base_url, link['href'])
                contact_links.append(full_url)
        
        return contact_links
    
    def extract_emails(self, soup: BeautifulSoup) -> List[str]:
        """Extract email addresses from page"""
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        text = soup.get_text()
        
        emails = re.findall(email_pattern, text)
        
        # Filter for relevant government emails
        gov_emails = []
        for email in emails:
            if any(domain in email.lower() for domain in ['.gov', '.org']) and \
               any(role in email.lower() for role in ['clerk', 'mayor', 'manager', 'admin', 'city', 'town']):
                gov_emails.append(email)
        
        return gov_emails
    
    def extract_phones(self, soup: BeautifulSoup) -> List[str]:
        """Extract phone numbers from page"""
        phone_patterns = [
            r'\b\d{3}[-.\s]?\d{3}[-.\s]?\d{4}\b',
            r'\(\d{3}\)\s?\d{3}[-.\s]?\d{4}'
        ]
        
        phones = []
        text = soup.get_text()
        
        for pattern in phone_patterns:
            matches = re.findall(pattern, text)
            phones.extend(matches)
        
        return phones
    
    def extract_officials(self, soup: BeautifulSoup) -> List[Dict]:
        """Extract official names and titles from page"""
        officials = []
        
        # Look for common official title patterns
        title_patterns = [
            r'(Mayor|City Manager|City Clerk|Town Clerk|Administrator):\s*([A-Za-z\s.]+)',
            r'([A-Za-z\s.]+),\s*(Mayor|City Manager|City Clerk|Town Clerk|Administrator)'
        ]
        
        text = soup.get_text()
        
        for pattern in title_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for match in matches:
                if len(match) == 2:
                    title, name = match
                    officials.append({
                        'name': name.strip(),
                        'title': title.strip()
                    })
        
        return officials
    
    def enrich_contacts(self, limit: int = 100):
        """Enrich contacts in database with additional information"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Get contacts without websites or emails
        cursor.execute("""
            SELECT id, municipality, state FROM government_contacts 
            WHERE (website IS NULL OR email IS NULL) AND population < 25000
            ORDER BY population DESC
            LIMIT ?
        """, (limit,))
        
        contacts_to_enrich = cursor.fetchall()
        
        logger.info(f"Enriching {len(contacts_to_enrich)} contacts...")
        
        for contact_id, municipality, state in contacts_to_enrich:
            logger.info(f"Enriching {municipality}, {state}...")
            
            # Find website if not present
            website = self.find_municipality_website(municipality, state)
            
            if website:
                # Scrape contact information
                contact_info = self.scrape_municipality_contacts(website, municipality, state)
                
                # Update database
                self.update_contact_info(contact_id, website, contact_info)
                
                time.sleep(3)  # Be respectful
            
            # Progress indicator
            if contact_id % 10 == 0:
                logger.info(f"Processed {contact_id} contacts...")
        
        conn.close()
        logger.info("Contact enrichment complete!")
    
    def update_contact_info(self, contact_id: int, website: str, contact_info: Dict):
        """Update contact information in database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Prepare update data
        email = contact_info['emails'][0] if contact_info['emails'] else None
        phone = contact_info['phones'][0] if contact_info['phones'] else None
        
        # If we found officials, use the first one
        contact_name = None
        title = None
        if contact_info['officials']:
            official = contact_info['officials'][0]
            contact_name = official['name']
            title = official['title']
        
        cursor.execute("""
            UPDATE government_contacts 
            SET website = ?, email = COALESCE(email, ?), phone = COALESCE(phone, ?),
                contact_name = COALESCE(contact_name, ?), title = COALESCE(title, ?)
            WHERE id = ?
        """, (website, email, phone, contact_name, title, contact_id))
        
        conn.commit()
        conn.close()

class LinkedInFinder:
    """Find LinkedIn profiles for government officials"""
    
    def __init__(self):
        self.session = requests.Session()
    
    def find_official_linkedin(self, name: str, title: str, municipality: str, state: str) -> Optional[str]:
        """Find LinkedIn profile for government official"""
        # This would require LinkedIn API or web scraping
        # For demonstration purposes, return None
        # In practice, you'd use LinkedIn Sales Navigator API or similar tools
        return None

def main():
    """Main execution function"""
    enricher = ContactEnricher()
    
    print("🔍 Government Contact Enrichment Tool")
    print("=" * 40)
    
    # Enrich contacts with websites and additional info
    enricher.enrich_contacts(limit=50)  # Start with 50 for testing
    
    print("✅ Contact enrichment complete!")

if __name__ == "__main__":
    main()