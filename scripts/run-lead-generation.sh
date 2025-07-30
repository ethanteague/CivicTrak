#!/bin/bash

# Government Contact Lead Generation Pipeline
# Runs the complete process to find and qualify government prospects

echo "🏛️  CivicTrak Lead Generation Pipeline"
echo "====================================="

# Install requirements if needed
echo "📦 Installing Python requirements..."
pip3 install requests beautifulsoup4

echo ""
echo "Step 1: Scraping government contact databases..."
python3 government-contact-scraper.py

echo ""
echo "Step 2: Enriching contacts with additional information..."
python3 contact-enrichment.py

echo ""
echo "Step 3: Qualifying and scoring leads..."
python3 lead-qualification.py

echo ""
echo "🎉 Lead generation complete!"
echo ""
echo "Files generated:"
echo "  📊 government_contacts.db - SQLite database with all contacts"
echo "  📄 government_contacts.csv - Full contact export"
echo "  🎯 qualified_leads.csv - High-scoring prospects ready for outreach"
echo ""
echo "Next steps:"
echo "  1. Review qualified_leads.csv for highest scoring prospects"
echo "  2. Import contacts into your CRM or email system"
echo "  3. Begin targeted outreach campaigns"
echo "  4. Track responses and conversions"