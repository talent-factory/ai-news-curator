#!/usr/bin/env python3
"""
AI News Curator - Intelligenter Filter für AI/ML News
Speziell für Software-Entwicklung mit KI und KI-Integration in Produkte
"""

import os
import json
import anthropic
from datetime import datetime, timedelta
from typing import List, Dict
import feedparser
import requests
from dataclasses import dataclass, asdict

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
    def __init__(self, anthropic_api_key: str):
        self.client = anthropic.Anthropic(api_key=anthropic_api_key)
        self.sources = {
            'anthropic_blog': 'https://www.anthropic.com/news',
            'openai_blog': 'https://openai.com/blog/rss',
            'google_ai': 'https://blog.google/technology/ai/rss',
            'hacker_news_ai': 'https://hnrss.org/newest?q=AI+OR+LLM+OR+Claude+OR+GPT',
        }
    
    def fetch_news(self, hours_back: int = 24) -> List[Dict]:
        """Sammelt News von verschiedenen Quellen"""
        news_items = []
        cutoff_date = datetime.now() - timedelta(hours=hours_back)
        
        # Hacker News AI-relevante Posts
        try:
            hn_feed = feedparser.parse(self.sources['hacker_news_ai'])
            for entry in hn_feed.entries[:20]:  # Top 20
                pub_date = datetime(*entry.published_parsed[:6])
                if pub_date > cutoff_date:
                    news_items.append({
                        'title': entry.title,
                        'url': entry.link,
                        'source': 'Hacker News',
                        'published': pub_date.isoformat(),
                        'summary': entry.get('summary', '')[:500]
                    })
        except Exception as e:
            print(f"Error fetching HN: {e}")
        
        # GitHub Trending
        try:
            gh_url = "https://api.github.com/search/repositories"
            params = {
                'q': 'ai OR llm OR claude OR cursor created:>=' + cutoff_date.strftime('%Y-%m-%d'),
                'sort': 'stars',
                'order': 'desc',
                'per_page': 10
            }
            response = requests.get(gh_url, params=params)
            if response.ok:
                for repo in response.json().get('items', []):
                    news_items.append({
                        'title': f"📦 {repo['full_name']}: {repo['description'][:100]}",
                        'url': repo['html_url'],
                        'source': 'GitHub Trending',
                        'published': repo['created_at'],
                        'summary': repo['description'] or ''
                    })
        except Exception as e:
            print(f"Error fetching GitHub: {e}")
        
        # Reddit r/LocalLLaMA top posts
        try:
            reddit_url = "https://www.reddit.com/r/LocalLLaMA/top.json?t=day&limit=10"
            headers = {'User-Agent': 'AI-News-Curator/1.0'}
            response = requests.get(reddit_url, headers=headers)
            if response.ok:
                for post in response.json().get('data', {}).get('children', []):
                    data = post['data']
                    news_items.append({
                        'title': data['title'],
                        'url': f"https://reddit.com{data['permalink']}",
                        'source': 'Reddit r/LocalLLaMA',
                        'published': datetime.fromtimestamp(data['created_utc']).isoformat(),
                        'summary': data.get('selftext', '')[:500]
                    })
        except Exception as e:
            print(f"Error fetching Reddit: {e}")
        
        return news_items
    
    def analyze_relevance(self, news_items: List[Dict]) -> List[NewsItem]:
        """Nutzt Claude API um Relevanz zu bewerten"""
        
        # Batch-Processing für Effizienz
        filtered_items = []
        
        for item in news_items:
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

            try:
                response = self.client.messages.create(
                    model="claude-sonnet-4-20250514",
                    max_tokens=300,
                    messages=[{"role": "user", "content": prompt}]
                )
                
                analysis = json.loads(response.content[0].text)
                
                filtered_items.append(NewsItem(
                    title=item['title'],
                    url=item['url'],
                    source=item['source'],
                    published=item['published'],
                    summary=item['summary'][:200],
                    relevance_score=analysis['relevance_score'],
                    category=analysis['category'],
                    reasoning=analysis['reasoning']
                ))
                
            except Exception as e:
                print(f"Error analyzing {item['title']}: {e}")
                continue
        
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
        
        if not high_priority:
            report += "_Keine hochprioren Updates heute._\n\n"
        else:
            for item in high_priority:
                report += f"""### {item.title}
**Quelle:** {item.source} | **Score:** {item.relevance_score}/5 | **Kategorie:** {item.category}

💡 **Warum relevant:** {item.reasoning}

🔗 [Link]({item.url})

---

"""
        
        report += """## 📊 Beobachten (Score 3)

"""
        
        if not medium_priority:
            report += "_Keine mittelprioren Updates._\n\n"
        else:
            for item in medium_priority:
                report += f"- **{item.title}** ([Link]({item.url})) - {item.reasoning}\n"
        
        report += f"""

---
**Total analysierte Items:** {len(analyzed_items)}
**Hochpriorität:** {len(high_priority)}
**Mittelpriorität:** {len(medium_priority)}

_Generiert mit Claude API | Talent Factory GmbH_
"""
        
        return report
    
    def run(self, hours_back: int = 24) -> str:
        """Hauptfunktion - führt gesamten Workflow aus"""
        print(f"🔍 Sammle News der letzten {hours_back} Stunden...")
        news_items = self.fetch_news(hours_back)
        print(f"✅ {len(news_items)} Items gefunden")
        
        print("🤖 Analysiere Relevanz mit Claude...")
        analyzed_items = self.analyze_relevance(news_items)
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
