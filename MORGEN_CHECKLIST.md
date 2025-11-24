# ✅ Morgen-Checklist - Nach dem automatischen Run um 08:00 CET

## 📅 Erwartetes Verhalten

**06:00 CET** - GitHub Actions Workflow startet automatisch

Der Workflow wird:
1. ✅ 40 News von Hacker News, Reddit, GitHub sammeln
2. ✅ Mit Claude API analysieren (100% Erfolgsrate erwartet)
3. ✅ Markdown-Report generieren: `ai_news_digest_YYYYMMDD.md`
4. ✅ Automatisch zum `develop` Branch committen

## 🔍 So prüfst du, ob es funktioniert hat:

### Option 1: Lokales Git Pull (Terminal)

```bash
cd ~/GitRepository/ai-news-curator
git pull origin develop

# Neuer Report sollte da sein:
ls -la ai_news_digest_*.md

# Report ansehen:
cat ai_news_digest_$(date +%Y%m%d).md
```

### Option 2: GitHub Web UI

**Prüfe den Workflow-Run:**
```
https://github.com/talent-factory/ai-news-curator/actions
```
- Sollte einen grünen ✅ Run zeigen: "Daily AI News Digest (Simple)"
- Klicke darauf für Details

**Prüfe den neuen Commit:**
```
https://github.com/talent-factory/ai-news-curator/commits/develop
```
- Neuer Commit sollte da sein: "📰 Daily AI News Digest 2025-11-24"

**Prüfe den Report direkt:**
```
https://github.com/talent-factory/ai-news-curator/blob/develop/ai_news_digest_20251124.md
```

## ⚠️ Was tun bei Problemen?

### Workflow ist nicht gelaufen

**Prüfe:**
```bash
gh workflow list
gh run list --workflow="Daily AI News Digest"
```

**Manuell triggern:**
1. https://github.com/talent-factory/ai-news-curator/actions
2. "Daily AI News Digest" → "Run workflow"

### Workflow ist fehlgeschlagen

**Prüfe Logs:**
```bash
gh run view --log
# oder
gh run list --limit 1
gh run view <RUN_ID> --log
```

**Häufige Fehler:**
- API Key fehlt → Secret nochmal setzen
- Rate Limit → Warten und erneut versuchen
- Permissions → Workflow braucht `write` Permission

### Report wurde nicht committed

**Prüfe Workflow-Logs:**
- Schritt "Commit and Push Report" ansehen
- Mögliche Ursache: Git-Konflikt oder Permission-Problem

## 📊 Erwartete Metriken

**Basierend auf heutigem Test:**
- ✅ ~40 News-Items gesammelt
- ✅ 100% Erfolgsrate (40/40 analysiert)
- ✅ ~22 High-Priority Items (Score 4-5)
- ✅ ~9 Medium-Priority Items (Score 3)
- ⏱️ Laufzeit: ~2-3 Minuten

## 🎯 Nächste Schritte nach erfolgreichem Run

1. **Report reviewen** - Sind die Bewertungen sinnvoll?
2. **Konfiguration anpassen** (optional)
   - `config.yaml` - Andere News-Quellen?
   - Prompt in `ai_news_curator.py` - Bessere Filter?
3. **Slack/Discord Integration** (optional)
4. **Wöchentliches Digest** statt täglich? (Cron anpassen)

## 📞 Support

Bei Fragen oder Problemen:
- Check Logs: `gh run view --log`
- Check Workflow: https://github.com/talent-factory/ai-news-curator/actions
- Dokumentation: README.md, CLAUDE.md, GITHUB_ACTIONS_SETUP.md
