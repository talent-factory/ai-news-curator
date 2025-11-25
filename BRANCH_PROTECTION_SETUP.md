# Branch Protection Setup für develop

## 🔒 Branch Protection Regeln

Der `develop` branch ist geschützt, um die Code-Qualität sicherzustellen und sicherzustellen, dass nur geprüfte Änderungen eingehen.

## ⚙️ Setup (für Repository Owner)

### Option 1: Via GitHub Web UI (Empfohlen)

1. **Gehe zu Repository Settings:**
   ```
   https://github.com/talent-factory/ai-news-curator/settings/branches
   ```

2. **Branch Protection Rule hinzufügen:**
   - Klicke "Add branch protection rule"
   - Branch name pattern: `develop`

3. **Aktiviere folgende Settings:**

   **Require a pull request before merging:**
   - ✅ Aktivieren
   - Require approvals: 1
   - ✅ Dismiss stale pull request approvals when new commits are pushed
   - ✅ Require review from Code Owners (optional, wenn CODEOWNERS file existiert)

   **Require status checks to pass before merging:**
   - ⬜ Optional - aktivieren wenn CI/CD Tests existieren
   - Status checks: (später hinzufügen wenn Tests existieren)

   **Require conversation resolution before merging:**
   - ✅ Aktivieren (alle Kommentare müssen resolved sein)

   **Do not allow bypassing the above settings:**
   - ⬜ NICHT aktivieren (Owner soll weiterhin direkt pushen können)

   **Restrict who can push to matching branches:**
   - ✅ Aktivieren
   - Füge hinzu: `daniel-senften` (oder dein GitHub Username)
   - Nur diese User können direkt pushen

   **Allow force pushes:**
   - ⬜ NICHT aktivieren (keine force pushes)

   **Allow deletions:**
   - ⬜ NICHT aktivieren (develop kann nicht gelöscht werden)

4. **Save changes**

### Option 2: Via GitHub CLI

```bash
# Branch Protection mit gh CLI einrichten
gh api repos/talent-factory/ai-news-curator/branches/develop/protection \
  --method PUT \
  --field required_pull_request_reviews='{"required_approving_review_count":1,"dismiss_stale_reviews":true}' \
  --field restrictions='{"users":["daniel-senften"],"teams":[],"apps":[]}' \
  --field enforce_admins=false \
  --field required_status_checks=null \
  --field allow_force_pushes=false \
  --field allow_deletions=false
```

**Hinweis:** Ersetze `daniel-senften` mit deinem GitHub Username.

### Option 3: Via Repository Settings File (.github/settings.yml)

**Empfohlen für automatisches Setup mit [Probot Settings App](https://probot.github.io/apps/settings/):**

```yaml
# .github/settings.yml
branches:
  - name: develop
    protection:
      required_pull_request_reviews:
        required_approving_review_count: 1
        dismiss_stale_reviews: true
        require_code_owner_reviews: false
      restrictions:
        users:
          - daniel-senften
        teams: []
        apps: []
      enforce_admins: false
      required_status_checks: null
      allow_force_pushes: false
      allow_deletions: false
```

## 🔄 Workflow für Contributors

### Für Maintainer (Daniel)

```bash
# Direkt auf develop pushen (erlaubt)
git checkout develop
git add .
git commit -m "feat: Neue Funktion"
git push origin develop
```

### Für Contributors (Community)

```bash
# 1. Fork das Repository auf GitHub

# 2. Clone deinen Fork
git clone https://github.com/DEIN-USERNAME/ai-news-curator.git
cd ai-news-curator

# 3. Erstelle Feature Branch
git checkout develop
git checkout -b feature/meine-feature

# 4. Mache Änderungen
# ... (Code ändern)

# 5. Commit & Push zu deinem Fork
git add .
git commit -m "feat: Meine neue Feature"
git push origin feature/meine-feature

# 6. Erstelle Pull Request auf GitHub
# Base: talent-factory/ai-news-curator:develop
# Compare: DEIN-USERNAME/ai-news-curator:feature/meine-feature
```

## 📋 Pull Request Review Process

1. **Contributor erstellt PR**
   - PR wird automatisch auf develop gemerged-ready geprüft
   - Maintainer wird benachrichtigt

2. **Code Review durch Maintainer**
   - Mindestens 1 Approval erforderlich
   - Alle Kommentare müssen resolved sein
   - CI Tests müssen passieren (wenn konfiguriert)

3. **Merge**
   - Nach Approval kann der PR gemerged werden
   - Squash & Merge empfohlen für saubere History

## 🚨 Branch Protection Bypass

Nur der Repository Owner (daniel-senften) kann:
- Direkt auf develop pushen (ohne PR)
- Branch Protection Rules ändern
- Ausnahmen für spezielle Situationen machen

## 🔧 Troubleshooting

### "Protected branch push failed"

**Problem:** Du versuchst direkt auf develop zu pushen ohne Rechte.

**Lösung:** Erstelle einen PR statt direkt zu pushen:
```bash
git checkout -b fix/meine-fix
git push origin fix/meine-fix
# Dann PR auf GitHub erstellen
```

### "Required review approvals not met"

**Problem:** PR hat noch keine Approvals.

**Lösung:** Warte auf Maintainer Review oder frage nach Review.

### "Required conversation resolution not met"

**Problem:** Nicht alle Kommentare sind resolved.

**Lösung:** Gehe durch alle Kommentare und markiere sie als resolved.

## 📚 Weiterführende Links

- [GitHub Branch Protection](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches)
- [GitHub Pull Requests](https://docs.github.com/en/pull-requests)
- [Contributing Guide](CONTRIBUTING.md)

---

**Setup durchgeführt am:** TBD
**Maintainer:** @daniel-senften
