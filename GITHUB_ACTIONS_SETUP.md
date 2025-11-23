# GitHub Actions Setup - Schritt für Schritt

## 📁 Workflow-Datei richtig platzieren

GitHub Actions erwartet Workflows in einem **spezifischen Verzeichnis**:

```
dein-projekt/
├── .github/
│   └── workflows/
│       └── daily_news.yml          ← Hier muss die Datei hin!
├── ai_news_curator.py
├── requirements.txt
└── ...
```

### ✅ Korrekte Installation

```bash
# 1. Verzeichnis-Struktur erstellen
mkdir -p .github/workflows

# 2. Workflow-Datei platzieren
cp daily_news_simple.yml .github/workflows/daily_news.yml

# Alternative: Fortgeschrittene Version mit Issue-Erstellung
# cp daily_news.yml .github/workflows/daily_news.yml

# 3. Zu Git hinzufügen
git add .github/workflows/daily_news.yml
git commit -m "Add daily news digest workflow"
git push
```

## 🔧 Welche Version soll ich nutzen?

### Option 1: **daily_news_simple.yml** (Empfohlen für Start)
✅ Einfacher  
✅ Erstellt nur Reports  
✅ Weniger Berechtigungen nötig  
❌ Keine automatischen GitHub Issues  

**Nutze diese Version wenn:**
- Du gerade startest
- Du Reports nur per Commit haben willst
- Du Probleme mit Berechtigungen vermeiden willst

### Option 2: **daily_news.yml** (Fortgeschritten)
✅ Erstellt Reports  
✅ Erstellt GitHub Issues bei High-Priority News  
✅ Automatische Benachrichtigungen  
❌ Benötigt zusätzliche Berechtigungen  

**Nutze diese Version wenn:**
- Du automatische Notifications willst
- Du GitHub Issues als To-Do nutzt
- Du den Workflow gut verstehst

## 🔑 API Key als Secret hinzufügen

**Wichtig:** GitHub Actions braucht deinen Anthropic API Key!

### Schritt für Schritt:

1. **Gehe zu deinem GitHub Repository**
   - URL: `https://github.com/talent-factory/ai-news-curator`

2. **Settings Tab öffnen**
   - Oben rechts auf "Settings" klicken

3. **Secrets and variables**
   - Linke Sidebar: "Secrets and variables" → "Actions"

4. **New repository secret**
   - Button: "New repository secret" klicken
   - **Name:** `ANTHROPIC_API_KEY`
   - **Secret:** Dein Claude API Key (z.B. `sk-ant-api03-...`)
   - "Add secret" klicken

✅ **Das war's!** Der Workflow kann jetzt auf den Key zugreifen.

## ✅ Testen ob es funktioniert

### Manueller Test

1. Gehe zu: **Actions Tab** in deinem Repository
2. Klicke auf: **"Daily AI News Digest"** (oder "Daily AI News Digest (Simple)")
3. Rechts oben: **"Run workflow"** → "Run workflow"
4. Warte ~2-3 Minuten
5. Check ob neuer Commit mit Report da ist

### Automatischer Test

Warte bis 08:00 Uhr morgen (CET) - dann sollte automatisch ein neuer Report committed werden!

## 🐛 Troubleshooting

### Workflow erscheint nicht in Actions Tab

**Problem:** `.github/workflows/` Verzeichnis fehlt oder falsch benannt

**Lösung:**
```bash
# Verzeichnis muss GENAU so heißen (.github nicht github!)
ls -la .github/workflows/
# Sollte deine .yml Datei zeigen

# Wenn nicht:
mkdir -p .github/workflows
mv daily_news.yml .github/workflows/
```

### "Error: ANTHROPIC_API_KEY not set"

**Problem:** Secret nicht korrekt hinzugefügt

**Lösung:**
1. Settings → Secrets and variables → Actions
2. Überprüfe: Secret heißt **exakt** `ANTHROPIC_API_KEY`
3. Falls nicht: Lösche und neu erstellen

### "Permission denied" beim Push

**Problem:** Workflow hat keine Write-Rechte

**Lösung 1 (einfach):** Nutze `daily_news_simple.yml`

**Lösung 2 (fortgeschritten):**
1. Settings → Actions → General
2. Scroll zu "Workflow permissions"
3. Wähle: "Read and write permissions"
4. "Allow GitHub Actions to create and approve pull requests" ✅
5. Save

### Workflow läuft, aber keine Reports

**Problem:** Script schlägt fehl

**Lösung:**
1. Actions Tab → Letzte Workflow-Run anklicken
2. "Run AI News Curator" Step anklicken
3. Logs lesen - dort steht der Fehler
4. Häufig: API Key falsch oder Rate Limit

## 📊 Was passiert beim automatischen Run?

```
07:00 UTC (08:00 CET):
  └─ Workflow startet
     ├─ Repository auschecken
     ├─ Python installieren
     ├─ Dependencies installieren
     ├─ ai_news_curator.py ausführen
     │  ├─ News von HN, Reddit, GitHub sammeln
     │  ├─ Claude API für Relevanz-Analyse
     │  └─ Report generieren
     ├─ Report zu Git committen
     └─ [Optional] GitHub Issue erstellen
```

**Ergebnis:** Neuer Report in deinem Repo!

## 💡 Pro-Tipps

### Reports in separatem Ordner

Editiere `ai_news_curator.py`:

```python
# Statt:
output_file = f"ai_news_digest_{datetime.now().strftime('%Y%m%d')}.md"

# Nutze:
os.makedirs("reports", exist_ok=True)
output_file = f"reports/ai_news_digest_{datetime.now().strftime('%Y%m%d')}.md"
```

Dann in Workflow:
```yaml
git add reports/ai_news_digest_*.md
```

### Nur werktags laufen lassen

```yaml
on:
  schedule:
    # Montag bis Freitag um 07:00 UTC
    - cron: '0 7 * * 1-5'
```

### Mehrmals täglich

```yaml
on:
  schedule:
    # 08:00 und 17:00 CET
    - cron: '0 7 * * *'
    - cron: '0 16 * * *'
```

---

**Bei Fragen:** Schau in die [GitHub Actions Docs](https://docs.github.com/en/actions) oder öffne ein Issue!
