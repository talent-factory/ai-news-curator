# Contributing to AI News Curator

Vielen Dank für dein Interesse, zum AI News Curator beizutragen! 🎉

Dieses Projekt wurde von **Talent Factory GmbH** entwickelt und ist als Open-Source-Tool für die AI/ML-Community verfügbar.

## 🤝 Wie kann ich beitragen?

Es gibt viele Möglichkeiten, zu diesem Projekt beizutragen:

- 🐛 **Bug Reports:** Melde Fehler via GitHub Issues
- ✨ **Feature Requests:** Schlage neue Features vor
- 📚 **Dokumentation:** Verbessere README, Guides, Kommentare
- 🌍 **Übersetzungen:** Übersetze Prompts für andere Sprachen
- 💻 **Code:** Implementiere Features, fixe Bugs
- 🎨 **Prompt Engineering:** Optimiere den Analyse-Prompt
- 🧪 **Testing:** Schreibe Tests, teste neue Features

## 🚀 Getting Started

### 1. Fork & Clone

```bash
# Fork das Repository auf GitHub
# Dann clone deinen Fork:
git clone https://github.com/DEIN-USERNAME/ai-news-curator.git
cd ai-news-curator
```

### 2. Setup Development Environment

```bash
# Installiere Dependencies
pip install -r requirements.txt

# Optional: Installiere Development Tools
pip install pytest black ruff mypy

# Setze deinen API Key
export ANTHROPIC_API_KEY='sk-ant-...'
```

### 3. Erstelle einen Feature Branch

```bash
# Vom develop branch abzweigen
git checkout develop
git pull origin develop

# Erstelle Feature Branch
git checkout -b feature/deine-feature-beschreibung
```

### 4. Mache deine Änderungen

- Schreibe sauberen, gut dokumentierten Code
- Folge dem bestehenden Code-Stil
- Teste deine Änderungen lokal
- Schreibe/aktualisiere Tests falls relevant

### 5. Commit deine Änderungen

Verwende konventionelle Commit-Messages:

```bash
git add .
git commit -m "feat: Füge neue News-Quelle Substack hinzu"

# Oder für Bug Fixes:
git commit -m "fix: Behebe JSON-Parsing-Fehler bei Reddit API"
```

**Commit Types:**
- `feat`: Neue Features
- `fix`: Bug Fixes
- `docs`: Dokumentation
- `style`: Formatierung, Code-Stil
- `refactor`: Code-Umstrukturierung
- `test`: Tests hinzufügen/ändern
- `chore`: Build, Dependencies, Tools

### 6. Push & Pull Request

```bash
# Push zu deinem Fork
git push origin feature/deine-feature-beschreibung

# Gehe zu GitHub und erstelle einen Pull Request:
# - Base: talent-factory/ai-news-curator:develop
# - Compare: DEIN-USERNAME/ai-news-curator:feature/deine-feature-beschreibung
```

## 📝 Pull Request Guidelines

### Was macht einen guten PR aus?

1. **Klare Beschreibung:**
   - Was ändert der PR?
   - Warum ist die Änderung notwendig?
   - Wie wurde es getestet?

2. **Fokussiert:**
   - Ein PR = Ein Feature/Fix
   - Kleine, reviewbare PRs bevorzugt
   - Nicht mehrere unabhängige Änderungen mischen

3. **Getestet:**
   - Lokal getestet
   - Keine kaputten Tests
   - Neue Tests für neue Features

4. **Dokumentiert:**
   - README aktualisiert falls nötig
   - Code-Kommentare wo sinnvoll
   - CLAUDE.md bei Prompt-Änderungen

### PR Template

Dein PR sollte folgende Informationen enthalten:

```markdown
## 📝 Beschreibung
Kurze Beschreibung der Änderungen

## 🎯 Motivation
Warum ist diese Änderung notwendig?

## 🧪 Testing
Wie wurde getestet?
- [ ] Lokal getestet
- [ ] Unit Tests hinzugefügt/aktualisiert
- [ ] Manuell mit echten News getestet

## 📸 Screenshots (falls relevant)
Füge Screenshots hinzu für UI/Report-Änderungen

## ✅ Checklist
- [ ] Code folgt dem Projekt-Stil
- [ ] Dokumentation aktualisiert
- [ ] Tests passieren
- [ ] Commit-Message folgt Convention
```

## 🎨 Code Style

### Python Style Guide

- **PEP 8** konform
- **Type Hints** verwenden wo möglich
- **Docstrings** für Funktionen/Klassen
- **Max 100 Zeichen** pro Zeile (flexibel)

**Beispiel:**
```python
def fetch_news(self, hours_back: int = 24) -> List[Dict]:
    """Sammelt News von verschiedenen Quellen

    Args:
        hours_back: Anzahl Stunden in die Vergangenheit

    Returns:
        Liste von News-Items als Dicts
    """
    news_items = []
    # ...
    return news_items
```

