# Security Policy

## 🔒 Sicherheit beim AI News Curator

Die Sicherheit unserer Nutzer und der Community ist uns wichtig. Dieses Dokument beschreibt unsere Security Policy und wie du Sicherheitslücken melden kannst.

## 🛡️ Unterstützte Versionen

Wir bieten Security Updates für folgende Versionen:

| Version | Supported          |
| ------- | ------------------ |
| 2.0.x   | :white_check_mark: |
| < 2.0   | :x:                |

## 🚨 Sicherheitslücken melden

**Bitte melde Sicherheitslücken NICHT über öffentliche GitHub Issues!**

### Reporting Process

1. **E-Mail an:** daniel.senften@talent-factory.ch
2. **Betreff:** [SECURITY] AI News Curator - Kurze Beschreibung
3. **Inhalt:**
   - Beschreibung der Sicherheitslücke
   - Schritte zur Reproduktion
   - Mögliche Auswirkungen
   - Vorschläge für Fixes (optional)

### Was du erwarten kannst

- **Bestätigung:** Innerhalb von 48 Stunden
- **Erste Einschätzung:** Innerhalb von 7 Tagen
- **Updates:** Regelmässige Updates zum Status
- **Fix & Disclosure:** Koordinierte Veröffentlichung nach Fix

### Responsible Disclosure

Wir bitten dich:

- Gib uns angemessene Zeit, das Problem zu beheben (90 Tage)
- Veröffentliche keine Details vor koordinierter Disclosure
- Vermeide Datenzerstörung oder -diebstahl
- Teste nicht auf Production-Systemen anderer Nutzer

### Anerkennung

- Wir würdigen verantwortungsvolle Sicherheitsforscher im CHANGELOG
- Mit deinem Einverständnis nennen wir dich in Security Advisories

## 🔐 Best Practices für Nutzer

### API Keys schützen

**DO:**

- ✅ API Keys in `.env` Files speichern
- ✅ Environment Variables nutzen
- ✅ `.env` in `.gitignore` haben
- ✅ Unterschiedliche Keys für Dev/Prod
- ✅ Keys regelmässig rotieren

**DON'T:**

- ❌ Keys in Code committed
- ❌ Keys in Config-Files
- ❌ Keys in Screenshots/Logs
- ❌ Keys in Issue-Beschreibungen
- ❌ Keys in öffentlichen Repos

### Falls ein Key versehentlich committed wurde

1. **Sofort:** Widerrufe/regeneriere den Virtual Key am TF LLM-Gateway (`scripts/provision_keys.sh`)
2. **Entfernen:** Nutze `git filter-branch` oder BFG Repo-Cleaner
3. **Force Push:** Nur für eigenen Fork, NICHT für Main Repo
4. **Melden:** Informiere Maintainer wenn es im Main Repo war

```bash
# Key aus Git History entfernen (VORSICHT!)
git filter-branch --force --index-filter \
  "git rm --cached --ignore-unmatch .env" \
  --prune-empty --tag-name-filter cat -- --all

# Force Push zu deinem Fork
git push origin --force --all
```

**Besser:** Nutze [BFG Repo-Cleaner](https://rtyley.github.io/bfg-repo-cleaner/)

### Sicherer GitHub Actions Workflow

```yaml
# ✅ Richtig: Nutze GitHub Secrets
- name: Run AI News Curator
  env:
    GATEWAY_KEY: ${{ secrets.NEWS_CURATOR_GATEWAY_KEY }}
  run: python ai_news_curator.py

# ❌ Falsch: Nie Keys im YAML hardcoden
- name: Run AI News Curator
  env:
    GATEWAY_KEY: "sk-..."  # NIEMALS!
  run: python ai_news_curator.py
```

## 🛡️ Bekannte Sicherheitsüberlegungen

### API Key Exposure

**Risiko:** API Keys könnten in Logs auftauchen

**Mitigation:**

- Script loggt niemals Keys
- Fehler-Messages enthalten keine Keys
- GitHub Actions maskiert Secrets automatisch

### Dependency Vulnerabilities

**Risiko:** Abhängigkeiten könnten Sicherheitslücken haben

**Mitigation:**

- Regelmässige `pip install --upgrade`
- Dependabot aktiviert (empfohlen)
- Security Advisories beachten

### Prompt Injection

**Risiko:** Böswillige News könnten versuchen, den Prompt zu manipulieren

**Mitigation:**

- Prompt-Template verwendet `{placeholder}` statt f-strings
- Keine Execution von Code aus News
- Input-Längen sind begrenzt

### Rate Limiting

**Risiko:** Zu viele API-Calls könnten Account blockieren

**Mitigation:**

- Built-in Rate Limiting (300ms zwischen Calls)
- Fehler-Handling bei Rate Limit Errors
- Configurable `hours_back` Parameter

## 🔍 Security Audits

### Letzte Audits

- **v2.0 (2025-01):** Internal Security Review
  - API Key Handling ✅
  - Dependency Check ✅
  - Prompt Injection Check ✅

### Geplante Audits

- Regelmässige Dependency Updates
- Community Security Reviews

## 📚 Security Resources

### Für Entwickler

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Python Security Best Practices](https://python.readthedocs.io/en/stable/library/security_warnings.html)
- [GitHub Security Best Practices](https://docs.github.com/en/code-security)

### Für Nutzer

- [Anthropic API Security](https://docs.anthropic.com/en/api/security)
- [GitHub Secrets](https://docs.github.com/en/actions/security-guides/encrypted-secrets)

## 🤝 Security Acknowledgments

Wir danken folgenden Security Researchers:

<!-- Wird aktualisiert bei gemeldeten Vulnerabilities -->

_Noch keine gemeldeten Vulnerabilities_

## 📞 Kontakt

**Security Team:** daniel.senften@talent-factory.ch

**PGP Key:** (Optional, falls gewünscht)

---

**Letztes Update:** 2025-11-25
**Version:** 2.0
