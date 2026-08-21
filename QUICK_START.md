# ⚡ Quick Setup Guide - AI News Curator

## 🚀 In 5 Minuten zum ersten Report

### Schritt 1: Projekt Setup (1 Min)

```bash
# Dateien in dein Projekt-Verzeichnis laden
cd ~/projects
mkdir ai-news-curator
cd ai-news-curator

# Alle heruntergeladenen Dateien hierhin kopieren
```

### Schritt 2: Python Environment (2 Min)

```bash
# Virtuelles Environment erstellen
python3 -m venv venv

# Aktivieren
source venv/bin/activate  # Mac/Linux
# oder
venv\Scripts\activate     # Windows

# Dependencies installieren
pip install -r requirements.txt
```

### Schritt 3: Gateway-Zugang (1 Min)

Die App nutzt den **TF LLM-Gateway** (LiteLLM) statt eines direkten Provider-Keys.

```bash
# Gateway-Tunnel öffnen (privat im Fly-Netz)
fly proxy 4000:4000 -a tf-llm-gateway &

# Virtual Key + URL setzen (oder in .env eintragen, siehe .env.example)
export GATEWAY_KEY='sk-...'              # Virtual Key des Gateways
export GATEWAY_URL='http://localhost:4000'
```

> Virtual Key erzeugen: im `llm-gateway`-Repo `scripts/provision_keys.sh`
> mit `KEY_ALIAS=news-curator KEY_MODELS='["news-curator/classify"]'`.

### Schritt 4: Erster Test (1 Min)

```bash
# Test ob News-Quellen funktionieren (ohne API Key)
python test_sources.py

# Ersten echten Report generieren
python ai_news_curator.py
```

**Output:** `ai_news_digest_YYYYMMDD.md` 🎉

---

## 🔧 Anpassungen für deine Bedürfnisse

### A) Config anpassen

Editiere `config.yaml`:

```yaml
teaching_context:
  topics:
    - "Deine Schulungsthemen"
  tech_stack:
    - "Deine Tools"
```

### B) Mehr/weniger Stunden zurück

In `ai_news_curator.py`, Zeile am Ende:

```python
curator.run(hours_back=48)  # Statt 24
```

### C) Andere News-Quellen

In `ai_news_curator.py`, Methode `fetch_news()`:

```python
# Füge deinen RSS Feed hinzu
custom_feed = feedparser.parse('https://dein-blog.com/rss')
```

---

## ☁️ GitHub Actions Setup (Optional)

Für tägliche automatische Reports:

### 1. GitHub Repo erstellen

```bash
git init
git add .
git commit -m "Initial commit: AI News Curator"
git remote add origin https://github.com/DEIN-USERNAME/ai-news-curator.git
git push -u origin main
```

### 2. Secrets hinzufügen

Gehe zu: **Settings** → **Secrets and variables** → **Actions** → **New repository secret**
und lege zwei Secrets an:

- `NEWS_CURATOR_GATEWAY_KEY` — Virtual Key des Gateways (`sk-...`)
- `FLY_API_TOKEN` — Fly-Token mit Zugriff auf `tf-llm-gateway` (für den `fly proxy`-Tunnel)

### 3. Workflow aktivieren

- Gehe zu: **Actions** Tab
- Workflow "Daily AI News Digest" sollte sichtbar sein
- Teste manuell: **Run workflow**

**Das war's!** ✅ Läuft jetzt täglich automatisch.

---

## 🎓 Für den Unterricht nutzen

### Wöchentliche "What's New" Session

```bash
# Am Montag vor der Vorlesung
python ai_news_curator.py

# Report öffnen
open ai_news_digest_*.md
```

Zeige den Studierenden:
- **Score 5 Items:** "Das müsst ihr kennen!"
- **Score 4 Items:** "Beobachten für nächstes Projekt"
- **Score 3 Items:** "FYI, nicht kritisch"

### Als Homework/Research

Gib Studierenden den Report und bitte sie:
- Einen High-Priority Artikel deep-dive präsentieren
- Vergleich: Antigravity vs Cursor vs Windsurf
- Praktische Demo eines neuen Tools

---

## 🐛 Probleme?

### "Module not found"
```bash
pip install -r requirements.txt
```

### "GATEWAY_KEY not set" / "Connection refused"
```bash
echo $GATEWAY_KEY                                  # Sollte den Virtual Key zeigen
export GATEWAY_KEY='sk-...'
fly proxy 4000:4000 -a tf-llm-gateway &            # Tunnel zum privaten Gateway
curl -sf http://localhost:4000/health/liveliness   # sollte 200 liefern
```

### Keine News gefunden
- Internet-Verbindung checken
- Manche Feeds können temporär down sein
- Mit `python test_sources.py` einzelne Quellen testen

### GitHub Action läuft nicht
- Workflow-Datei in `.github/workflows/` ?
- Secrets korrekt als `NEWS_CURATOR_GATEWAY_KEY` und `FLY_API_TOKEN` benannt?
- In Settings → Actions → "Allow all actions" aktiviert?

---

## 💰 Kosten

**Lokal (täglich):**
- Claude API: ~$0.10-0.30/Tag
- **Pro Monat:** ~$3-9

**GitHub Actions:**
- Public Repos: **Kostenlos**
- Private Repos: 2000 min/Monat gratis (reicht locker)

---

## 🎯 Next Steps

1. **Jetzt:** Ersten Report generieren
2. **Heute:** Config an deine Bedürfnisse anpassen
3. **Diese Woche:** GitHub Actions Setup für Automatisierung
4. **Nächste Woche:** Erste "What's New" Session mit Studierenden

---

**Viel Erfolg!** 🚀

Bei Fragen: Issues auf GitHub oder direktes Feedback
