#!/bin/bash
# Quick script to push File Explorer to GitHub
# Usage: ./push_to_github.sh YOUR_GITHUB_USERNAME

if [ -z "$1" ]; then
    echo "Usage: ./push_to_github.sh YOUR_GITHUB_USERNAME"
    echo "Example: ./push_to_github.sh johndoe"
    exit 1
fi

USERNAME=$1
REPO_NAME="file-explorer"

echo "🚀 Preparing to push to GitHub..."
echo "Repository: https://github.com/$USERNAME/$REPO_NAME"
echo ""

# Check if remote already exists
if git remote | grep -q "^origin$"; then
    echo "⚠️  Remote 'origin' already exists. Removing it..."
    git remote remove origin
fi

# Add remote
echo "📡 Adding remote repository..."
git remote add origin https://github.com/$USERNAME/$REPO_NAME.git

# Push
echo "⬆️  Pushing to GitHub..."
git push -u origin main

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Successfully pushed to GitHub!"
    echo "🌐 View your repository at: https://github.com/$USERNAME/$REPO_NAME"
else
    echo ""
    echo "❌ Push failed. Make sure:"
    echo "   1. You've created the repository on GitHub"
    echo "   2. You have the correct permissions"
    echo "   3. You're authenticated (may need Personal Access Token)"
    echo ""
    echo "See DEPLOY.md for detailed instructions."
fi

