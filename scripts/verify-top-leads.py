#!/usr/bin/env python3
"""
Top Lead Verification Tool
Verifies contact information for your highest priority prospects
"""

import requests
import csv
import time
from urllib.parse import urlparse

def verify_top_leads():
    """Verify the top leads from our sample"""
    
    # Top prospects to verify manually
    top_prospects = [
        {
            'name': 'Laurinburg, NC',
            'population': 14978,
            'likely_website': 'https://www.laurinburg.nc.gov',
            'alt_websites': ['https://cityoflaurinburg.com', 'https://laurinburg.gov'],
            'likely_emails': ['clerk@laurinburg.nc.gov', 'info@laurinburg.nc.gov', 'mayor@laurinburg.nc.gov']
        },
        {
            'name': 'California City, CA', 
            'population': 14973,
            'likely_website': 'https://www.californiacity.ca.gov',
            'alt_websites': ['https://cal-city.ca.gov', 'https://californiacity.org'],
            'likely_emails': ['clerk@californiacity.ca.gov', 'info@californiacity.ca.gov']
        },
        {
            'name': 'Hereford, TX',
            'population': 14972,
            'likely_website': 'https://www.hereford-tx.gov',
            'alt_websites': ['https://cityofhereford.org', 'https://hereford.tx.gov'],
            'likely_emails': ['city@hereford-tx.gov', 'clerk@herefordtx.gov']
        },
        {
            'name': 'West University Place, TX',
            'population': 14955,
            'likely_website': 'https://www.westutx.gov',
            'alt_websites': ['https://westuniversityplace.org'],
            'likely_emails': ['city@westutx.gov', 'info@westutx.gov']
        },
        {
            'name': 'Canyon, TX',
            'population': 14836,
            'likely_website': 'https://www.canyon-tx.com',
            'alt_websites': ['https://canyontx.gov', 'https://cityofcanyon.org'],
            'likely_emails': ['city@canyon-tx.com', 'info@canyon-tx.com']
        }
    ]
    
    verified_leads = []
    
    print("🔍 Verifying Top 5 Government Prospects")
    print("=" * 45)
    
    for prospect in top_prospects:
        print(f"\n📍 {prospect['name']} (Pop: {prospect['population']:,})")
        
        # Test websites
        working_website = None
        for website in [prospect['likely_website']] + prospect['alt_websites']:
            try:
                response = requests.get(website, timeout=10, allow_redirects=True)
                if response.status_code == 200:
                    working_website = website
                    print(f"  ✅ Website found: {website}")
                    break
                else:
                    print(f"  ❌ {website} - Status: {response.status_code}")
            except Exception as e:
                print(f"  ❌ {website} - Error: Connection failed")
            
            time.sleep(2)  # Be respectful
        
        if not working_website:
            print(f"  🔍 Manual research needed for {prospect['name']}")
        
        verified_leads.append({
            'municipality': prospect['name'],
            'population': prospect['population'],
            'verified_website': working_website or 'NEEDS_RESEARCH',
            'suggested_emails': '; '.join(prospect['likely_emails']),
            'priority': 'HIGH - Immediate Outreach',
            'next_action': 'Send personalized email' if working_website else 'Research contact info'
        })
    
    # Save verification results
    with open('verified_top_leads.csv', 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['municipality', 'population', 'verified_website', 'suggested_emails', 'priority', 'next_action']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(verified_leads)
    
    print(f"\n✅ Verification complete!")
    print(f"📄 Results saved to: verified_top_leads.csv")
    
    # Show summary
    working_sites = len([lead for lead in verified_leads if lead['verified_website'] != 'NEEDS_RESEARCH'])
    print(f"\n📊 Results Summary:")
    print(f"  🌐 Working websites found: {working_sites}/5")
    print(f"  🔍 Need manual research: {5-working_sites}/5")

if __name__ == "__main__":
    verify_top_leads()