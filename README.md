# 🎯 AI News Curator für Teaching

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![GitHub Stars](https://img.shields.io/github/stars/talent-factory/ai-news-curator?style=social)](https://github.com/talent-factory/ai-news-curator/stargazers)
[![GitHub Forks](https://img.shields.io/github/forks/talent-factory/ai-news-curator?style=social)](https://github.com/talent-factory/ai-news-curator/network/members)
[![GitHub Issues](https://img.shields.io/github/issues/talent-factory/ai-news-curator)](https://github.com/talent-factory/ai-news-curator/issues)
[![GitHub Pull Requests](https://img.shields.io/github/issues-pr/talent-factory/ai-news-curator)](https://github.com/talent-factory/ai-news-curator/pulls)
[![Last Commit](https://img.shields.io/github/last-commit/talent-factory/ai-news-curator)](https://github.com/talent-factory/ai-news-curator/commits/develop)
[![Code Style: Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

> Intelligenter News-Filter speziell für **Software-Entwicklung mit KI** und **KI-Integration in Produkte** Schulungen.

**Version 2.0:** Jetzt mit erweitertem LLM- und CLI-Tool-Fokus! 🚀

## 🎓 Das Problem

Als Dozent für KI-Schulungen stehst du vor einer riesigen Herausforderung:

- 📰 Täglich erscheinen dutzende AI/ML News auf Hacker News, Reddit, GitHub
- ⚡ Die Entwicklung ist rasant: Neue LLMs, API-Updates, neue CLI-Tools, Breaking Changes
- 🎯 Nur ein Bruchteil ist für deine Studierenden relevant
- ⏰ Keine Zeit, alles manuell zu sichten und zu bewerten
- 🔍 Schwierig zu unterscheiden: Marketing-Hype vs. echte Innovation
- ⌨️ CLI-basierte Entwicklungsumgebungen werden immer wichtiger, aber schwer zu tracken

**Die Folge:** Du verpasst wichtige Updates oder verbringst Stunden mit News-Screening.

## 💡 Die Lösung

Ein intelligenter AI News Curator, der:

- ✅ **Automatisch** relevante News sammelt (Hacker News, Reddit, GitHub, Tech-Blogs)
- ✅ **Mit Claude API** die Relevanz für deine Schulungen bewertet
- ✅ **Priorisiert** nach Teaching-Relevanz (Score 1-5)
- ✅ **Kategorisiert** (LLM-Releases, CLI-Tools, Teaching, Tools, Research)
- ✅ **LLM-Fokus:** Erkennt neue Modelle (Claude, GPT, Gemini, o1, Deepseek)
- ✅ **CLI-Tool-Fokus:** Trackt Cursor, Windsurf, Claude Code, Auggie, Antigravity
- ✅ **Tägliche Reports** generiert mit direkten Links und Kontext
- ✅ **Optional automatisiert** läuft via GitHub Actions
- ✅ **Wartbarer Prompt** in separater Datei (`prompt_template.txt`)

## 🌟 Features

### 🤖 Intelligente Claude-Integration (NEU v2.0)
- **Erweiterter Tech-Stack:** Claude, GPT, Gemini, o1, Deepseek, Llama, Mistral
- **CLI-Tools:** Cursor, Windsurf, Claude Code, Auggie, Antigravity, Bolt.new, v0.dev
- **Kontext-bewusstes Filtern:** Claude versteht moderne Dev-Workflows
- **Teaching-Fokus:** Bewertet nicht "cool", sondern "unterrichtsrelevant"
- **Reasoning:** Erklärt, WARUM eine News wichtig ist
- **Wartbarer Prompt:** Externe Datei für einfache Anpassungen

### 📰 News-Quellen
- Hacker News (AI/LLM/Claude/GPT/Cursor/Windsurf Keywords)
- Reddit (r/LocalLLaMA, r/ClaudeAI, r/OpenAI, etc.)
- GitHub Trending (AI/ML Repos mit Filter)
- Erweiterbar um eigene RSS-Feeds

### 📊 Output (NEU v2.0)
- **Markdown Reports** mit direkten Links
- **Priorisierte Struktur:** High-Priority → Medium → Low
- **6 Kategorien mit Emojis:**
  - 🤖 LLM-Releases (Claude, GPT, Gemini, o1, etc.)
  - ⌨️ CLI-Tools (Cursor, Windsurf, Claude Code, etc.)
  - 🎓 Teaching (Direkt unterrichtsrelevant)
  - 🛠️ Tools (Dev-Tools, Extensions)
  - 🔬 Research (Experimentelles)
- **Kategorien-Statistik** am Ende des Reports
- **GitHub Issues** (optional) für High-Priority Items
- **Automatisierbar** via GitHub Actions oder Cron

## 🔄 Wie es funktioniert

```
1. News Sammeln
   ├─ Hacker News (Top AI-Topics)
   ├─ Reddit (r/LocalLLaMA, r/ClaudeAI, etc.)
   ├─ GitHub Trending (AI/ML Repos)
   └─ [Optional: Eigene RSS-Feeds]

2. Claude Analyse (pro News-Item)
   ├─ Kontext: Deine Schulungsthemen
   ├─ Bewertung: Relevanz-Score 1-5
   ├─ Kategorisierung: Teaching/Tools/Research
   └─ Reasoning: Warum relevant/nicht relevant

3. Report Generierung
   ├─ Sortiert nach Priorität
   ├─ Markdown-Format
   └─ Mit direkten Links & Kontext

4. [Optional] Automatisierung
   ├─ GitHub Actions: Täglich um 08:00
   ├─ Auto-Commit des Reports
   └─ GitHub Issues für High-Priority
```

**Beispiele von Claude-Analysen:**
```
Input: "Claude 3.7 Opus Released with 500K Context Window"
Claude analysiert:
- Relevanz: 5/5 (Major LLM Release, direkt relevant)
- Kategorie: llm_release 🤖
- Reasoning: "Wichtiges Update für Haupt-LLM der Schulung"

Input: "Cursor 0.42: Multi-Agent Code Editing"
Claude analysiert:
- Relevanz: 5/5 (Breaking Change in Haupt-IDE)
- Kategorie: cli_tools ⌨️
- Reasoning: "Studierende nutzen Cursor täglich, Update sofort relevant"

Input: "Google Antigravity: Neue agentic IDE mit Gemini"
Claude analysiert:
- Relevanz: 4/5 (Neuer Konkurrent zu Cursor/Windsurf)
- Kategorie: cli_tools ⌨️
- Reasoning: "Zeigt zukünftige CLI-Tool-Entwicklung, wichtiger Vergleich"
```

## 🚀 Quick Start

- 📖 **Neu hier?** Lies zuerst die [5-Minuten Quick-Start Anleitung](QUICK_START.md)
- 🤖 **Claude API & Prompt Details?** Siehe [Claude Integration Dokumentation](CLAUDE.md)
- 🆕 **NEU in v2.0?** Siehe [CHANGELOG](#-changelog-v20) am Ende

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

**Tipp:** Der Prompt ist jetzt in `prompt_template.txt` - passe ihn nach Bedarf an!

## 📁 Projektstruktur

```
ai-news-curator/
├── ai_news_curator.py          # Hauptscript mit Claude-Integration
├── prompt_template.txt         # 🆕 Externer Analyse-Prompt (anpassbar!)
├── config.yaml                 # Konfiguration (Quellen, Filter, etc.)
├── requirements.txt            # Python Dependencies
├── test_sources.py             # Test-Script (ohne API Key)
│
├── README.md                   # Diese Datei
├── QUICK_START.md              # 5-Minuten Setup Guide
├── CLAUDE.md                   # Claude API & Prompt Engineering Guide
├── GITHUB_ACTIONS_SETUP.md     # GitHub Actions Anleitung
├── example_output.md           # Beispiel-Report
│
└── .github/
    └── workflows/
        ├── daily_news.yml          # Vollständiger Workflow
        └── daily_news_simple.yml   # Einfacher Workflow (empfohlen)
```

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
   - Läuft automatisch täglich um 05:00 UTC (06:00 CET)
   - Manuelles Triggern: Actions Tab → "Daily AI News Digest" → "Run workflow"

3. **Reports finden:**
   - Werden automatisch ins Repo committed
   - High-Priority Items erstellen GitHub Issues

4. **⚠️ Wichtig bei manuellen Workflow-Triggers:**

   Wenn du Code-Änderungen im Workflow gemacht hast und manuell triggern willst:

   - **Option 1 (empfohlen):** Warte 2-3 Minuten nach dem Push, bevor du manuell triggerst
     - GitHub cached Workflow-Definitionen
     - Die UI zeigt manchmal alte Commits

   - **Option 2 (sofort):** Nutze GitHub CLI:
     ```bash
     gh workflow run daily_news.yml --ref develop
     ```

   - **Scheduled Runs** verwenden immer automatisch den aktuellsten Commit ✅

   **Hintergrund:** GitHub Actions kann beim manuellen Trigger eine gecachte/alte Version des Workflows verwenden. Der automatische scheduled Run hat dieses Problem nicht.

### Automatisiert via Cron (Linux/Mac)

```bash
crontab -e
```

Füge hinzu:
```bash
0 8 * * * cd /pfad/zu/ai-news-curator && /usr/bin/python3 ai_news_curator.py
```

## 📊 Output Format (NEU v2.0)

```markdown
# 🎯 AI News Digest für Teaching
**Datum:** 2025-11-25

---

## 🔥 Sofort relevant (Score 4-5)

### 🤖 Claude 3.7 Opus Released
**Quelle:** Hacker News | **Score:** 5/5 | **Kategorie:** llm_release

💡 **Warum relevant:** Major LLM Release mit 500K Context Window.
Direkt relevant für Schulung.

🔗 [Link](https://...)

---

### ⌨️ Cursor 0.42: Multi-Agent Code Editing
**Quelle:** GitHub | **Score:** 5/5 | **Kategorie:** cli_tools

💡 **Warum relevant:** Breaking Change in Haupt-IDE. Studierende
nutzen Cursor täglich.

🔗 [Link](https://...)

---

## 📊 Beobachten (Score 3)

- 🛠️ **New RAG Pattern** - Interessante Architektur...
- 🔬 **Research: Better Prompting** - Gut für Semesterarbeiten...

---
**Total analysierte Items:** 25
**Hochpriorität:** 7
**Mittelpriorität:** 5

**Nach Kategorien:**
- 🤖 llm_release: 3
- ⌨️ cli_tools: 5
- 🎓 teaching: 2
- 🛠️ tools: 8
- 🔬 research: 7
```

## ⚙️ Konfiguration

### Prompt anpassen (NEU v2.0)

**Einfach:** Editiere `prompt_template.txt`

```bash
nano prompt_template.txt
# oder
code prompt_template.txt
```

Passe an:
- **Tech-Stack:** Füge neue LLMs/Tools hinzu
- **Kontext:** Ändere Schulungs-Fokus
- **Kategorien:** Definiere neue Kategorien
- **Scoring:** Passe Bewertungskriterien an

Siehe [CLAUDE.md](CLAUDE.md) für detaillierte Anleitung zum Prompt Engineering.

### Weitere Konfiguration

`config.yaml` (optional):
- **News-Quellen:** Blogs, Subreddits, GitHub Topics
- **Filter-Kriterien:** Was ist hochprior für deine Schulungen?
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

**Claude API Kosten (NEU v2.0):**
- ~20-30 Items pro Tag
- ~800 tokens Input pro Analyse (erweiterter Prompt)
- ~120 tokens Output
- **Gesamt:** ~$0.08 pro Tag = ~$2.40/Monat (mit Claude Sonnet 4)

**Details:** Siehe [CLAUDE.md - Kosten & Rate Limits](CLAUDE.md#-kosten--rate-limits)

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

### Manueller Workflow-Trigger verwendet alte Code-Version
**Problem:** Du hast Code geändert, aber der manuelle Run verwendet die alte Version.

**Ursache:** GitHub Actions cached Workflow-Definitionen. Beim manuellen Trigger kann GitHub eine alte Branch-Referenz verwenden.

**Lösung:**
```bash
# Option 1: Warte 2-3 Minuten nach dem Push, dann triggern

# Option 2: Nutze CLI für sofortiges Triggern mit aktuellem Code
gh workflow run daily_news.yml --ref develop

# Option 3: Warte auf den scheduled Run (verwendet immer aktuellen Code)
```

## 📝 CHANGELOG v2.0

### 🆕 Neue Features
- ✅ **Externe Prompt-Datei:** `prompt_template.txt` für einfache Wartung
- ✅ **Erweiterte LLM-Coverage:** Claude, GPT, Gemini, o1, Deepseek, Llama, Mistral
- ✅ **CLI-Tool-Fokus:** Cursor, Windsurf, Claude Code, Auggie, Antigravity, Bolt.new, v0.dev
- ✅ **Neue Kategorien:** `llm_release` und `cli_tools` mit Emojis
- ✅ **Kategorien-Statistik:** Am Ende jedes Reports
- ✅ **Fallback-Prompt:** Automatisches Fallback wenn Template fehlt

### 🔧 Technische Verbesserungen
- Prompt-Template in separater Datei (bessere Wartbarkeit)
- Erweiterte Relevanz-Kriterien für LLMs und CLI-Tools
- Verbesserte Report-Formatierung mit Emojis
- Kategorie-Tracking und Statistiken

### 📚 Dokumentation
- Komplett überarbeitetes [CLAUDE.md](CLAUDE.md) mit Prompt Engineering Guide
- Aktualisiertes [README.md](README.md) mit v2.0 Features
- Beispiele für neue Kategorien und Bewertungen

### 💰 Kosten
- Leicht höhere API-Kosten durch längeren Prompt (~$0.08/Tag statt $0.06/Tag)
- Immer noch sehr günstig: ~$2.40/Monat

## 🔮 Roadmap v2.1+

- [ ] **Prompt Caching:** 90% Kosten-Reduktion durch Claude Prompt Caching
- [ ] **Batch-Processing:** 5 Items pro API-Request (80% weniger Calls)
- [ ] Slack/Discord Bot Integration
- [ ] Web Dashboard mit Trend-Analyse
- [ ] Multi-Language Support (EN/DE)
- [ ] PDF Export mit Grafiken
- [ ] Duplicate Detection über Tage hinweg

## 🤝 Contributing

Wir freuen uns über Beiträge! 🎉

Dieses Projekt ist Open Source und lädt die Community ein:

- 🐛 **Bug Reports:** Melde Probleme via [GitHub Issues](https://github.com/talent-factory/ai-news-curator/issues)
- ✨ **Feature Requests:** Schlage neue Features vor
- 💻 **Pull Requests:** Trage Code bei (siehe [CONTRIBUTING.md](CONTRIBUTING.md))
- 📚 **Dokumentation:** Verbessere Docs und Guides
- 🎨 **Prompt Engineering:** Optimiere den Analyse-Prompt
- 🌍 **Übersetzungen:** Übersetze für andere Sprachen/Domänen

**Branch Protection:**
- `develop` branch ist geschützt
- Nur Maintainer können direkt pushen
- Alle anderen: Fork + Pull Request

Lies unseren [Contributing Guide](CONTRIBUTING.md) für Details!

## 📄 License

MIT License - Use freely for educational and commercial purposes.

See [LICENSE](LICENSE) for full details.

---

**Entwickelt für:** Talent Factory GmbH
**Kontext:** Software-Entwicklung mit KI & KI-Integration
**Powered by:** Claude API (Anthropic)
**Version:** 2.0 - LLM & CLI-Tool Focus
**License:** MIT - Open Source
**Community:** [Contributing Guide](CONTRIBUTING.md) | [Code of Conduct](CODE_OF_CONDUCT.md) | [Security Policy](SECURITY.md)
