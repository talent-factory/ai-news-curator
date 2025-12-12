#!/bin/bash
# Script to create Pull Request via GitHub API
# Usage: ./create_pr.sh YOUR_GITHUB_TOKEN

if [ -z "$1" ]; then
    echo "❌ Error: GitHub Token required"
    echo "Usage: ./create_pr.sh YOUR_GITHUB_TOKEN"
    echo ""
    echo "Create a token at: https://github.com/settings/tokens/new"
    echo "Required scopes: repo"
    exit 1
fi

GITHUB_TOKEN="$1"
REPO_OWNER="talent-factory"
REPO_NAME="ai-news-curator"
HEAD_BRANCH="claude/prevent-issue-spam-01HDoWz63m8dyp3nfGBVS7AA"
BASE_BRANCH="develop"

PR_TITLE="feat: Prevent spam comments on auto-generated issues"

PR_BODY=$(cat <<'EOF'
## 🎯 Zusammenfassung

Implementiert zweistufigen Spam-Schutz für automatisch erstellte AI News Issues.

## 🔒 Änderungen

### 1. Auto-Lock für neue Issues
- Issues werden automatisch nach Erstellung gesperrt
- Nur Collaborators können kommentieren
- Issues bleiben öffentlich sichtbar
- Lock-Reason: `spam`

### 2. Automatische Spam-Moderation
- Neue GitHub Action überwacht alle Issue-Kommentare
- Erkennt Spam anhand von Patterns (Werbung, Crypto, excessive Links)
- Löscht Spam automatisch
- Collaborators sind auf Whitelist

## 📁 Geänderte Dateien

- ✏️ `.github/workflows/daily_news.yml` - Auto-Lock nach Issue-Erstellung
- ✨ `.github/workflows/spam_moderation.yml` - Neue Spam-Detection Action

## 🧪 Test Plan

- [ ] Workflow manuell triggern
- [ ] Prüfen, dass neues Issue automatisch gesperrt ist

## ✅ Checklist

- [x] Code committed und gepusht
- [x] Spam-Patterns definiert
- [x] Collaborator-Whitelist implementiert
- [x] Lock-Reason gesetzt
EOF
)

echo "🚀 Creating Pull Request..."
echo "   Repository: $REPO_OWNER/$REPO_NAME"
echo "   Base: $BASE_BRANCH ← Head: $HEAD_BRANCH"
echo ""

RESPONSE=$(curl -s -X POST \
  -H "Authorization: token $GITHUB_TOKEN" \
  -H "Accept: application/vnd.github.v3+json" \
  https://api.github.com/repos/$REPO_OWNER/$REPO_NAME/pulls \
  -d "$(jq -n \
    --arg title "$PR_TITLE" \
    --arg body "$PR_BODY" \
    --arg head "$HEAD_BRANCH" \
    --arg base "$BASE_BRANCH" \
    '{title: $title, body: $body, head: $head, base: $base}')")

# Check if PR was created successfully
PR_URL=$(echo "$RESPONSE" | jq -r '.html_url // empty')

if [ -n "$PR_URL" ]; then
    echo "✅ Pull Request created successfully!"
    echo "🔗 $PR_URL"
else
    ERROR=$(echo "$RESPONSE" | jq -r '.message // "Unknown error"')
    echo "❌ Failed to create PR: $ERROR"
    echo ""
    echo "Full response:"
    echo "$RESPONSE" | jq '.'
    exit 1
fi
