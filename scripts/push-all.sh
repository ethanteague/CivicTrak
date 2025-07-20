#!/bin/bash

# === CivicTrak Multi-Site Platform.sh Deployment Script ===
# Push the current GitHub repo to multiple Platform.sh project remotes
# Set this up in your canonical repo (e.g., ethanteague/CivicTrak)

# List of Platform.sh project IDs and optional envs
# Format: ["project_id_1:env_name" "project_id_2:env_name"]
PROJECTS=(
  "aix7krbcuwq3u:main"
)

# Set your local CivicTrak repo path
REPO_PATH="$HOME/workspace/govt"

cd "$REPO_PATH" || exit 1

echo "\n🚀 Starting CivicTrak multi-site push from: $REPO_PATH\n"

for PROJECT_ENV in "${PROJECTS[@]}"; do
  PROJECT_ID="${PROJECT_ENV%%:*}"
  ENVIRONMENT="${PROJECT_ENV##*:}"

  echo "🔗 Setting Platform.sh remote for project $PROJECT_ID"
  platform project:set-remote "$PROJECT_ID" --yes

  echo "⬆️  Pushing code to project $PROJECT_ID (env: $ENVIRONMENT)..."
  platform push --yes

  echo "✅ Deployed to https://$ENVIRONMENT-$PROJECT_ID.platform.sh"
  echo "----------------------------------------"
done

echo "\n🎉 All Platform.sh projects updated from GitHub repo.\n"
