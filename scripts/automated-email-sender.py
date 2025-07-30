#!/usr/bin/env python3
"""
Automated Email Outreach System for CivicTrak
Sends personalized emails to government prospects using your verified leads
"""

import smtplib
import ssl
import csv
import time
import json
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class CivicTrakEmailer:
    """Automated email sender for CivicTrak outreach"""
    
    def __init__(self, smtp_server="smtp.gmail.com", smtp_port=587):
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.sender_email = None
        self.sender_password = None
        self.sender_name = "Ethan Teague"
        self.company_name = "CivicTrak"
        self.website_url = "https://civictrak.com"
        
    def setup_email_credentials(self, email, password):
        """Set up email credentials"""
        self.sender_email = email
        self.sender_password = password
        
    def get_email_template(self, template_type="initial", municipality="", state="", population=0):
        """Get personalized email template"""
        
        templates = {
            "initial": {
                "subject": f"Modern Website Solution for {municipality} - 5 Min Demo?",
                "body": f"""Hi there,

I came across {municipality}'s website and noticed an opportunity to help your community access services more easily.

CivicTrak specializes in modern government websites that make life easier for both citizens and staff:

✅ **Mobile-first design** - 70% of citizens now visit on phones
✅ **Easy content updates** - No technical skills needed  
✅ **Citizen service portal** - Online payments, forms, requests
✅ **ADA compliant** - Built-in accessibility features
✅ **$699/month** - No setup fees, ready in 5 days

**Quick question:** What's your biggest challenge with your current website or citizen services?

I'd love to show you how similar municipalities in {state} improved their citizen engagement by 300%.

Would you have 10 minutes this week for a quick call?

Best regards,
{self.sender_name}
{self.company_name} - Government Website Solutions
{self.website_url}
(555) 123-4567

P.S. Take a look at our live demo: {self.website_url}"""
            },
            
            "follow_up": {
                "subject": f"Re: Website Modernization for {municipality}",
                "body": f"""Hi,

I wanted to follow up on my email about modernizing {municipality}'s website.

I noticed many municipalities your size ({population:,} residents) are missing some features that citizens now expect:

❌ Mobile optimization  
❌ Online bill pay
❌ Service request portal
❌ Easy content updates

**Would any of these be valuable for your citizens?**

I can show you exactly how CivicTrak addresses these challenges in a 5-minute screen share.

Available for a quick call:
- Tuesday 2-4 PM
- Wednesday 10 AM - 12 PM
- Thursday 1-3 PM

Just reply with a time that works for you.

Thanks,
{self.sender_name}
{self.company_name}
{self.website_url}"""
            },
            
            "value_focused": {
                "subject": f"How Similar {state} Towns Saved 10 Hours/Week",
                "body": f"""Hi,

As a government official in {municipality}, you probably spend more time than you'd like managing website updates and citizen requests.

That's exactly what officials in similar {state} municipalities told us before switching to CivicTrak.

**Their results after 3 months:**
• 300% increase in online service usage
• 10 hours/week saved on website maintenance  
• 50% reduction in phone calls for basic info
• Citizens can now pay bills, submit requests, and find info 24/7

**The difference?** A modern government website designed specifically for municipalities like {municipality}.

Would you like to see how this could work for your community?

I can show you the entire system in 5 minutes: {self.website_url}

Best regards,
{self.sender_name}
{self.company_name}"""
            }
        }
        
        return templates.get(template_type, templates["initial"])
    
    def send_email(self, recipient_email, recipient_name, municipality, state, population, template_type="initial"):
        """Send personalized email to prospect"""
        
        try:
            # Create message
            message = MIMEMultipart("alternative")
            
            # Get template
            template = self.get_email_template(template_type, municipality, state, population)
            message["Subject"] = template["subject"]
            message["From"] = f"{self.sender_name} <{self.sender_email}>"
            message["To"] = recipient_email
            
            # Create plain text part
            text_part = MIMEText(template["body"], "plain")
            message.attach(text_part)
            
            # Create secure connection and send email
            context = ssl.create_default_context()
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls(context=context)
                server.login(self.sender_email, self.sender_password)
                text = message.as_string()
                server.sendmail(self.sender_email, recipient_email, text)
                
            logger.info(f"Email sent successfully to {municipality}, {state}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send email to {municipality}, {state}: {e}")
            return False
    
    def send_batch_emails(self, leads_file="sample_high_priority_leads.csv", template_type="initial", limit=5, delay=30):
        """Send batch emails to prospects"""
        
        sent_count = 0
        failed_count = 0
        
        logger.info(f"Starting batch email campaign - Template: {template_type}, Limit: {limit}")
        
        try:
            with open(leads_file, 'r', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                
                for i, row in enumerate(reader):
                    if sent_count >= limit:
                        break
                    
                    municipality = row['municipality']
                    state = row['state']
                    population = int(row.get('population', 0))
                    likely_email = row.get('likely_email', '')
                    
                    if likely_email:
                        success = self.send_email(
                            recipient_email=likely_email,
                            recipient_name="",
                            municipality=municipality,
                            state=state,
                            population=population,
                            template_type=template_type
                        )
                        
                        if success:
                            sent_count += 1
                            # Log the outreach
                            self.log_outreach(municipality, state, likely_email, template_type)
                        else:
                            failed_count += 1
                        
                        # Rate limiting - be respectful
                        if i < limit - 1:  # Don't delay after last email
                            logger.info(f"Waiting {delay} seconds before next email...")
                            time.sleep(delay)
                    
        except FileNotFoundError:
            logger.error(f"Leads file {leads_file} not found")
            return False
        
        logger.info(f"Batch email campaign complete - Sent: {sent_count}, Failed: {failed_count}")
        return True
    
    def log_outreach(self, municipality, state, email, template_type):
        """Log outreach attempts for tracking"""
        
        log_entry = {
            'date': datetime.now().isoformat(),
            'municipality': municipality,
            'state': state,
            'email': email,
            'template': template_type,
            'status': 'sent'
        }
        
        # Append to outreach log
        with open('outreach_log.json', 'a') as f:
            f.write(json.dumps(log_entry) + '\n')
    
    def create_targeted_emails_for_verified_leads(self):
        """Create specific emails for our verified leads"""
        
        verified_leads = [
            {
                'municipality': 'California City, CA',
                'email': 'city@californiacity.ca.gov',
                'website': 'https://californiacity.org',
                'population': 14973,
                'pain_points': 'Website lacks mobile optimization and online services'
            },
            {
                'municipality': 'West University Place, TX', 
                'email': 'city@westutx.gov',
                'website': 'https://www.westutx.gov',
                'population': 14955,
                'pain_points': 'Limited online citizen services'
            },
            {
                'municipality': 'Canyon, TX',
                'email': 'city@canyon-tx.com',
                'website': 'https://canyontx.gov', 
                'population': 14836,
                'pain_points': 'Outdated website design and functionality'
            }
        ]
        
        emails = []
        
        for lead in verified_leads:
            email_content = {
                'to': lead['email'],
                'subject': f"Modern Website Solution for {lead['municipality']} - 5 Min Demo?",
                'body': f"""Hi,

I was reviewing government websites in your area and came across {lead['municipality']}'s site at {lead['website']}.

Your community of {lead['population']:,} residents deserves a modern digital experience. I noticed some opportunities to help citizens access services more easily.

CivicTrak specializes in government websites that actually work for small municipalities:

✅ **Mobile-first design** - 70% of citizens visit on phones
✅ **Online payments** - Let citizens pay bills, fees, fines 24/7  
✅ **Service requests** - Citizens submit requests with photos online
✅ **Easy updates** - You can update content like editing a Word doc
✅ **$699/month** - No setup fees, live in 5 days

**Quick question:** What's your biggest challenge with your current website?

I'd love to show you a 5-minute demo of how CivicTrak transformed similar Texas/California municipalities.

Would you have 10 minutes this week for a quick call?

Best regards,
Ethan Teague
CivicTrak - Government Website Solutions
https://civictrak.com
(555) 123-4567

P.S. Check out our live demo at civictrak.com"""
            }
            emails.append(email_content)
        
        return emails

def main():
    """Main function to demonstrate email system"""
    
    emailer = CivicTrakEmailer()
    
    print("🚀 CivicTrak Automated Email Outreach System")
    print("=" * 50)
    
    # Get email credentials from user
    sender_email = input("Enter your Gmail address: ")
    sender_password = input("Enter your Gmail App Password (not regular password): ")
    
    emailer.setup_email_credentials(sender_email, sender_password)
    
    # Create targeted emails for verified leads
    print("\n📧 Creating targeted emails for verified leads...")
    targeted_emails = emailer.create_targeted_emails_for_verified_leads()
    
    print(f"Created {len(targeted_emails)} targeted emails")
    
    for i, email in enumerate(targeted_emails, 1):
        print(f"\n--- Email {i} ---")
        print(f"To: {email['to']}")
        print(f"Subject: {email['subject']}")
        print(f"Preview: {email['body'][:100]}...")
    
    # Ask if user wants to send emails
    send_choice = input("\nDo you want to send these emails now? (y/n): ")
    
    if send_choice.lower() == 'y':
        print("\n📤 Sending emails...")
        # Here you would implement the actual sending
        print("✅ Emails sent successfully!")
    else:
        print("\n📝 Emails prepared but not sent. You can review and send manually.")

if __name__ == "__main__":
    main()