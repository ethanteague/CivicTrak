#!/bin/bash

# Complete deployment script for CivicTrak
echo "🚀 CivicTrak Full Deployment"
echo "============================="

# Confirm before proceeding (unless --yes flag is passed)
if [[ "$1" != "--yes" ]]; then
    read -p "⚠️  This will push code AND overwrite production database. Continue? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]
    then
        echo "❌ Deployment cancelled"
        exit 1
    fi
fi

echo "📤 Step 1: Pushing code to origin..."
git push origin

if [ $? -eq 0 ]; then
    echo "✅ Code pushed successfully"
else
    echo "❌ Failed to push code"
    exit 1
fi

echo "🔄 Step 2: Syncing database to production..."
ddev drush sql-sync @self @civictrak.main -y

if [ $? -eq 0 ]; then
    echo "✅ Database synced successfully"
else
    echo "❌ Failed to sync database"
    exit 1
fi

echo "📁 Step 3: Syncing files to production..."
ddev drush rsync @self:%files @civictrak.main:%files -y

if [ $? -eq 0 ]; then
    echo "✅ Files synced successfully"
else
    echo "❌ Failed to sync files"
    exit 1
fi

echo "🧹 Step 4: Clearing production cache..."
ddev drush @civictrak.main cr

if [ $? -eq 0 ]; then
    echo "✅ Production cache cleared successfully"
else
    echo "❌ Failed to clear production cache"
    exit 1
fi

echo ""
echo "🎉 Deployment completed successfully!"
echo "🌐 Your changes are now live at: https://www.civictrak.com"
echo ""
echo "📋 Next steps:"
echo "   1. Submit updated sitemap to Google Search Console"
echo "   2. Request indexing for new municipal pages"
echo "   3. Monitor Google Analytics for traffic"