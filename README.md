# 🎯 AI News Curator für Teaching

Intelligenter News-Filter speziell für **Software-Entwicklung mit KI** und **KI-Integration in Produkte** Schulungen.

## 🌟 Features

- ✅ **Automatische News-Sammlung** von 10+ relevanten Quellen
- 🤖 **Claude-powered Relevanz-Analyse** mit kontextuellem Verständnis
- 📊 **Intelligente Kategorisierung** (Teaching, Tools, Research)
- 🔥 **Prioritäts-Scoring** (1-5) basierend auf Unterrichtsrelevanz
- 📝 **Markdown Reports** für einfaches Sharing
- ⚡ **GitHub Actions Integration** für tägliche Auto-Runs

## 🚀 Quick Start

### 1. Repository Setup

```bash
git clone <dein-repo>
cd ai-news-curator
```

### 2. Dependencies installieren

```bash
pip install -r requirements.txt
```

### 3. API Key konfigurieren

```bash
export ANTHROPIC_API_KEY='sk-ant-...'
```

Oder für permanente Konfiguration in `~/.bashrc` oder `~/.zshrc`:
```bash
echo 'export ANTHROPIC_API_KEY="sk-ant-..."' >> ~/.bashrc
```

### 4. Ersten Report generieren

```bash
python ai_news_curator.py
```

Output: `ai_news_digest_YYYYMMDD.md`

## 📖 Verwendung

### Lokales Ausführen

```bash
# Letzte 24 Stunden
python ai_news_curator.py

# Letzte 48 Stunden
# (in ai_news_curator.py: curator.run(hours_back=48))
```

### Automatisiert via GitHub Actions

1. **GitHub Secret hinzufügen:**
   - Gehe zu: Repository Settings → Secrets and Variables → Actions
   - Klicke: "New repository secret"
   - Name: `ANTHROPIC_API_KEY`
   - Value: Dein Claude API Key

2. **Workflow aktivieren:**
   - Läuft automatisch täglich um 08:00 CET
   - Manuelles Triggern: Actions Tab → "Daily AI News Digest" → "Run workflow"

3. **Reports finden:**
   - Werden automatisch ins Repo committed
   - High-Priority Items erstellen GitHub Issues

### Automatisiert via Cron (Linux/Mac)

```bash
crontab -e
```

Füge hinzu:
```bash
0 8 * * * cd /pfad/zu/ai-news-curator && /usr/bin/python3 ai_news_curator.py
```

## 📊 Output Format

```markdown
# 🎯 AI News Digest für Teaching
**Datum:** 2025-11-21

---

## 🔥 Sofort relevant (Score 4-5)

### Google Antigravity: Neue agentic IDE
**Quelle:** Hacker News | **Score:** 5/5 | **Kategorie:** tools

💡 **Warum relevant:** Direkter Konkurrent zu Windsurf/Cursor. 
Studierende sollten Vergleich kennen. Agent-first Ansatz zeigt 
zukünftige Entwicklung.

🔗 [Link](https://...)

---

## 📊 Beobachten (Score 3)

- **Claude 3.5 Sonnet Update** - Performance Improvements...
- **New RAG Pattern** - Interessante Architektur...
```

## ⚙️ Konfiguration

Passe `config.yaml` an für:
- **News-Quellen:** Blogs, Subreddits, GitHub Topics
- **Filter-Kriterien:** Was ist hochprior für deine Schulungen?
- **Tech-Stack:** Welche Tools nutzt dein Team?
- **Timing:** Wann soll der Digest laufen?

## 🎓 Use Cases für Teaching

### 1. Wöchentliche "What's New" Session
```bash
# Letzten 7 Tage
python ai_news_curator.py  # Anpassen: hours_back=168
```
→ Zeige Studierenden die wichtigsten Updates der Woche

### 2. Kursinhalt aktualisieren
- High-Priority Items (Score 5) → Sofort in Slides einbauen
- Medium-Priority (Score 3-4) → Für nächstes Semester merken

### 3. Student Research Topics
- Research-Category Items → Thesis/Projekt-Themen

## 🔧 Erweiterte Anpassungen

### Eigene News-Quelle hinzufügen

```python
# In ai_news_curator.py, Methode fetch_news()

# Beispiel: Eigener RSS Feed
custom_feed = feedparser.parse('https://your-blog.com/rss')
for entry in custom_feed.entries:
    news_items.append({
        'title': entry.title,
        'url': entry.link,
        'source': 'Your Blog',
        'published': entry.published,
        'summary': entry.summary
    })
```

### Slack/Discord Integration

```python
# Nach Report-Generierung
import requests

webhook_url = "https://hooks.slack.com/services/..."
requests.post(webhook_url, json={"text": report})
```

### Notion Integration

```python
from notion_client import Client

notion = Client(auth=os.getenv("NOTION_TOKEN"))
# Erstelle neue Page mit Report
```

## 📈 Kosten & Limits

**Claude API Kosten:**
- ~10-20 Items pro Tag
- ~200 tokens pro Analyse
- **Gesamt:** ~$0.10-0.30 pro Tag (mit Claude Sonnet 4)

**GitHub Actions:**
- 2000 Minuten/Monat kostenlos (Public Repos)
- ~2-3 Minuten pro Run
- **Gesamt:** Kostenlos für Daily Digest

## 🛠️ Troubleshooting

### "ANTHROPIC_API_KEY nicht gesetzt"
```bash
echo $ANTHROPIC_API_KEY  # Sollte Key zeigen
export ANTHROPIC_API_KEY='dein-key'
```

### Keine News gefunden
- Prüfe Internetverbindung
- Manche Feeds können temporär down sein
- Erhöhe `hours_back` Parameter

### GitHub Action läuft nicht
- Prüfe: Repository Settings → Actions → "Allow all actions"
- Secret korrekt gesetzt?
- Workflow-File in `.github/workflows/` ?

## 🔮 Roadmap

- [ ] Slack/Discord Bot Integration
- [ ] Web Dashboard mit Trend-Analyse
- [ ] Multi-Language Support (EN/DE)
- [ ] PDF Export mit Grafiken
- [ ] Duplicate Detection über Tage hinweg
- [ ] Custom Training für Teaching-Kontext

## 🤝 Contributing

Dieses Tool ist für **Talent Factory GmbH** entwickelt, aber gerne:
- Issues für Bugs oder Feature Requests
- Pull Requests für Verbesserungen
- Teile deine Anpassungen für andere Schulungs-Kontexte

## 📄 License

MIT License - Use freely for educational purposes

---

**Entwickelt für:** Talent Factory GmbH  
**Kontext:** Software-Entwicklung mit KI & KI-Integration  
**Powered by:** Claude API (Anthropic)
