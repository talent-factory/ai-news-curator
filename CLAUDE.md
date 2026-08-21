# 🤖 Claude API Integration

## Überblick

Der AI News Curator nutzt **Claude** als intelligenten Filter-Agenten. Jede gesammelte News wird einzeln analysiert und bewertet - nicht nur nach Keywords, sondern mit echtem Kontext-Verständnis.

> **NEU ab Version 3.0 (Gateway-Migration):** Die Calls laufen nicht mehr direkt gegen
> die Anthropic-API, sondern über den **TF LLM-Gateway** (LiteLLM, OpenAI-kompatibel) unter
> dem logischen Alias `news-curator/classify` (dahinter weiterhin Claude Sonnet, Fallback
> Opus). Modellwechsel = Config-Edit am Gateway, nicht in dieser App. Zugang: siehe
> [Gateway-Zugang](#-gateway-zugang-statt-provider-api-key).

### Warum Claude?

- ✅ **Kontext-Verständnis:** Claude versteht den Unterschied zwischen "neues Tool" und "Marketing-Ankündigung"
- ✅ **Reasoning:** Claude erklärt WARUM etwas relevant ist, nicht nur dass es relevant ist
- ✅ **Konsistenz:** Bewertet nach deinen spezifischen Kriterien, nicht nach allgemeiner "Wichtigkeit"
- ✅ **Skalierbar:** Claude Sonnet 4 ist schnell und kosteneffizient für diese Aufgabe

## 🎯 Der Analyse-Prompt

### Neue Architektur: Externe Prompt-Datei

**NEU ab Version 2.0:** Der Prompt ist jetzt in `prompt_template.txt` ausgelagert!

**Vorteile:**
- ✅ Einfacher zu warten und zu iterieren
- ✅ Versionskontrolle für Prompt-Änderungen
- ✅ Keine Code-Änderungen für Prompt-Anpassungen
- ✅ Teilen und Wiederverwenden von Prompts

### Aktuelle Template-Struktur

Die Datei `prompt_template.txt` enthält den vollständigen Analyse-Prompt mit:

#### 1. Kontext-Sektion
```yaml
KONTEXT:
- Schulungen: "Software-Entwicklung mit KI" und "Integration von KI in Produkte"
- Zielgruppe: IT-Studierende und Young Professionals
- Fokus: Praktische Tools und Anwendungen, nicht nur Theorie
```

**Neu:** Der Kontext ist präziser auf die tatsächliche Zielgruppe fokussiert.

#### 2. Erweiterter Tech-Stack

**Large Language Models (LLMs):**
- Claude (Anthropic): Sonnet, Opus, Haiku
- GPT (OpenAI): GPT-4, o1, o3
- Gemini (Google): 2.0 Flash, Pro
- Weitere: Deepseek, Llama, Mistral

**CLI-basierte Entwicklungsumgebungen:**
- Claude Code: Terminal-basiertes AI-Coding
- Cursor: AI-first Code-Editor
- Windsurf: Agentic IDE von Codeium
- Augment Code (Auggie): Terminal AI-Assistant
- Google Antigravity: Gemini-basierte agentic IDE
- Bolt.new: Instant fullstack apps
- v0.dev: AI-gestützte React-Component-Generierung

**AI-Frameworks & Libraries:**
- LangChain, LlamaIndex: LLM-Application Frameworks
- CrewAI, AutoGen: Multi-Agent Frameworks
- Vercel AI SDK: React/Next.js AI Integration

**Development Tools:**
- VS Code mit AI-Extensions
- GitHub Copilot, Cody
- Promptfoo, LangSmith, Braintrust

#### 3. Neue Relevanz-Kriterien

**LLM-RELEASES & UPDATES:**
- Neue Modelle → HOCH RELEVANT
- Neue Capabilities → SEHR RELEVANT
- Breaking Changes → SOFORT RELEVANT
- Preisänderungen → RELEVANT

**CLI/TERMINAL-BASIERTE DEV-TOOLS:**
- Neue CLI-Tools → HOCH RELEVANT
- Updates von Cursor/Windsurf/Claude Code → SEHR RELEVANT
- "Agentic" Development → HOCH RELEVANT

#### 4. Erweiterte Kategorien

Neu sind **6 Kategorien** statt 4:

- `llm_release` 🤖 = Neue oder aktualisierte LLM-Modelle
- `cli_tools` ⌨️ = Terminal/CLI-basierte Entwicklungsumgebungen
- `teaching` 🎓 = Direkt für Unterricht nutzbar
- `tools` 🛠️ = Development Tools, Extensions
- `research` 🔬 = Interessante Entwicklung
- `skip` = Nicht relevant

#### 5. Verbessertes Scoring mit Beispielen

```text
5 = Muss sofort in Schulung eingebaut werden
    Beispiele: Breaking Change in Haupt-Tool, neues Claude/GPT Release,
               Cursor/Windsurf Major Update, neue agentic IDE

4 = Sehr relevant, baldige Integration sinnvoll
    Beispiele: Neue LLM-Features, neue CLI-Tools, Framework-Updates

3 = Interessant, beobachten
    Beispiele: Experimentelle Tools, Research mit praktischem Potential
```

## 🔧 Prompt Anpassen

### Methode 1: Direkt in prompt_template.txt editieren

```bash
# Öffne die Datei
nano prompt_template.txt

# Oder mit deinem Editor
code prompt_template.txt
```

**Beispiel-Anpassungen:**

**Fokus auf Data Science:**

```yaml
KONTEXT:
- Schulungen: "Data Science mit AI-Tools"
- Zielgruppe: Data Scientists, ML Engineers
- Tech-Stack: Python, Jupyter, pandas, scikit-learn, TensorFlow, PyTorch
```

**Fokus auf Enterprise:**

```yaml
KONTEXT:
- Schulungen: "Enterprise AI Integration"
- Zielgruppe: Senior Developers, Architects
- Tech-Stack: Java, Spring Boot, Azure OpenAI, AWS Bedrock
```

### Methode 2: Alternative Prompt-Datei verwenden

```python
# In ai_news_curator.py oder beim Initialisieren
curator = AINewsCurator(
    gateway_key,                       # Virtual Key des Gateways
    gateway_url="http://localhost:4000",
    model="news-curator/classify",
    prompt_template_path="custom_prompt.txt",
)
```

### Methode 3: Prompt-Versionierung

```bash
# Git-basierte Versionierung
cp prompt_template.txt prompts/v2.0_llm_focus.txt
git add prompts/
git commit -m "Add LLM-focused prompt variant"
```

## 📊 Output-Format mit neuen Kategorien

Reports zeigen jetzt Kategorien mit Emojis:

```markdown
## 🔥 Sofort relevant (Score 4-5)

### 🤖 Claude 3.7 Opus Released
**Quelle:** Hacker News | **Score:** 5/5 | **Kategorie:** llm_release

💡 **Warum relevant:** Major LLM Release...

### ⌨️ Cursor 0.42: Multi-Agent Editing
**Quelle:** GitHub | **Score:** 5/5 | **Kategorie:** cli_tools

💡 **Warum relevant:** Wichtiges Update für Haupt-IDE...

---

**Nach Kategorien:**
- 🤖 llm_release: 3
- ⌨️ cli_tools: 5
- 🎓 teaching: 2
- 🛠️ tools: 4
```

## 💰 Kosten & Rate Limits

> **Gateway-Hinweis:** Kosten werden jetzt am Gateway pro Projekt getrackt
> (`metadata.project=news-curator`) und über `max_budget`/`budget_duration` des Virtual
> Keys begrenzt. Die folgenden Modell-Preise gelten weiterhin, da hinter
> `news-curator/classify` Claude Sonnet steht.

### Claude Sonnet 4 Pricing (Stand Januar 2025)

```
Input:  $3 per Million Tokens
Output: $15 per Million Tokens
```

### Typischer Daily Digest (20 News-Items)

**Mit neuem, längerem Prompt:**
```
Pro News-Item:
- Input:  ~800 tokens (Erweiterter Prompt + News)
- Output: ~120 tokens (JSON Response)

Tägliche Kosten:
- Input:  20 × 800 = 16,000 tokens = $0.048
- Output: 20 × 120 = 2,400 tokens  = $0.036
- TOTAL: ~$0.08 pro Tag
```

**Monatlich:** ~$2.40 (bei täglichem Run)
**Jährlich:** ~$29

**Hinweis:** Leicht höhere Kosten durch erweiterten Prompt, aber immer noch sehr günstig!

### Kosten optimieren

**Option 1: Prompt Caching (Beta)**
```python
# Anthropic Prompt Caching
# Spart 90% Input-Kosten bei wiederholtem Kontext
# TODO: Implementierung geplant für v2.1
```

**Option 2: Batch-Processing**
```python
# TODO: 5 Items pro Request statt 1
# Reduziert API-Calls um 80%
```

## 🔐 Gateway-Zugang (statt Provider-API-Key)

Seit der Gateway-Migration spricht die App **nicht mehr direkt** Anthropic an, sondern
den **TF LLM-Gateway** (LiteLLM, OpenAI-kompatibel). Provider-Keys (`ANTHROPIC_API_KEY`
etc.) liegen ausschliesslich als Fly-Secret am Gateway — ein zurückgezogenes Modell ist
damit ein Config-Edit am Gateway statt eines Ausfalls hier.

### Virtual Key erhalten

Im `llm-gateway`-Repo einen projekt-scoped Virtual Key provisionieren:

```bash
LITELLM_MASTER_KEY=sk-master-… \
KEY_ALIAS=news-curator \
KEY_MODELS='["news-curator/classify"]' \
scripts/provision_keys.sh        # gibt einen sk-… zurück
```

### Lokal verwenden

```bash
# Tunnel zum privaten Gateway (Fly 6PN)
fly proxy 4000:4000 -a tf-llm-gateway &

# Environment Variablen (oder .env, siehe .env.example)
export GATEWAY_KEY='sk-...'                 # Virtual Key
export GATEWAY_URL='http://localhost:4000'  # Default
# export GATEWAY_MODEL='news-curator/classify'  # optionaler Alias-Override
```

**Alternative: .env File** (siehe `.env.example`)
```bash
# .env
GATEWAY_KEY=sk-...
GATEWAY_URL=http://localhost:4000
```

## 🛠️ Troubleshooting

### Error: "Prompt template not found"

**Ursache:** `prompt_template.txt` fehlt im Working Directory

**Lösung:**
```bash
# Check if file exists
ls -la prompt_template.txt

# If missing, restore from git
git checkout prompt_template.txt
```

**Fallback:** Script verwendet automatisch einen eingebauten Fallback-Prompt.

### Error: "KeyError: 'title' or 'source' or 'summary'"

**Ursache:** Prompt-Template verwendet Platzhalter, die nicht existieren

**Lösung:**
Stelle sicher, dass `prompt_template.txt` diese Platzhalter enthält:
- `{title}` - News-Titel
- `{source}` - News-Quelle
- `{summary}` - News-Zusammenfassung

### Prompt-Änderungen werden nicht übernommen

**Ursache:** Du musst das Script neu starten nach Prompt-Änderungen

**Lösung:**
```bash
# Stoppe aktuellen Run
Ctrl+C

# Starte neu
python ai_news_curator.py
```

### Claude ignoriert neue Kategorien

**Problem:** Claude verwendet alte Kategorien (teaching, tools, research, skip)

**Lösung:**

1. Check `prompt_template.txt` enthält neue Kategorien
2. Füge Beispiele für neue Kategorien hinzu
3. Mache die Definitionen expliziter

**Beispiel-Verbesserung:**

```yaml
KATEGORIE (WICHTIG: Nutze die NEUEN Kategorien!):
- "llm_release" = LLM-Modell Updates (Claude, GPT, Gemini, etc.)
- "cli_tools" = Terminal/CLI Tools (Cursor, Windsurf, Claude Code, etc.)
...
```

## 📚 Prompt Engineering Best Practices

### 1. Iteratives Verbesserung

```bash
# Workflow für Prompt-Optimierung
1. Baseline: Ersten Report generieren
2. Analyse: Welche News wurden falsch bewertet?
3. Update: prompt_template.txt anpassen
4. Test: Neuen Report generieren
5. Repeat: Bis Qualität passt
```

### 2. Few-Shot Examples hinzufügen

Wenn Claude Kategorien falsch zuordnet:

```text
BEISPIELE:
- "Cursor 0.42 Released" → Score 5, Kategorie: cli_tools
  Reasoning: "Wichtiges Update für Haupt-IDE der Studierenden"

- "Claude 3.7 Opus API" → Score 5, Kategorie: llm_release
  Reasoning: "Major LLM Release, direkt relevant für AI-Entwicklung"

- "Research Paper: Transformers" → Score 2, Kategorie: skip
  Reasoning: "Zu theoretisch, nicht praktisch anwendbar"
```

### 3. Klare Prioritäten setzen

```text
WICHTIG (Sortierung nach Relevanz):
1. CLI-basierte Dev-Tools (Cursor, Windsurf, Claude Code) → HÖCHSTE PRIORITÄT
2. LLM-Releases (Claude, GPT, Gemini) → SEHR HOCH
3. Frameworks für AI-Development → HOCH
4. Theoretische Papers → NIEDRIG
```

### 4. Kontext regelmässig updaten

```bash
# Jeden Monat Tech-Stack aktualisieren
# Neue Tools hinzufügen
# Veraltete Tools entfernen
```

## 🔄 Alternative LLM APIs

Falls du Claude nicht nutzen willst/kannst:

### OpenAI GPT-4
```python
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
response = client.chat.completions.create(
    model="gpt-4-turbo",
    messages=[{"role": "user", "content": prompt}]
)
```

**Kosten:** ~$0.01/1K Input Tokens (3× teurer als Claude)

### Google Gemini
```python
import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel('gemini-1.5-flash')
response = model.generate_content(prompt)
```

**Kosten:** ~$0.075/1M Tokens (günstiger als Claude)

### Ollama (Lokal, kostenlos)
```python
import requests

response = requests.post('http://localhost:11434/api/generate',
    json={'model': 'llama2', 'prompt': prompt}
)
```

**Pros:** Kostenlos, Privacy
**Cons:** Schlechtere Analyse-Qualität

## 📝 Dokumentations-Standards

### Schweizer Hochdeutsch

**Schreibweise in allen Markdown-Dateien:**
- ✅ **RICHTIG:** ß → ss (z.B. "regelmässig", "gross", "Grösse")
- ✅ **RICHTIG:** Umlaute ä, ö, ü bleiben erhalten
- ❌ **FALSCH:** ä → ae, ö → oe, ü → ue (verwende NICHT diese Konvertierung!)

**Beispiele:**
- ✅ "für" nicht ❌ "fuer"
- ✅ "Änderungen" nicht ❌ "Aenderungen"
- ✅ "verfügbar" nicht ❌ "verfuegbar"
- ✅ "regelmässig" nicht ❌ "regelmäßig"

### Markdown-Formatierung

**Code-Blocks:**
- Immer mit Language-Identifiers: `bash`, `python`, `yaml`, `text`
- Beispiel: ` ```python ` nicht nur ` ``` `

**Heading-Hierarchie:**
- Korrekte Struktur: H1 → H2 → H3 (keine Sprünge)
- Ein H1 pro Datei (Titel)

**Listen-Formatierung:**
- Unordered Lists: `-` (konsistent)
- Ordered Lists: `1.`, `2.`, `3.`
- Leerzeile vor Listen für bessere Lesbarkeit

**Spacing:**
- Eine Leerzeile zwischen Abschnitten
- Keine doppelten Leerzeilen
- Leerzeile vor/nach Code-Blocks

**Links:**
- Markdown-Format: `[Text](URL)`
- Interne Links: `[README](README.md)`

## 🎓 Weiterführende Links

- **Claude API Docs:** https://docs.anthropic.com/
- **Prompt Engineering Guide:** https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering
- **Prompt Library:** https://docs.anthropic.com/en/prompt-library
- **Rate Limits:** https://docs.anthropic.com/en/api/rate-limits
- **Pricing:** https://www.anthropic.com/pricing

---

**Nächste Schritte:**
1. Teste den neuen Prompt: `python ai_news_curator.py`
2. Analysiere erste Reports
3. Passe `prompt_template.txt` an deine Bedürfnisse an
4. Siehe [README.md](README.md) für allgemeine Infos
