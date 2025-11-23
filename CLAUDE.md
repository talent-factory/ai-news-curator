# 🤖 Claude API Integration

## Überblick

Der AI News Curator nutzt **Anthropic's Claude API** als intelligenten Filter-Agenten. Jede gesammelte News wird einzeln von Claude analysiert und bewertet - nicht nur nach Keywords, sondern mit echtem Kontext-Verständnis.

### Warum Claude?

- ✅ **Kontext-Verständnis:** Claude versteht den Unterschied zwischen "neues Tool" und "Marketing-Ankündigung"
- ✅ **Reasoning:** Claude erklärt WARUM etwas relevant ist, nicht nur dass es relevant ist
- ✅ **Konsistenz:** Bewertet nach deinen spezifischen Kriterien, nicht nach allgemeiner "Wichtigkeit"
- ✅ **Skalierbar:** Claude Sonnet 4 ist schnell und kosteneffizient für diese Aufgabe

## 🎯 Der Analyse-Prompt

### Template-Struktur

```python
prompt = f"""Analysiere diese AI/Tech-News auf Relevanz für Schweizer Hochschul-Schulungen.

Kontext:
- Schulungen: "Software-Entwicklung mit KI" und "Integration von KI in Produkte"
- Zielgruppe: IT-Studierende und Young Professionals
- Tech-Stack: Python, Java, React, Windsurf, VS Code, Claude Code, Augment Code
- Fokus: Praktische Tools und Anwendungen, nicht nur Theorie

News-Item:
Titel: {item['title']}
Quelle: {item['source']}
URL: {item['url']}
Zusammenfassung: {item['summary']}

Bewerte nach folgenden Kriterien:

1. RELEVANZ-SCORE (1-5):
   5 = Muss sofort in Schulung eingebaut werden
   4 = Sehr relevant, baldige Integration sinnvoll
   3 = Interessant, beobachten
   2 = Wenig relevant
   1 = Nicht relevant

2. KATEGORIE:
   - "teaching" = Direkt für Unterricht nutzbar
   - "tools" = Tool-Update/neue Entwicklungsumgebung
   - "research" = Interessante Entwicklung, aber nicht unmittelbar praktisch
   - "skip" = Nicht relevant

3. REASONING: Kurze Begründung (1-2 Sätze)

Antworte NUR mit JSON:
{{
  "relevance_score": <1-5>,
  "category": "<teaching|tools|research|skip>",
  "reasoning": "<begründung>"
}}"""
```

### Prompt-Komponenten erklärt

#### 1. Kontext-Sektion
```yaml
Kontext:
- Schulungen: "Software-Entwicklung mit KI" und "Integration von KI in Produkte"
- Zielgruppe: IT-Studierende und Young Professionals
- Tech-Stack: Python, Java, React, Windsurf, VS Code, Claude Code, Augment Code
- Fokus: Praktische Tools und Anwendungen, nicht nur Theorie
```

**Warum wichtig?** Claude verwendet diesen Kontext, um die Relevanz zu bewerten. Ohne diesen Kontext würde Claude generisch bewerten ("ist das wichtig für irgendwen?") statt spezifisch ("ist das wichtig für MEINE Studierenden?").

**Anpassung:** Editiere `config.yaml` → `teaching_context` oder passe direkt in `ai_news_curator.py:107-113` an.

#### 2. Scoring-System (1-5)
```
5 = Muss sofort in Schulung eingebaut werden
4 = Sehr relevant, baldige Integration sinnvoll
3 = Interessant, beobachten
2 = Wenig relevant
1 = Nicht relevant
```

**Warum 1-5?** Gibt dir klare Handlungsempfehlungen:
- **5:** Action needed NOW
- **4:** Plan für nächste Session
- **3:** Auf Radar behalten
- **1-2:** Ignorieren

**Beispiele:**
- Score 5: "Windsurf 2.0 mit Breaking Changes" (Dein Haupt-Tool!)
- Score 4: "Neue Claude API Feature für Code-Gen" (Relevant für Kurs)
- Score 3: "Interessantes RAG Pattern" (Gut zu wissen)
- Score 1: "OpenAI CEO Tweet ohne Substanz" (Marketing)

#### 3. Kategorien
```
- "teaching" = Direkt für Unterricht nutzbar
- "tools" = Tool-Update/neue Entwicklungsumgebung
- "research" = Interessante Entwicklung, nicht unmittelbar praktisch
- "skip" = Nicht relevant
```

