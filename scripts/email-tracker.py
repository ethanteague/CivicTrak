#!/usr/bin/env python3
"""
Simple Email Tracking System for CivicTrak Outreach
Tracks email campaigns and responses
"""

import csv
import json
from datetime import datetime, timedelta

class EmailTracker:
    """Track email outreach campaigns"""
    
    def __init__(self, tracking_file="email_tracking.csv"):
        self.tracking_file = tracking_file
        self.init_tracking_file()
    
    def init_tracking_file(self):
        """Initialize tracking CSV file"""
        try:
            with open(self.tracking_file, 'r') as f:
                pass
        except FileNotFoundError:
            # Create new tracking file
            with open(self.tracking_file, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow([
                    'Date', 'Municipality', 'State', 'Email', 'Template', 
                    'Status', 'Response_Date', 'Response_Type', 'Notes', 'Demo_Scheduled'
                ])
    
    def log_email_sent(self, municipality, state, email, template="initial"):
        """Log when an email is sent"""
        with open(self.tracking_file, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([
                datetime.now().strftime('%Y-%m-%d %H:%M'),
                municipality,
                state, 
                email,
                template,
                'sent',
                '',  # response_date
                '',  # response_type
                '',  # notes
                'No'  # demo_scheduled
            ])
        print(f"✅ Logged email sent to {municipality}, {state}")
    
    def log_response(self, email, response_type, notes="", demo_scheduled=False):
        """Log when you get a response"""
        # Read existing data
        rows = []
        with open(self.tracking_file, 'r') as f:
            reader = csv.reader(f)
            rows = list(reader)
        
        # Update the row with response
        for i, row in enumerate(rows):
            if len(row) > 3 and row[3] == email and row[5] == 'sent':
                rows[i][5] = 'responded'  # status
                rows[i][6] = datetime.now().strftime('%Y-%m-%d %H:%M')  # response_date
                rows[i][7] = response_type
                rows[i][8] = notes
                rows[i][9] = 'Yes' if demo_scheduled else 'No'
                break
        
        # Write back to file
        with open(self.tracking_file, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerows(rows)
        
        print(f"✅ Logged response from {email}: {response_type}")
    
    def get_stats(self):
        """Get campaign statistics"""
        try:
            with open(self.tracking_file, 'r') as f:
                reader = csv.DictReader(f)
                rows = list(reader)
            
            total_sent = len([r for r in rows if r['Status'] == 'sent' or r['Status'] == 'responded'])
            total_responses = len([r for r in rows if r['Status'] == 'responded'])
            demos_scheduled = len([r for r in rows if r['Demo_Scheduled'] == 'Yes'])
            
            response_rate = (total_responses / total_sent * 100) if total_sent > 0 else 0
            demo_rate = (demos_scheduled / total_sent * 100) if total_sent > 0 else 0
            
            return {
                'total_sent': total_sent,
                'total_responses': total_responses,
                'demos_scheduled': demos_scheduled,
                'response_rate': response_rate,
                'demo_rate': demo_rate
            }
            
        except FileNotFoundError:
            return {
                'total_sent': 0,
                'total_responses': 0,
                'demos_scheduled': 0,
                'response_rate': 0,
                'demo_rate': 0
            }
    
    def show_dashboard(self):
        """Show tracking dashboard"""
        stats = self.get_stats()
        
        print("\n📊 CivicTrak Email Campaign Dashboard")
        print("=" * 40)
        print(f"📧 Total Emails Sent: {stats['total_sent']}")
        print(f"📬 Responses Received: {stats['total_responses']}")
        print(f"📞 Demos Scheduled: {stats['demos_scheduled']}")
        print(f"📈 Response Rate: {stats['response_rate']:.1f}%")
        print(f"🎯 Demo Conversion: {stats['demo_rate']:.1f}%")
        
        # Show who to follow up with
        self.show_follow_ups()
    
    def show_follow_ups(self):
        """Show prospects that need follow-up"""
        try:
            with open(self.tracking_file, 'r') as f:
                reader = csv.DictReader(f)
                rows = list(reader)
            
            # Find emails sent 4+ days ago with no response
            follow_ups = []
            cutoff_date = datetime.now() - timedelta(days=4)
            
            for row in rows:
                if row['Status'] == 'sent':
                    sent_date = datetime.strptime(row['Date'], '%Y-%m-%d %H:%M')
                    if sent_date < cutoff_date:
                        follow_ups.append(row)
            
            if follow_ups:
                print(f"\n🔄 Follow-up Needed ({len(follow_ups)} prospects):")
                for row in follow_ups:
                    print(f"  • {row['Municipality']}, {row['State']} - Sent {row['Date']}")
            else:
                print(f"\n✅ No follow-ups needed right now")
                
        except (FileNotFoundError, ValueError):
            print(f"\n📝 No tracking data yet")

def main():
    """Main function for email tracking"""
    tracker = EmailTracker()
    
    print("🏛️ CivicTrak Email Tracking System")
    print("=" * 35)
    
    while True:
        print("\nWhat would you like to do?")
        print("1. Log email sent")
        print("2. Log response received") 
        print("3. View dashboard")
        print("4. Quick log - Top 3 prospects")
        print("5. Exit")
        
        choice = input("\nEnter choice (1-5): ")
        
        if choice == '1':
            municipality = input("Municipality: ")
            state = input("State: ")
            email = input("Email address: ")
            template = input("Template used (initial/follow_up/value): ") or "initial"
            tracker.log_email_sent(municipality, state, email, template)
            
        elif choice == '2':
            email = input("Email address that responded: ")
            response_type = input("Response type (interested/not_interested/demo_request/more_info): ")
            notes = input("Notes (optional): ")
            demo = input("Demo scheduled? (y/n): ").lower() == 'y'
            tracker.log_response(email, response_type, notes, demo)
            
        elif choice == '3':
            tracker.show_dashboard()
            
        elif choice == '4':
            # Quick log for your top 3 verified prospects
            prospects = [
                ("California City, CA", "California", "city@californiacity.ca.gov"),
                ("West University Place, TX", "Texas", "city@westutx.gov"),
                ("Canyon, TX", "Texas", "city@canyon-tx.com")
            ]
            
            for municipality, state, email in prospects:
                tracker.log_email_sent(municipality, state, email, "initial")
            
            print("✅ Logged all 3 prospect emails!")
            
        elif choice == '5':
            print("👋 Happy prospecting!")
            break
        
        else:
            print("❌ Invalid choice. Please try again.")

if __name__ == "__main__":
    main()