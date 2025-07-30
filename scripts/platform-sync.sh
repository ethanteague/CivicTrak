#!/bin/bash

# Platform.sh sync script for CivicTrak
echo "🚀 CivicTrak Platform.sh Database Sync"
echo "===================================="

# Confirm before proceeding
read -p "⚠️  This will OVERWRITE the Platform.sh database. Continue? (y/N): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]
then
    echo "❌ Sync cancelled"
    exit 1
fi

echo "🔄 Starting database sync..."

# Export local database
echo "📤 Exporting local database..."
ddev drush sql-dump > /tmp/local-db-backup.sql

if [ $? -eq 0 ]; then
    echo "✅ Local database exported successfully"
    
    # Upload to Platform.sh
    echo "📤 Uploading to Platform.sh..."
    cat /tmp/local-db-backup.sql | platform ssh -e main "cat > /tmp/import.sql"
    
    echo "📥 Importing to Platform.sh database..."
    platform ssh -e main 'mysql -h $PLATFORM_RELATIONSHIPS_DATABASE_0_HOST -P $PLATFORM_RELATIONSHIPS_DATABASE_0_PORT -u $PLATFORM_RELATIONSHIPS_DATABASE_0_USERNAME -p$PLATFORM_RELATIONSHIPS_DATABASE_0_PASSWORD $PLATFORM_RELATIONSHIPS_DATABASE_0_PATH < /tmp/import.sql'
    
    # Clean up
    platform ssh -e main "rm /tmp/import.sql"
    rm /tmp/local-db-backup.sql
    
    echo "✅ Database sync completed successfully!"
    echo "🌐 Your changes are now live at: https://www.civictrak.com"
else
    echo "❌ Failed to export local database"
    exit 1
fi