**Verwendung im Report:**
- **teaching:** "Diese API-Change zeig ich morgen in der Vorlesung"
- **tools:** "Studierende sollten das neue Feature kennen"
- **research:** "Spannend für Semesterarbeit-Themen"
- **skip:** Wird nicht im Report angezeigt

#### 4. Reasoning (1-2 Sätze)
```
"Direkter Konkurrent zu Windsurf/Cursor. Das agent-first Konzept
ist ein neuer Ansatz, den Studierende verstehen sollten."
```

**Warum wichtig?**
- Du siehst sofort WARUM Claude etwas als wichtig einstuft
- Hilft dir zu entscheiden: Stimme ich zu?
- Kann direkt in Vorlesung gezeigt werden ("Claude sagt...")

## 🔧 Prompt Anpassen

### Für andere Schulungs-Kontexte

**Beispiel: Data Science Bootcamp**

```python
Kontext:
- Schulungen: "Data Science für Einsteiger"
- Zielgruppe: Career Switcher, Junior Data Scientists
- Tech-Stack: Python, Jupyter, pandas, scikit-learn, TensorFlow
- Fokus: Praktische Data Science Workflows, MLOps
```

**Beispiel: Enterprise AI Development**

```python
Kontext:
- Schulungen: "Enterprise AI Integration"
- Zielgruppe: Senior Developers, Architects
- Tech-Stack: Java, Spring Boot, Azure OpenAI, LangChain
- Fokus: Production-ready AI Integration, Security, Skalierung
```

### Für strengere Filter

Wenn du WENIGER News willst (nur das Wichtigste):

```python
1. RELEVANZ-SCORE (1-5):
   5 = Kritisches Update, das Schulung sofort betrifft
   4 = Sehr relevant für Unterricht
   3 = Interessant für fortgeschrittene Studierende
   2 = Nischentopic
   1 = Nicht relevant

# Dann in generate_report():
high_priority = [item for item in analyzed_items if item.relevance_score >= 5]
```

### Für lockere Filter

Wenn du MEHR News willst (auch experimentelles):

```python
high_priority = [item for item in analyzed_items if item.relevance_score >= 3]
medium_priority = [item for item in analyzed_items if item.relevance_score == 2]
```

## 💰 Kosten & Rate Limits

### Claude Sonnet 4 Pricing (Stand Januar 2025)

```
Input:  ~$3 per Million Tokens
Output: ~$15 per Million Tokens
```

### Typischer Daily Digest (20 News-Items)

```
Pro News-Item:
- Input:  ~500 tokens (Prompt + News)
- Output: ~100 tokens (JSON Response)

Tägliche Kosten:
- Input:  20 × 500 = 10,000 tokens = $0.03
- Output: 20 × 100 = 2,000 tokens  = $0.03
- TOTAL: ~$0.06 pro Tag
```

**Monatlich:** ~$1.80 (bei täglichem Run)
**Jährlich:** ~$22

### Rate Limits

Anthropic Claude API Standard Tier:
- **Requests:** 50 requests/minute
- **Tokens:** 40,000 tokens/minute

**Unser Script:** ~20 requests in 2-3 Minuten → Kein Problem!

### Kosten optimieren

**Option 1: Weniger News analysieren**
```python
# In fetch_news():
for entry in hn_feed.entries[:10]:  # Statt [:20]
```

**Option 2: Caching nutzen**
```python
# Anthropic Prompt Caching (Beta)
# Spart 90% Input-Kosten bei wiederholtem Kontext
```

**Option 3: Nur Werktags**
```yaml
# In .github/workflows/daily_news.yml
schedule:
  - cron: '0 7 * * 1-5'  # Montag-Freitag
```

## 🔐 API Key Setup

### API Key erhalten

1. Gehe zu: https://console.anthropic.com/
2. Login/Signup
3. Settings → API Keys → "Create Key"
4. Kopiere den Key (format: `sk-ant-api03-...`)

### Lokal verwenden

**Option 1: Environment Variable (Empfohlen)**
```bash
export ANTHROPIC_API_KEY='sk-ant-api03-...'
```

**Option 2: .env File**
```bash
# .env
ANTHROPIC_API_KEY=sk-ant-api03-...
```

Dann in Code:
```python
from dotenv import load_dotenv
load_dotenv()
api_key = os.getenv('ANTHROPIC_API_KEY')
```

**Option 3: Config File (NICHT empfohlen)**
```yaml
# ❌ NICHT committen!
api_key: sk-ant-api03-...
```

### In GitHub Actions

Siehe [GITHUB_ACTIONS_SETUP.md](GITHUB_ACTIONS_SETUP.md)

## 🛠️ Troubleshooting

### Error: "ANTHROPIC_API_KEY not set"