### Formatierung

```bash
# Automatische Formatierung mit Black (optional)
black ai_news_curator.py

# Linting mit Ruff (optional)
ruff check ai_news_curator.py
```

## 📚 Dokumentation

### Wann Dokumentation aktualisieren?

- **README.md**: Bei neuen Features, Setup-Änderungen
- **CLAUDE.md**: Bei Prompt-Änderungen, API-Updates
- **CONTRIBUTING.md**: Bei Prozess-Änderungen
- **Code-Kommentare**: Bei komplexer Logik

### Dokumentations-Stil

- Klar und präzise
- Deutsch für Hauptdokumentation
- Englisch für Code-Kommentare (optional)
- Beispiele wo hilfreich

## 🧪 Testing

### Manuelle Tests

```bash
# Teste mit echten News
python ai_news_curator.py

# Teste ohne API Key (nur Source-Fetching)
python test_sources.py
```

### Unit Tests (optional, noch nicht implementiert)

```bash
pytest tests/
```

## 🐛 Bug Reports

Gute Bug Reports enthalten:

1. **Beschreibung**: Was ist das Problem?
2. **Reproduktion**: Schritte um den Bug zu reproduzieren
3. **Erwartetes Verhalten**: Was sollte passieren?
4. **Aktuelles Verhalten**: Was passiert stattdessen?
5. **Environment**: Python Version, OS, etc.
6. **Logs/Screenshots**: Error Messages, Stack Traces

**Beispiel:**
```markdown
### Beschreibung
Claude API gibt JSON-Parsing-Fehler bei Reddit Posts

### Reproduktion
1. python ai_news_curator.py
2. Warte bis Reddit-Posts analysiert werden
3. Error tritt bei ~5. Post auf

### Environment
- Python 3.11
- macOS 14.0
- anthropic==0.40.0

### Error Log
```
KeyError: 'relevance_score'
...
```
```

## ✨ Feature Requests

Gute Feature Requests enthalten:

1. **Problem**: Welches Problem löst das Feature?
2. **Lösung**: Wie stellst du dir die Lösung vor?
3. **Alternativen**: Hast du andere Ansätze erwogen?
4. **Use Case**: Wann würdest du das Feature nutzen?

## 🎯 Prompt Engineering Contributions

Der Prompt (`prompt_template.txt`) ist das Herzstück des Tools!

### Prompt verbessern

1. **Problem identifizieren:**
   - Welche News werden falsch bewertet?
   - Welche Kategorien sind unklar?

2. **Änderung vorschlagen:**
   - Teste lokal mit verschiedenen News
   - Dokumentiere Verbesserung in PR

3. **Beispiele hinzufügen:**
   - Füge Few-Shot Examples hinzu
   - Erkläre Reasoning

### Prompt für andere Domänen

Erstelle Varianten für andere Use Cases:

```
prompts/
├── v2.0_teaching.txt          # Original
├── v2.0_data_science.txt      # Data Science Focus
├── v2.0_enterprise.txt        # Enterprise AI Focus
├── v2.0_research.txt          # Academic Research
```

## 🌍 Übersetzungen

### Prompt-Übersetzungen

Übersetze `prompt_template.txt` für andere Sprachen:

```
prompts/
├── de/
│   └── prompt_template.txt
├── en/
│   └── prompt_template.txt
├── fr/
│   └── prompt_template.txt
```

### Dokumentations-Übersetzungen

Übersetze README, CONTRIBUTING für internationale Community.

## 🔒 Security

**WICHTIG:** Committe niemals API Keys!

- Keine Keys in Code oder Configs
- Nutze `.env` Files (werden ignoriert)
- Nutze Environment Variables

Falls du versehentlich einen Key committed hast:
1. Regeneriere den Key sofort
2. Nutze `git filter-branch` oder BFG Repo-Cleaner
3. Force Push (nur für eigenen Fork!)

Siehe [SECURITY.md](SECURITY.md) für Details.

## 💬 Community

### Fragen stellen

- **GitHub Issues**: Für Bugs, Features, Fragen
- **Discussions**: Für allgemeine Diskussionen (falls aktiviert)

### Respektvoller Umgang

Bitte lies unseren [Code of Conduct](CODE_OF_CONDUCT.md).

## 📜 License

Durch deinen Beitrag stimmst du zu, dass deine Änderungen unter der **MIT License** veröffentlicht werden.

## 🙏 Danke!

Jeder Beitrag - egal wie klein - hilft der Community!

Besonderer Dank geht an alle Contributors! 🎉

---

**Entwickelt von:** Talent Factory GmbH
**Maintainer:** @daniel-senften (Daniel kann direkt auf develop pushen)
**Community:** Open for all contributions via Pull Requests
