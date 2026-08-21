# GitHub Actions Setup - Schritt für Schritt

## 📁 Workflow-Datei richtig platzieren

GitHub Actions erwartet Workflows in einem **spezifischen Verzeichnis**:

```
dein-projekt/
├── .github/
│   └── workflows/
│       └── daily_news.yml          <- Hier muss die Datei hin!
├── ai_news_curator.py
├── requirements.txt
└── ...
```

## Korrekte Installation

Der Workflow (`.github/workflows/daily_news.yml`) ist bereits im Repo eingecheckt — kein
manuelles Platzieren nötig. Er läuft gegen den zentralen **TF LLM-Gateway** (LiteLLM,
`talent-factory/llm-gateway`), nicht mehr direkt gegen die Anthropic-API. Provider-Keys
liegen ausschliesslich am Gateway; dieses Repo braucht nur einen projekt-scoped Virtual Key.

## Secrets als GitHub Actions Secrets hinzufügen

**Wichtig:** Der Workflow braucht zwei Secrets, um durch den privaten Gateway-Tunnel zu kommen:

| Secret | Zweck |
|---|---|
| `NEWS_CURATOR_GATEWAY_KEY` | Virtual Key am Gateway, least privilege auf `news-curator/classify` |
| `FLY_API_TOKEN` | App-scoped Fly-Token, öffnet den `fly proxy`-Tunnel zum privaten Gateway (der GH-Runner ist öffentlich, das Gateway hat keine öffentliche IP) |

### Schritt für Schritt

1. **Virtual Key am Gateway provisionieren** (im `llm-gateway`-Repo, mit dem Prod-Master-Key):
   ```bash
   LITELLM_MASTER_KEY=<prod-master-key> \
   KEY_ALIAS=news-curator \
   KEY_MODELS='["news-curator/classify"]' \
   KEY_MAX_BUDGET=10 \
   just provision
   ```
   → liefert `"key": "sk-..."`. Achtung: LiteLLM speichert nur den Hash — der Klartext-Key
   ist danach nicht mehr abrufbar. Alias muss eindeutig sein; existiert er schon, vorher via
   `POST /key/delete` mit `{"key_aliases": ["news-curator"]}` löschen.

2. **Fly-Token erzeugen** (app-scoped auf `tf-llm-gateway`, least privilege):
   ```bash
   fly tokens create deploy -a tf-llm-gateway -n "ai-news-curator-ci" -x 8760h
   ```

3. Gehe zu deinem GitHub Repository
   - URL: `https://github.com/talent-factory/ai-news-curator`

4. Settings Tab öffnen
   - Oben rechts auf "Settings" klicken

5. Secrets and variables
   - Linke Sidebar: "Secrets and variables" → "Actions"

6. New repository secret
   - Button: "New repository secret" klicken, je einmal für:
     - Name: `NEWS_CURATOR_GATEWAY_KEY`, Secret: der Virtual Key aus Schritt 1
     - Name: `FLY_API_TOKEN`, Secret: der Token aus Schritt 2
   - "Add secret" klicken

Oder per CLI (Wert wird interaktiv abgefragt, landet nie im Terminal-Log):
```bash
gh secret set NEWS_CURATOR_GATEWAY_KEY --repo talent-factory/ai-news-curator
gh secret set FLY_API_TOKEN --repo talent-factory/ai-news-curator
```

Das war's! Der Workflow kann jetzt durch den Tunnel auf den Gateway-Alias zugreifen.

> Historie: Bis zur Gateway-Migration lief dieses Repo mit einem eigenen `ANTHROPIC_API_KEY`-
> Secret direkt gegen die Anthropic-API. Das Secret ist inzwischen ungenutzt und sollte
> entfernt werden (Settings → Secrets and variables → Actions → `ANTHROPIC_API_KEY` → Remove).

## Testen ob es funktioniert

### Manueller Test

1. Gehe zu: Actions Tab in deinem Repository
2. Klicke auf: "Weekly AI News Digest"
3. Rechts oben: "Run workflow" → "Run workflow"
4. Warte ca. 2-3 Minuten
5. Überprüfe ob ein neues GitHub Issue mit dem Report erstellt wurde

