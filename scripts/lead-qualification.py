#!/usr/bin/env python3
"""
Lead Qualification Tool
Analyzes government contacts to identify high-potential prospects for CivicTrak
"""

import sqlite3
import requests
import logging
from typing import Dict, List, Optional
from dataclasses import dataclass
import json
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import re

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@dataclass
class LeadScore:
    """Lead scoring data structure"""
    contact_id: int
    municipality: str
    state: str
    score: float
    reasons: List[str]
    priority: str  # High, Medium, Low
    website_analysis: Dict
    next_steps: List[str]

class LeadQualifier:
    """Analyzes and scores government contacts as potential leads"""
    
    def __init__(self, db_path: str = "government_contacts.db"):
        self.db_path = db_path
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def analyze_website_technology(self, website: str) -> Dict:
        """Analyze what technology a municipality website is using"""
        analysis = {
            'cms': 'Unknown',
            'is_outdated': False,
            'has_mobile_responsive': False,
            'load_speed_issues': False,
            'accessibility_issues': False,
            'content_management_issues': [],
            'technology_stack': []
        }
        
        try:
            response = self.session.get(website, timeout=30)
            soup = BeautifulSoup(response.content, 'html.parser')
            html_content = response.text.lower()
            
            # Detect CMS
            cms_indicators = {
                'wordpress': ['wp-content', 'wp-includes', 'wordpress'],
                'drupal': ['drupal', 'sites/default', 'misc/drupal'],
                'joomla': ['joomla', 'templates/system'],
                'squarespace': ['squarespace'],
                'wix': ['wix.com', 'wixstatic'],
                'civicplus': ['civicplus', 'civic-plus'],
                'granicus': ['granicus'],
                'revize': ['revize'],
                'vision': ['visioninternet']
            }
            
            for cms, indicators in cms_indicators.items():
                if any(indicator in html_content for indicator in indicators):
                    analysis['cms'] = cms
                    break
            
            # Check for outdated indicators
            outdated_indicators = [
                'table-based layout',
                'flash',
                'internet explorer',
                '<font',
                'bgcolor='
            ]
            
            analysis['is_outdated'] = any(indicator in html_content for indicator in outdated_indicators)
            
            # Check mobile responsiveness
            viewport_tag = soup.find('meta', attrs={'name': 'viewport'})
            analysis['has_mobile_responsive'] = viewport_tag is not None
            
            # Check for accessibility issues
            accessibility_checks = [
                len(soup.find_all('img', alt=False)) > 0,  # Images without alt text
                len(soup.find_all('a', title=False)) > 5,  # Links without titles
                not soup.find('h1')  # No main heading
            ]
            
            analysis['accessibility_issues'] = any(accessibility_checks)
            
            # Content management red flags
            content_issues = []
            
            # Check for "under construction" or maintenance messages
            if any(phrase in html_content for phrase in ['under construction', 'coming soon', 'maintenance']):
                content_issues.append('Site under construction/maintenance')
            
            # Check for broken links (sample check)
            links = soup.find_all('a', href=True)[:10]  # Check first 10 links
            broken_links = 0
            for link in links:
                try:
                    link_response = self.session.head(link['href'], timeout=5)
                    if link_response.status_code >= 400:
                        broken_links += 1
                except:
                    broken_links += 1
            
            if broken_links > 2:
                content_issues.append('Multiple broken links detected')
            
            analysis['content_management_issues'] = content_issues
            
        except Exception as e:
            logger.error(f"Error analyzing website {website}: {e}")
            analysis['cms'] = 'Error'
        
        return analysis
    
    def calculate_lead_score(self, contact: Dict, website_analysis: Dict) -> LeadScore:
        """Calculate lead score based on various factors"""
        score = 0.0
        reasons = []
        next_steps = []
        
        municipality = contact['municipality']
        state = contact['state']
        population = contact.get('population', 0)
        website = contact.get('website')
        email = contact.get('email')
        
        # Population scoring (sweet spot: 1,000 - 25,000)
        if 1000 <= population <= 25000:
            score += 25
            reasons.append(f"Ideal population size ({population:,})")
        elif 500 <= population < 1000:
            score += 15
            reasons.append(f"Small but viable population ({population:,})")
        elif population > 25000:
            score += 5
            reasons.append(f"Larger municipality ({population:,}) - may have existing solutions")
        else:
            score -= 10
            reasons.append(f"Very small population ({population:,}) - limited budget")
        
        # Technology analysis scoring
        if website_analysis['cms'] == 'Unknown' or website_analysis['cms'] == 'Error':
            score += 20
            reasons.append("No modern CMS detected - high potential need")
            next_steps.append("Offer free website audit")
        
        elif website_analysis['cms'] in ['wordpress', 'joomla']:
            score += 15
            reasons.append(f"Using {website_analysis['cms']} - not government-specific")
            next_steps.append("Highlight government-specific features")
        
        elif website_analysis['cms'] in ['civicplus', 'granicus', 'revize']:
            score -= 15
            reasons.append(f"Already using government CMS ({website_analysis['cms']})")
            next_steps.append("Research contract renewal dates")
        
        # Outdated website bonus
        if website_analysis['is_outdated']:
            score += 20
            reasons.append("Website appears outdated - modernization need")
            next_steps.append("Emphasize modern design and mobile responsiveness")
        
        # Mobile responsiveness
        if not website_analysis['has_mobile_responsive']:
            score += 15
            reasons.append("Website not mobile-responsive")
            next_steps.append("Demo mobile-first design")
        
        # Accessibility issues
        if website_analysis['accessibility_issues']:
            score += 10
            reasons.append("Potential accessibility compliance issues")
            next_steps.append("Highlight ADA compliance features")
        
        # Content management issues
        for issue in website_analysis['content_management_issues']:
            score += 10
            reasons.append(f"Content issue: {issue}")
            next_steps.append("Offer easy content management demo")
        
        # Contact information availability
        if email:
            score += 10
            reasons.append("Direct email contact available")
            next_steps.append("Send personalized email with demo link")
        else:
            score -= 5
            reasons.append("No direct email contact")
            next_steps.append("Research contact information")
        
        # State-specific scoring (some states more likely to adopt new tech)
        progressive_states = ['California', 'Washington', 'Colorado', 'North Carolina', 'Virginia']
        if state in progressive_states:
            score += 5
            reasons.append(f"{state} - tech-progressive state")
        
        # Priority classification
        if score >= 60:
            priority = "High"
        elif score >= 40:
            priority = "Medium"
        else:
            priority = "Low"
        
        return LeadScore(
            contact_id=contact['id'],
            municipality=municipality,
            state=state,
            score=score,
            reasons=reasons,
            priority=priority,
            website_analysis=website_analysis,
            next_steps=next_steps
        )
    
    def qualify_leads(self, limit: int = 50) -> List[LeadScore]:
        """Qualify leads from the contacts database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Get contacts with websites for analysis
        cursor.execute("""
            SELECT id, municipality, state, population, email, website, contact_name, title
            FROM government_contacts 
            WHERE website IS NOT NULL AND population > 500 AND population < 50000
            ORDER BY population DESC
            LIMIT ?
        """, (limit,))
        
        contacts = cursor.fetchall()
        conn.close()
        
        lead_scores = []
        
        logger.info(f"Qualifying {len(contacts)} leads...")
        
        for i, contact_data in enumerate(contacts):
            contact = {
                'id': contact_data[0],
                'municipality': contact_data[1],
                'state': contact_data[2],
                'population': contact_data[3],
                'email': contact_data[4],
                'website': contact_data[5],
                'contact_name': contact_data[6],
                'title': contact_data[7]
            }
            
            logger.info(f"Analyzing {contact['municipality']}, {contact['state']} ({i+1}/{len(contacts)})")
            
            # Analyze website technology
            website_analysis = self.analyze_website_technology(contact['website'])
            
            # Calculate lead score
            lead_score = self.calculate_lead_score(contact, website_analysis)
            lead_scores.append(lead_score)
            
            # Rate limiting
            if i % 10 == 0 and i > 0:
                logger.info(f"Processed {i} contacts...")
        
        # Sort by score (highest first)
        lead_scores.sort(key=lambda x: x.score, reverse=True)
        
        return lead_scores
    
    def save_qualified_leads(self, lead_scores: List[LeadScore]):
        """Save qualified leads to database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create qualified_leads table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS qualified_leads (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                contact_id INTEGER,
                municipality TEXT,
                state TEXT,
                score REAL,
                priority TEXT,
                reasons TEXT,
                next_steps TEXT,
                website_analysis TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (contact_id) REFERENCES government_contacts (id)
            )
        ''')
        
        # Clear existing qualified leads
        cursor.execute("DELETE FROM qualified_leads")
        
        # Insert new qualified leads
        for lead in lead_scores:
            cursor.execute('''
                INSERT INTO qualified_leads 
                (contact_id, municipality, state, score, priority, reasons, next_steps, website_analysis)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                lead.contact_id,
                lead.municipality,
                lead.state,
                lead.score,
                lead.priority,
                json.dumps(lead.reasons),
                json.dumps(lead.next_steps),
                json.dumps(lead.website_analysis)
            ))
        
        conn.commit()
        conn.close()
        
        logger.info(f"Saved {len(lead_scores)} qualified leads to database")
    
    def export_qualified_leads(self, filename: str = "qualified_leads.csv"):
        """Export qualified leads to CSV"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT ql.municipality, ql.state, gc.population, gc.email, gc.website, 
                   gc.contact_name, gc.title, ql.score, ql.priority, ql.reasons, ql.next_steps
            FROM qualified_leads ql
            JOIN government_contacts gc ON ql.contact_id = gc.id
            ORDER BY ql.score DESC
        """)
        
        rows = cursor.fetchall()
        
        import csv
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([
                'Municipality', 'State', 'Population', 'Email', 'Website',
                'Contact Name', 'Title', 'Lead Score', 'Priority', 'Reasons', 'Next Steps'
            ])
            
            for row in rows:
                # Parse JSON fields
                reasons = json.loads(row[9]) if row[9] else []
                next_steps = json.loads(row[10]) if row[10] else []
                
                writer.writerow([
                    row[0], row[1], row[2], row[3], row[4], row[5], row[6],
                    row[7], row[8], '; '.join(reasons), '; '.join(next_steps)
                ])
        
        logger.info(f"Exported {len(rows)} qualified leads to {filename}")
        conn.close()
    
    def get_lead_stats(self) -> Dict:
        """Get statistics on qualified leads"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        stats = {}
        
        # Priority distribution
        cursor.execute("SELECT priority, COUNT(*) FROM qualified_leads GROUP BY priority")
        stats['priority_distribution'] = dict(cursor.fetchall())
        
        # Top scoring leads
        cursor.execute("""
            SELECT ql.municipality, ql.state, ql.score 
            FROM qualified_leads ql 
            ORDER BY ql.score DESC LIMIT 10
        """)
        stats['top_leads'] = cursor.fetchall()
        
        # Average score by state
        cursor.execute("""
            SELECT ql.state, AVG(ql.score) as avg_score, COUNT(*) as count
            FROM qualified_leads ql 
            GROUP BY ql.state 
            HAVING COUNT(*) >= 3
            ORDER BY avg_score DESC
        """)
        stats['state_averages'] = cursor.fetchall()
        
        conn.close()
        return stats

def main():
    """Main execution function"""
    qualifier = LeadQualifier()
    
    print("🎯 Government Contact Lead Qualification")
    print("=" * 45)
    
    # Qualify leads
    print("\n🔍 Analyzing websites and qualifying leads...")
    lead_scores = qualifier.qualify_leads(limit=30)  # Start small for testing
    
    # Save to database
    print("\n💾 Saving qualified leads...")
    qualifier.save_qualified_leads(lead_scores)
    
    # Export to CSV
    print("\n📄 Exporting to CSV...")
    qualifier.export_qualified_leads()
    
    # Show statistics
    print("\n📊 Lead Qualification Statistics:")
    stats = qualifier.get_lead_stats()
    
    print(f"\nPriority Distribution:")
    for priority, count in stats['priority_distribution'].items():
        print(f"  {priority}: {count}")
    
    print(f"\nTop 5 Scoring Leads:")
    for municipality, state, score in stats['top_leads'][:5]:
        print(f"  {municipality}, {state}: {score:.1f}")
    
    print(f"\nTop States by Average Score:")
    for state, avg_score, count in stats['state_averages'][:5]:
        print(f"  {state}: {avg_score:.1f} (n={count})")
    
    print(f"\n✅ Lead qualification complete!")
    print(f"📄 Results saved to: qualified_leads.csv")

if __name__ == "__main__":
    main()