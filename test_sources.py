#!/usr/bin/env python3
"""
Test Script - Überprüft News-Sammlung ohne API Key
Nützlich zum Debuggen der News-Quellen
"""

import feedparser
import requests
from datetime import datetime, timedelta
import json

def test_hacker_news():
    print("\n🔍 Testing Hacker News AI Feed...")
    try:
        feed = feedparser.parse('https://hnrss.org/newest?q=AI+OR+LLM+OR+Claude+OR+GPT')
        print(f"✅ Found {len(feed.entries)} entries")
        if feed.entries:
            print(f"   Latest: {feed.entries[0].title[:80]}...")
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_reddit():
    print("\n🔍 Testing Reddit r/LocalLLaMA...")
    try:
        url = "https://www.reddit.com/r/LocalLLaMA/top.json?t=day&limit=5"
        headers = {'User-Agent': 'AI-News-Test/1.0'}
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.ok:
            data = response.json()
            posts = data.get('data', {}).get('children', [])
            print(f"✅ Found {len(posts)} posts")
            if posts:
                print(f"   Top post: {posts[0]['data']['title'][:80]}...")
            return True
        else:
            print(f"❌ HTTP {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_github():
    print("\n🔍 Testing GitHub Trending...")
    try:
        cutoff = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
        url = "https://api.github.com/search/repositories"
        params = {
            'q': f'ai OR llm created:>={cutoff}',
            'sort': 'stars',
            'per_page': 5
        }
        response = requests.get(url, params=params, timeout=10)
        
        if response.ok:
            repos = response.json().get('items', [])
            print(f"✅ Found {len(repos)} trending repos")
            if repos:
                print(f"   Top repo: {repos[0]['full_name']}")
            return True
        else:
            print(f"❌ HTTP {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_all():
    print("="*60)
    print("🧪 AI News Curator - Source Testing")
    print("="*60)
    
    results = {
        'Hacker News': test_hacker_news(),
        'Reddit': test_reddit(),
        'GitHub': test_github()
    }
    
    print("\n" + "="*60)
    print("📊 Summary:")
    for source, success in results.items():
        status = "✅ OK" if success else "❌ FAILED"
        print(f"   {source:20} {status}")
    
    all_success = all(results.values())
    print("="*60)
    
    if all_success:
        print("\n✅ Alle Quellen funktionieren!")
        print("Nächster Schritt: python ai_news_curator.py")
    else:
        print("\n⚠️  Einige Quellen haben Probleme.")
        print("Das ist meist temporär - versuche es später nochmal.")
    
    return all_success

if __name__ == "__main__":
    test_all()