### Automatischer Test

Läuft **wöchentlich Montag 05:00 UTC** (06:00 CET / 07:00 CEST je nach Sommerzeit) — siehe
`cron: '0 5 * * 1'` in `.github/workflows/daily_news.yml`.

## Troubleshooting

### Workflow erscheint nicht in Actions Tab

**Problem:** `.github/workflows/` Verzeichnis fehlt oder falsch benannt

**Lösung:**

```bash
# Verzeichnis muss GENAU so heissen (.github nicht github!)
ls -la .github/workflows/
# Sollte deine .yml Datei zeigen

# Wenn nicht:
mkdir -p .github/workflows
mv daily_news.yml .github/workflows/
```

### "GATEWAY_KEY environment variable nicht gesetzt!"

**Problem:** Secret `NEWS_CURATOR_GATEWAY_KEY` fehlt oder ist leer

**Lösung:**

1. Settings → Secrets and variables → Actions
2. Überprüfe: Secret heisst **exakt** `NEWS_CURATOR_GATEWAY_KEY`
3. Falls nicht/falsch: neuen Virtual Key am Gateway provisionieren (siehe oben) und Secret neu setzen

### "✗ Gateway-Tunnel kam nicht hoch" (Step "Open tunnel to private LLM-Gateway")

**Problem:** `FLY_API_TOKEN` fehlt, ist abgelaufen, oder hat nicht genug Rechte für `tf-llm-gateway`

**Lösung:**

1. Neuen app-scoped Token erzeugen: `fly tokens create deploy -a tf-llm-gateway -n "ai-news-curator-ci" -x 8760h`
2. Secret `FLY_API_TOKEN` im Repo neu setzen
3. Prüfen, dass `tf-llm-gateway` selbst erreichbar ist (`just health` im `llm-gateway`-Repo)

### "Permission denied" beim Erstellen des Issues

**Problem:** Workflow hat keine Write-Rechte

**Lösung:**

1. Settings → Actions → General
2. Scroll zu "Workflow permissions"
3. Wähle: "Read and write permissions"
4. "Allow GitHub Actions to create and approve pull requests"
5. Save

### Workflow läuft, aber kein Issue/Report

**Problem:** Script schlägt fehl (Tunnel steht, aber der eigentliche Curator-Lauf scheitert)

**Lösung:**

1. Actions Tab → Letzte Workflow-Run anklicken
2. "Run AI News Curator" Step anklicken
3. Logs lesen — Fehlermeldung nennt explizit die Ursache (Tunnel/`GATEWAY_URL`, ungültiger `GATEWAY_KEY`, unbekannter Modell-Alias, o.ä.)
4. Häufig: `NEWS_CURATOR_GATEWAY_KEY` falsch/gelöscht, oder Alias `news-curator/classify` existiert nicht (mehr) am Gateway (`config.yaml` im `llm-gateway`-Repo prüfen)

## Was passiert beim automatischen Run?

```
Montag 05:00 UTC (06:00 CET / 07:00 CEST):
  └─ Workflow startet
     ├─ Repository auschecken
     ├─ Python installieren
     ├─ Dependencies installieren
     ├─ flyctl installieren + Tunnel zum privaten LLM-Gateway öffnen
     │  └─ fly proxy 4000:4000 -a tf-llm-gateway (via FLY_API_TOKEN)
     ├─ ai_news_curator.py ausführen
     │  ├─ News von HN, Reddit, GitHub sammeln
     │  ├─ TF LLM-Gateway (Alias news-curator/classify) für Relevanz-Analyse
     │  └─ Report generieren
     └─ GitHub Issue mit dem Report erstellen (+ sperren gegen Spam-Kommentare)
```

**Ergebnis:** Neues GitHub Issue mit dem News-Digest in deinem Repo!

## Pro-Tipps

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

Bei Fragen: Schau in die [GitHub Actions Docs](https://docs.github.com/en/actions) oder öffne ein Issue!
