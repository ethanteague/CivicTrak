#!/bin/bash

# Simple Platform.sh sync without drush aliases
echo "🚀 Simple CivicTrak Database Sync"
echo "================================"

read -p "⚠️  This will OVERWRITE the Platform.sh database. Continue? (y/N): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]
then
    echo "❌ Sync cancelled"
    exit 1
fi

echo "🔄 Starting sync..."

# Method 1: Direct SQL export/import
echo "📤 Exporting local database..."
ddev drush sql-dump --gzip --result-file=/tmp/local-backup.sql.gz

echo "📤 Uploading to Platform.sh..."
platform mount:upload --mount=tmp --source=/tmp/local-backup.sql.gz --environment=main

echo "📥 Importing database on Platform.sh..."
platform ssh -e main "gunzip -c /tmp/local-backup.sql.gz | mysql -h \$PLATFORM_RELATIONSHIPS_DATABASE_0_HOST -P \$PLATFORM_RELATIONSHIPS_DATABASE_0_PORT -u \$PLATFORM_RELATIONSHIPS_DATABASE_0_USERNAME -p\$PLATFORM_RELATIONSHIPS_DATABASE_0_PASSWORD \$PLATFORM_RELATIONSHIPS_DATABASE_0_PATH"

# Clean up
platform ssh -e main "rm /tmp/local-backup.sql.gz"
rm /tmp/local-backup.sql.gz

echo "✅ Database sync completed!"
echo "🌐 Live at: https://www.civictrak.com"