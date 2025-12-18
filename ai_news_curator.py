#!/usr/bin/env python3
"""
AI News Curator - Intelligenter Filter für AI/ML News
Speziell für Software-Entwicklung mit KI und KI-Integration in Produkte
"""

import os
import json
import re
import time
import anthropic
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import feedparser
import requests
from dataclasses import dataclass, asdict
from dotenv import load_dotenv

# Load environment variables from .env file
# override=True ensures .env takes precedence over shell variables
load_dotenv(override=True)

@dataclass
class NewsItem:
    title: str
    url: str
    source: str
    published: str
    summary: str
    relevance_score: int  # 1-5
    category: str  # "teaching", "tools", "research", "skip"
    reasoning: str

class AINewsCurator:
    def __init__(self, anthropic_api_key: str, prompt_template_path: str = "prompt_template.txt"):
        self.client = anthropic.Anthropic(api_key=anthropic_api_key)
        self.sources = {
            # Official Blogs & News
            'anthropic_blog': 'https://www.anthropic.com/news/rss',
            'openai_blog': 'https://openai.com/blog/rss',
            'google_ai': 'https://blog.google/technology/ai/rss',
            'google_developers': 'https://developers.googleblog.com/feeds/posts/default',

            # AI News Aggregators
            'hacker_news_ai': 'https://hnrss.org/newest?q=AI+OR+LLM+OR+Claude+OR+GPT+OR+Cursor+OR+Windsurf',
            'last_week_in_ai': 'https://lastweekin.ai/feed',
            'daily_dose_ds': 'https://blog.dailydoseofds.com/feed',

            # Developer News
            'infoq_llm': 'https://www.infoq.com/llms/rss',
            'thenewstack': 'https://thenewstack.io/blog/feed/',

            # Tech News
            'techcrunch_ai': 'https://techcrunch.com/category/artificial-intelligence/feed/',
            'venturebeat_ai': 'https://venturebeat.com/category/ai/feed/',
        }

        # Load prompt template from file
        try:
            with open(prompt_template_path, 'r', encoding='utf-8') as f:
                self.prompt_template = f.read()
        except FileNotFoundError:
            print(f"⚠️  Warning: Prompt template not found at {prompt_template_path}")
            print("    Using fallback prompt...")
            self.prompt_template = self._get_fallback_prompt()

    def _get_fallback_prompt(self) -> str:
        """Fallback prompt if template file is not found"""
        return """Du bist ein Experte für AI/ML-Technologien und Hochschul-Bildung.

Analysiere diese News auf Relevanz für Schweizer Hochschul-Schulungen:

KONTEXT:
- Schulungen: "Software-Entwicklung mit KI" und "Integration von KI in Produkte"
- Zielgruppe: IT-Studierende und Young Professionals
- Tech-Stack: Python, Java, React, Claude, GPT, Cursor, Windsurf, Claude Code

NEWS-ITEM:
Titel: {title}
Quelle: {source}
Zusammenfassung: {summary}

RELEVANZ-SCORE (1-5):
5 = Muss sofort in Schulung eingebaut werden
4 = Sehr relevant, baldige Integration sinnvoll
3 = Interessant, beobachten
2 = Wenig relevant
1 = Nicht relevant

KATEGORIE:
- "teaching" = Direkt für Unterricht nutzbar
- "tools" = Tool-Update/neue Entwicklungsumgebung
- "research" = Interessante Entwicklung
- "skip" = Nicht relevant

WICHTIG: Antworte AUSSCHLIESSLICH mit gültigem JSON. Kein Text davor oder danach.

Format:
{{"relevance_score": 3, "category": "tools", "reasoning": "Deine Begründung hier"}}"""

    def load_previous_news(self, days_back: int = 7) -> (set, list):
        """Loads URLs and titles from past reports to avoid duplicates."""
        seen_urls = set()
        seen_titles = []
        import glob
        import re

        # Find all report files
        report_files = glob.glob("ai_news_digest_*.md")
        report_files.sort(reverse=True)

        # Parse the last N reports
        for report_file in report_files[:days_back]:
            try:
                with open(report_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    # Extract URLs from Markdown links: [Link](url)
                    urls = re.findall(r'\[Link\]\((https?://[^\)]+)\)', content)
                    seen_urls.update(urls)
                    # Extract titles from Markdown headers: ### emoji Title
                    titles = re.findall(r'### [^\s]+ (.+)', content)
                    seen_titles.extend([title.strip() for title in titles])
            except Exception as e:
                continue

        return seen_urls, seen_titles

    def extract_json_from_text(self, text: str) -> Optional[Dict]:
        """Extrahiert JSON aus Text, auch wenn Claude Text drum herum schreibt"""
        # Versuche zuerst direktes JSON parsing
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            pass

        # Suche nach JSON-Block im Text (zwischen geschweiften Klammern)
        json_pattern = r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}'
        matches = re.finditer(json_pattern, text, re.DOTALL)

        for match in matches:
            try:
                potential_json = match.group(0)
                return json.loads(potential_json)
            except json.JSONDecodeError:
                continue

        return None
    
    def fetch_news(self, hours_back: int = 168) -> (List[Dict], list):
        """Sammelt News von verschiedenen Quellen (Standard: 7 Tage für Weekly Digest)"""
        news_items = []

        # Load URLs from previous reports to avoid duplicates
        print("🔍 Checking for duplicates in previous reports...")
        seen_urls, seen_titles = self.load_previous_news(days_back=14)
        print(f"   Found {len(seen_urls)} URLs and {len(seen_titles)} titles in previous reports")

        cutoff_date = datetime.now() - timedelta(hours=hours_back)

        # Limit items per source (Google sources are limited to reduce dominance)
        google_sources = {'google_ai', 'google_developers'}

        # Fetch from all RSS feeds
        print(f"📡 Fetching from {len(self.sources)} RSS sources...")
        for source_name, feed_url in self.sources.items():
            try:
                feed = feedparser.parse(feed_url)
                count = 0
                max_items = 10 if source_name in google_sources else 20
                for entry in feed.entries[:max_items]:
                    try:
                        # Parse publication date
                        if hasattr(entry, 'published_parsed') and entry.published_parsed:
                            pub_date = datetime(*entry.published_parsed[:6])
                        elif hasattr(entry, 'updated_parsed') and entry.updated_parsed:
                            pub_date = datetime(*entry.updated_parsed[:6])
                        else:
                            # If no date, use current time
                            pub_date = datetime.now()

                        # Check if recent enough
                        if pub_date < cutoff_date:
                            continue

                        # Get URL and check for duplicates
                        url = entry.get('link', '')
                        if not url or url in seen_urls:
                            continue

                        seen_urls.add(url)

                        # Extract summary
                        summary = entry.get('summary', entry.get('description', ''))
                        if not summary:
                            summary = entry.get('content', [{}])[0].get('value', '') if entry.get('content') else ''

                        # Clean HTML tags from summary
                        import re
                        summary = re.sub(r'<[^>]+>', '', summary)

                        news_items.append({
                            'title': entry.title,
                            'url': url,
                            'source': source_name.replace('_', ' ').title(),
                            'published': pub_date.isoformat(),
                            'summary': summary[:500]
                        })
                        count += 1
                    except Exception as e:
                        # Skip individual entry errors
                        continue

                if count > 0:
                    print(f"  ✓ {source_name}: {count} items")
            except Exception as e:
                print(f"  ✗ {source_name}: {str(e)[:50]}")
        
        # GitHub Trending
        print(f"📡 Fetching GitHub trending repositories...")
        try:
            gh_url = "https://api.github.com/search/repositories"
            params = {
                'q': 'ai OR llm OR claude OR cursor OR windsurf OR antigravity created:>=' + cutoff_date.strftime('%Y-%m-%d'),
                'sort': 'stars',
                'order': 'desc',
                'per_page': 15
            }
            response = requests.get(gh_url, params=params)
            if response.ok:
                gh_count = 0
                for repo in response.json().get('items', []):
                    url = repo['html_url']
                    if url not in seen_urls:
                        seen_urls.add(url)
                        news_items.append({
                            'title': f"📦 {repo['full_name']}: {repo['description'][:100] if repo['description'] else 'No description'}",
                            'url': url,
                            'source': 'GitHub Trending',
                            'published': repo['created_at'],
                            'summary': repo['description'] or 'No description available'
                        })
                        gh_count += 1
                print(f"  ✓ GitHub: {gh_count} repos")
            else:
                print(f"  ✗ GitHub: HTTP {response.status_code}")
        except Exception as e:
            print(f"  ✗ GitHub: {str(e)[:50]}")
        
        # Reddit r/LocalLLaMA top posts
        print(f"📡 Fetching Reddit r/LocalLLaMA...")
        try:
            reddit_url = "https://www.reddit.com/r/LocalLLaMA/top.json?t=day&limit=15"
            headers = {'User-Agent': 'AI-News-Curator/2.0'}
            response = requests.get(reddit_url, headers=headers)
            if response.ok:
                reddit_count = 0
                for post in response.json().get('data', {}).get('children', []):
                    data = post['data']
                    url = f"https://reddit.com{data['permalink']}"
                    if url not in seen_urls:
                        seen_urls.add(url)
                        news_items.append({
                            'title': data['title'],
                            'url': url,
                            'source': 'Reddit r/LocalLLaMA',
                            'published': datetime.fromtimestamp(data['created_utc']).isoformat(),
                            'summary': data.get('selftext', '')[:500]
                        })
                        reddit_count += 1
                print(f"  ✓ Reddit: {reddit_count} posts")
            else:
                print(f"  ✗ Reddit: HTTP {response.status_code}")
        except Exception as e:
            print(f"  ✗ Reddit: {str(e)[:50]}")

        print(f"\n✅ Total fetched: {len(news_items)} unique items from {len(self.sources) + 2} sources")
        return news_items, seen_titles
    
    def analyze_relevance(self, news_items: List[Dict], seen_titles: list) -> List[NewsItem]:
        """Nutzt Claude API um Relevanz zu bewerten"""

        filtered_items = []
        success_count = 0
        error_count = 0

        # Format seen_titles for the prompt
        seen_titles_text = "\n".join(f"- {title}" for title in seen_titles)

        for idx, item in enumerate(news_items, 1):
            # Rate limiting: Kleine Pause zwischen Requests
            if idx > 1:
                time.sleep(0.3)

            # Use template and fill in the news item details
            prompt = self.prompt_template.format(
                title=item['title'],
                source=item['source'],
                summary=item['summary'][:300],
                recent_news=seen_titles_text
            )

            try:
                response = self.client.messages.create(
                    model="claude-sonnet-4-20250514",
                    max_tokens=400,
                    messages=[{"role": "user", "content": prompt}]
                )

                # Verbesserte JSON-Extraktion
                response_text = response.content[0].text.strip()
                analysis = self.extract_json_from_text(response_text)

                if not analysis:
                    raise ValueError(f"Konnte kein JSON in Response finden: {response_text[:100]}")

                # Validierung der erforderlichen Felder
                if 'relevance_score' not in analysis or 'category' not in analysis:
                    raise ValueError(f"JSON fehlt erforderliche Felder: {analysis}")

                # Fallback für fehlendes reasoning
                reasoning = analysis.get('reasoning', 'Keine Begründung verfügbar')

                filtered_items.append(NewsItem(
                    title=item['title'],
                    url=item['url'],
                    source=item['source'],
                    published=item['published'],
                    summary=item['summary'][:200],
                    relevance_score=int(analysis['relevance_score']),
                    category=analysis['category'],
                    reasoning=reasoning
                ))
                success_count += 1

            except Exception as e:
                error_count += 1
                # Detaillierteres Error-Logging für Debugging
                if error_count <= 3:  # Zeige nur erste 3 Fehler im Detail
                    print(f"⚠️  Error analyzing '{item['title'][:50]}...': {e}")

                # Fallback: Füge Item mit niedrigem Score hinzu statt es zu verlieren
                filtered_items.append(NewsItem(
                    title=item['title'],
                    url=item['url'],
                    source=item['source'],
                    published=item['published'],
                    summary=item['summary'][:200],
                    relevance_score=1,  # Niedrigster Score
                    category='skip',
                    reasoning=f'Automatische Analyse fehlgeschlagen: {str(e)[:100]}'
                ))

        print(f"📊 Analyse-Statistik: {success_count} erfolgreich, {error_count} Fehler")

        # Sortiere nach Relevanz
        return sorted(filtered_items, key=lambda x: x.relevance_score, reverse=True)
    
    def generate_report(self, analyzed_items: List[NewsItem]) -> str:
        """Erstellt Markdown-Report"""

        today = datetime.now().strftime("%Y-%m-%d")

        report = f"""# 🎯 AI News Digest für Teaching
**Datum:** {today}
**Generiert für:** Talent Factory GmbH - Software-Entwicklung mit KI

---

## 🔥 Sofort relevant (Score 4-5)

"""

        high_priority = [item for item in analyzed_items if item.relevance_score >= 4]
        medium_priority = [item for item in analyzed_items if item.relevance_score == 3]

        # Kategorien-Emojis für bessere Übersicht
        category_emojis = {
            'llm_release': '🤖',
            'cli_tools': '⌨️',
            'teaching': '🎓',
            'tools': '🛠️',
            'research': '🔬',
            'frameworks': '📦'
        }

        if not high_priority:
            report += "_Keine hochprioritäre Updates heute._\n\n"
        else:
            for item in high_priority:
                emoji = category_emojis.get(item.category, '📌')
                report += f"""### {emoji} {item.title}
**Quelle:** {item.source} | **Score:** {item.relevance_score}/5 | **Kategorie:** {item.category}

💡 **Warum relevant:** {item.reasoning}

🔗 [Link]({item.url})

---

"""

        report += """## 📊 Beobachten (Score 3)

"""

        if not medium_priority:
            report += "_Keine mittelprioritäre Updates._\n\n"
        else:
            for item in medium_priority:
                emoji = category_emojis.get(item.category, '📌')
                report += f"- {emoji} **{item.title}** ([Link]({item.url})) - {item.reasoning}\n"

        # Kategorien-Statistik
        categories = {}
        for item in analyzed_items:
            categories[item.category] = categories.get(item.category, 0) + 1

        report += f"""

---
**Total analysierte Items:** {len(analyzed_items)}
**Hochpriorität:** {len(high_priority)}
**Mittelpriorität:** {len(medium_priority)}

**Nach Kategorien:**
"""
        for cat, count in sorted(categories.items(), key=lambda x: x[1], reverse=True):
            emoji = category_emojis.get(cat, '📌')
            report += f"- {emoji} {cat}: {count}\n"

        report += "\n_Generiert mit Claude API | Talent Factory GmbH_\n"

        return report
    
    def run(self, hours_back: int = 24) -> str:
        """Hauptfunktion - führt gesamten Workflow aus"""
        print(f"🔍 Sammle News der letzten {hours_back} Stunden...")
        news_items, seen_titles = self.fetch_news(hours_back)
        print(f"✅ {len(news_items)} Items gefunden")
        
        print("🤖 Analysiere Relevanz mit Claude...")
        analyzed_items = self.analyze_relevance(news_items, seen_titles)
        print(f"✅ {len(analyzed_items)} Items analysiert")
        
        print("📝 Generiere Report...")
        report = self.generate_report(analyzed_items)
        
        # Speichere Report
        output_file = f"ai_news_digest_{datetime.now().strftime('%Y%m%d')}.md"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(report)
        
        print(f"✅ Report gespeichert: {output_file}")
        return report


def main():
    # API Key aus Environment Variable
    api_key = os.getenv('ANTHROPIC_API_KEY')
    if not api_key:
        print("❌ Error: ANTHROPIC_API_KEY environment variable nicht gesetzt!")
        print("Setze mit: export ANTHROPIC_API_KEY='dein-key'")
        return
    
    curator = AINewsCurator(api_key)
    report = curator.run(hours_back=24)
    print("\n" + "="*60)
    print(report[:500] + "...")
    print("="*60)


if __name__ == "__main__":
    main()
