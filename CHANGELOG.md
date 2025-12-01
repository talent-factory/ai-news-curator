# Changelog - AI News Curator

## Version 2.1 - News Detection Fix & Enhanced Sources (2025-12-01)

### 🎯 Problem behoben

**Hauptproblem:** Der Curator hat in den letzten Tagen keine News mehr gefunden, obwohl früher 30-40 Items pro Tag gefunden wurden.

**Ursache:** Die definierten RSS-Feed-Quellen wurden im Code gar nicht verwendet! Die `fetch_news()` Methode nutzte nur Hacker News, GitHub und Reddit, aber ignorierte alle Blog-Feeds.

### ✨ Neue Features

#### 1. Erweiterte News-Quellen (11 statt 4)

**Neue Quellen hinzugefügt:**

- ✅ **Last Week in AI** (`https://lastweekin.ai/feed`) - Wöchentliche AI News Zusammenfassung
- ✅ **Daily Dose of Data Science** (`https://blog.dailydoseofds.com/feed`) - Data Science & ML Content
- ✅ **InfoQ LLM News** (`https://www.infoq.com/llms/rss`) - Developer-fokussierte LLM News
- ✅ **The New Stack** (`https://thenewstack.io/blog/feed/`) - Developer Tools & Infrastructure
- ✅ **TechCrunch AI** (`https://techcrunch.com/category/artificial-intelligence/feed/`) - Tech Industry News
- ✅ **VentureBeat AI** (`https://venturebeat.com/category/ai/feed/`) - AI Business News
- ✅ **Google Developers Blog** (`https://developers.googleblog.com/feeds/posts/default`) - Google Developer Updates

**Korrigierte Quellen:**

- 🔧 Anthropic Blog RSS-Feed korrigiert
- 🔧 Hacker News Query erweitert: `AI OR LLM OR Claude OR GPT OR Cursor OR Windsurf`
- 🔧 GitHub Trending Query erweitert: `+antigravity`

#### 2. RSS-Feeds tatsächlich implementiert

Die `fetch_news()` Methode wurde komplett umgeschrieben:

- Iteriert jetzt durch ALLE definierten RSS-Quellen
- Verbesserte Fehlerbehandlung pro Quelle
- Detailliertes Logging welche Quellen funktionieren
- Fallback für fehlende Publikationsdaten

#### 3. Duplikats-Erkennung implementiert

**Zwei-Ebenen Duplikats-Check:**

- ✅ **Innerhalb eines Runs:** URLs werden getrackt um Duplikate zu vermeiden
- ✅ **Mit vorherigen Reports:** `load_previous_news_urls()` liest die letzten 7 Tage Reports und filtert bereits gesehene URLs

**Vorteile:**

- Keine doppelten News in einem Report
- Keine Wiederholung von News aus den letzten 7 Tagen
- Bessere Signal-to-Noise Ratio

#### 4. Prompt-Template Updates

**Google Antigravity Integration:**

```text
- Google Antigravity: Gemini 3-basierte agentic IDE (NEU: Nov 2025 Launch!)
```

**Windsurf/OpenAI Acquisition:**

```text
- Windsurf: Agentic IDE (übernommen von OpenAI in 2025, nutzt GPT-5.1)
```

**Cursor & Claude Code Updates:**

```text
- Claude Code: Terminal-basiertes AI-Coding mit Claude (Major Player 2025)
- Cursor: AI-first Code-Editor (Market Leader mit GPT-4/Claude)
```

**Neue Relevanz-Kriterien:**

- Major Releases (z.B. Antigravity Launch) → SOFORT RELEVANT
- Acquisitions & Partnerships (z.B. OpenAI/Windsurf) → SEHR RELEVANT
- CLI-Tool Updates von Antigravity hinzugefügt

**Neue Kategorie: Data Science Tools:**

```text
5. DATA SCIENCE & ML TOOLS:
   - Praktische DS/ML Libraries und Tools → RELEVANT
   - Jupyter/Notebook-Integration mit AI → RELEVANT
   - Data Analysis & Visualization mit AI → INTERESSANT
```

### 🔧 Code-Verbesserungen

#### `fetch_news()` Methode

```python
# NEU: Alle RSS-Feeds werden tatsächlich genutzt
for source_name, feed_url in self.sources.items():
    feed = feedparser.parse(feed_url)
    # ... processing
```

**Features:**

- Flexibles Datums-Parsing (published_parsed, updated_parsed, Fallback)
- HTML-Tag-Cleaning aus Summaries
- URL-Duplikats-Check pro Source
- Detailliertes Error-Logging

#### `load_previous_news_urls()` Methode

```python
def load_previous_news_urls(self, days_back: int = 7) -> set:
    """Lädt URLs aus vergangenen Reports um Duplikate zu vermeiden"""
    # Liest letzte 7 Reports
    # Extrahiert URLs via Regex
    # Returned Set von gesehenen URLs
```

### 📊 Erwartete Verbesserungen

**Vorher:**

- 0-5 News Items pro Tag
- Nur 3 aktive Quellen (HN, GitHub, Reddit)
- Viele Duplikate möglich

**Nachher:**

- 50-100+ News Items pro Tag (je nach Filter)
- 14 aktive Quellen (11 RSS + GitHub + Reddit)
- Keine Duplikate innerhalb 7 Tagen
- Bessere Coverage von:
  - LLM Releases (OpenAI, Anthropic, Google)
  - CLI-Tool Updates (Cursor, Windsurf, Antigravity)
  - Data Science News (Daily Dose of DS)
  - Developer News (InfoQ, The New Stack)
  - Industry News (TechCrunch, VentureBeat)

### 🚀 Nächste Schritte

**Sofort:**

1. Dependencies installieren: `pip install -r requirements.txt`
2. Test-Run: `python ai_news_curator.py`
3. Überprüfen dass News gefunden werden

**Optional:**

4. Weitere Quellen hinzufügen in `self.sources` Dictionary
5. `hours_back` Parameter anpassen (Standard: 24h)
6. `days_back` für Duplikats-Check anpassen (Standard: 7 Tage)

### 📚 Dokumentation Updates

**CLAUDE.md:**

- Erweiterter Tech-Stack dokumentiert
- Neue Relevanz-Kriterien beschrieben
- Prompt-Anpassungen erklärt

### ⚠️ Breaking Changes

Keine Breaking Changes. Alle Aenderungen sind rückwärtskompatibel.

### 🐛 Known Issues

- `sgmllib3k` Installation kann in manchen Python 3.11+ Umgebungen Probleme machen
  - **Lösung:** Neueste feedparser Version nutzen oder virtual environment

---

**Contributors:** Claude Code (AI Assistant)
**Date:** 2025-12-01
**Version:** 2.1
