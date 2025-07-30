#!/usr/bin/env python3
"""
Quick Sample Lead Generator
Creates a sample of high-potential government leads for immediate outreach
"""

import sqlite3
import csv
import random

def create_sample_leads():
    """Create a curated sample of high-potential leads"""
    
    # Connect to database
    conn = sqlite3.connect("government_contacts.db")
    cursor = conn.cursor()
    
    # Get municipalities in ideal range
    cursor.execute("""
        SELECT municipality, state, population 
        FROM government_contacts 
        WHERE population BETWEEN 2000 AND 15000
        AND state IN ('North Carolina', 'Virginia', 'Colorado', 'Washington', 'California', 'Texas', 'Florida')
        ORDER BY population DESC
        LIMIT 100
    """)
    
    contacts = cursor.fetchall()
    
    # Create sample leads with contact research needed
    sample_leads = []
    
    for municipality, state, population in contacts:
        # Generate likely government website
        municipality_clean = municipality.replace(' city', '').replace(' town', '').replace(' CDP', '').replace(' borough', '').lower()
        municipality_clean = municipality_clean.replace(' ', '')
        
        # Common government website patterns
        possible_websites = [
            f"https://www.{municipality_clean}.{state.lower().replace(' ', '')}.gov",
            f"https://www.cityof{municipality_clean}.gov",
            f"https://www.{municipality_clean}.gov",
            f"https://{municipality_clean}.gov"
        ]
        
        # Generate likely contact emails
        likely_emails = [
            f"clerk@{municipality_clean}.gov",
            f"info@{municipality_clean}.gov",
            f"mayor@{municipality_clean}.gov",
            f"citymanager@{municipality_clean}.gov"
        ]
        
        # Calculate basic lead score
        score = 50  # Base score
        
        # Population bonus
        if 3000 <= population <= 8000:
            score += 20
            priority = "High"
        elif 1500 <= population <= 12000:
            score += 10
            priority = "Medium"
        else:
            priority = "Low"
        
        # State bonus for tech-progressive states
        if state in ['North Carolina', 'Virginia', 'Colorado', 'Washington', 'California']:
            score += 10
        
        sample_leads.append({
            'municipality': municipality,
            'state': state,
            'population': population,
            'likely_website': possible_websites[0],
            'likely_email': likely_emails[0],
            'alt_emails': '; '.join(likely_emails[1:]),
            'score': score,
            'priority': priority,
            'target_persona': 'City Clerk / IT Director',
            'pain_points': 'Outdated website, manual processes, poor mobile experience',
            'value_proposition': 'Modern government website with citizen portal, mobile-first design, easy content management',
            'next_action': 'Send personalized email with demo link'
        })
    
    # Save to CSV
    with open('sample_high_priority_leads.csv', 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = [
            'municipality', 'state', 'population', 'likely_website', 'likely_email', 
            'alt_emails', 'score', 'priority', 'target_persona', 'pain_points',
            'value_proposition', 'next_action'
        ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(sample_leads)
    
    conn.close()
    
    print(f"✅ Created {len(sample_leads)} sample leads")
    print(f"📄 Saved to: sample_high_priority_leads.csv")
    
    # Show statistics
    high_priority = len([lead for lead in sample_leads if lead['priority'] == 'High'])
    medium_priority = len([lead for lead in sample_leads if lead['priority'] == 'Medium'])
    
    print(f"\n📊 Lead Breakdown:")
    print(f"  🔥 High Priority: {high_priority}")
    print(f"  📈 Medium Priority: {medium_priority}")
    print(f"  📍 Geographic Coverage: {len(set(lead['state'] for lead in sample_leads))} states")
    
    # Show top 5 leads
    print(f"\n🎯 Top 5 Leads:")
    sorted_leads = sorted(sample_leads, key=lambda x: x['score'], reverse=True)
    for i, lead in enumerate(sorted_leads[:5], 1):
        print(f"  {i}. {lead['municipality']}, {lead['state']} (Pop: {lead['population']:,}, Score: {lead['score']})")

if __name__ == "__main__":
    create_sample_leads()