**Ursache:** Environment Variable nicht gesetzt

**Lösung:**
```bash
echo $ANTHROPIC_API_KEY  # Sollte deinen Key zeigen
export ANTHROPIC_API_KEY='sk-ant-...'
```

### Error: "Invalid API Key"

**Ursache:** Key falsch kopiert oder abgelaufen

**Lösung:**
1. Console checken: https://console.anthropic.com/settings/keys
2. Neuen Key erstellen
3. Sicherstellen: Keine Leerzeichen beim Kopieren!

### Error: "Rate limit exceeded"

**Ursache:** Zu viele Requests in kurzer Zeit (unwahrscheinlich bei unserem Script)

**Lösung:**
```python
import time

for item in news_items:
    # ...
    time.sleep(0.5)  # 500ms Pause zwischen Requests
```

### Error: "JSON parsing failed"

**Ursache:** Claude hat nicht mit gültigem JSON geantwortet

**Lösung:**
```python
try:
    analysis = json.loads(response.content[0].text)
except json.JSONDecodeError:
    print(f"Claude response: {response.content[0].text}")
    # Fallback zu default values
    analysis = {
        "relevance_score": 2,
        "category": "skip",
        "reasoning": "Analysis failed"
    }
```

### Analyse-Qualität ist schlecht

**Problem:** Claude bewertet nicht nach deinen Kriterien

**Lösung 1: Kontext verbessern**
```python
# Füge MEHR Kontext hinzu
Kontext:
- Schulungen: ...
- Zielgruppe: ...
- Was Studierende BEREITS kennen: React, Python Basics
- Was sie NICHT kennen: Advanced ML, Papers
- Lernziele: Praktische Tool-Nutzung, nicht Theorie
```

**Lösung 2: Few-Shot Examples**
```python
Beispiele:
- "Windsurf 2.0 Update" → Score 5, Kategorie: tools
  Reasoning: "Haupt-IDE der Schulung, Update ist relevant"

- "Research Paper über Transformers" → Score 2, Kategorie: skip
  Reasoning: "Zu theoretisch für praktische Schulung"
```

## 🔄 Alternative LLM APIs

Falls du Claude nicht nutzen willst/kannst:

### OpenAI GPT-4
```python
from openai import OpenAI
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

response = client.chat.completions.create(
    model="gpt-4-turbo",
    messages=[{"role": "user", "content": prompt}],
    max_tokens=300
)
```

**Kosten:** ~$0.01/1K Input Tokens (3× teurer als Claude)

### Ollama (Lokal, kostenlos)
```python
import requests

response = requests.post('http://localhost:11434/api/generate',
    json={
        'model': 'llama2',
        'prompt': prompt
    }
)
```

**Pros:** Kostenlos, Privacy
**Cons:** Langsamere/weniger gute Analyse als Claude

### Google Gemini
```python
import google.generativeai as genai
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

model = genai.GenerativeModel('gemini-1.5-flash')
response = model.generate_content(prompt)
```

**Kosten:** ~$0.075/1M Tokens (günstiger als Claude)

## 📚 Best Practices

### 1. Prompt-Iterationen

Starte mit dem Standard-Prompt, dann:
- Analysiere erste Reports
- Sind Scores zu hoch/niedrig? → Beschreibung anpassen
- Sind Begründungen zu allgemein? → "Konkret auf Schulung beziehen"
- Kategorien falsch? → Klarere Definitionen

### 2. Batch-Processing

```python
# Aktuell: 1 Request pro News-Item
# Besser für Kosten (mit Prompt Caching):
# Batch von 5 Items pro Request
```

### 3. Caching

```python
# Für wiederholte Kontext-Teile
# Spart 90% Input-Kosten
# Siehe: https://docs.anthropic.com/en/docs/build-with-claude/prompt-caching
```

### 4. Monitoring

```python
# Log Costs
total_input_tokens = 0
total_output_tokens = 0

# Nach jedem Request:
total_input_tokens += response.usage.input_tokens
total_output_tokens += response.usage.output_tokens

print(f"Kosten heute: ${total_input_tokens/1e6 * 3 + total_output_tokens/1e6 * 15:.3f}")
```

## 🎓 Weiterführende Links

- **Claude API Docs:** https://docs.anthropic.com/
- **Prompt Engineering Guide:** https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering
- **Rate Limits:** https://docs.anthropic.com/en/api/rate-limits
- **Pricing:** https://www.anthropic.com/pricing

---

**Fragen?** Öffne ein Issue oder schau in die [README.md](README.md) für allgemeine Infos.
