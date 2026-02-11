#!/usr/bin/env python3
"""
Card Data Fetcher
Fetch latest credit card information from various sources
"""

import requests
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List
import time

class CardDataFetcher:
    """Fetch and cache credit card data"""
    
    def __init__(self, cache_dir: str = 'cache'):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(exist_ok=True)
        self.card_data = {}
    
    def fetch_reddit_discussions(self, subreddit: str = 'CreditCardsIndia', limit: int = 10) -> List[dict]:
        """Fetch recent discussions from Reddit"""
        
        url = f"https://www.reddit.com/r/{subreddit}/new.json?limit={limit}"
        headers = {'User-Agent': 'CreditCardOptimizer/1.0'}
        
        try:
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 200:
                data = response.json()
                posts = []
                
                for post in data['data']['children']:
                    post_data = post['data']
                    posts.append({
                        'title': post_data['title'],
                        'url': f"https://reddit.com{post_data['permalink']}",
                        'score': post_data['score'],
                        'created': datetime.fromtimestamp(post_data['created_utc']).isoformat()
                    })
                
                return posts
        except Exception as e:
            print(f"Error fetching Reddit data: {e}")
            return []
    
    def fetch_card_news(self) -> List[dict]:
        """Fetch latest credit card news"""
        
        # In real implementation, scrape from card news sites
        # For now, return placeholder
        
        return [
            {
                'title': 'Latest Credit Card Updates',
                'date': datetime.now().isoformat(),
                'source': 'Multiple'
            }
        ]
    
    def get_cached_data(self, key: str, max_age_hours: int = 24) -> dict:
        """Get cached data if fresh enough"""
        
        cache_file = self.cache_dir / f"{key}.json"
        
        if cache_file.exists():
            # Check age
            file_age = time.time() - cache_file.stat().st_mtime
            if file_age < max_age_hours * 3600:
                with open(cache_file, 'r') as f:
                    return json.load(f)
        
        return None
    
    def save_cache(self, key: str, data: dict):
        """Save data to cache"""
        
        cache_file = self.cache_dir / f"{key}.json"
        with open(cache_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    def generate_data_summary(self) -> str:
        """Generate summary of fetched data"""
        
        summary = f"""# Credit Card Data Summary

**Generated:** {datetime.now().strftime("%B %d, %Y at %I:%M %p IST")}

---

## Recent Reddit Discussions

"""
        
        reddit_posts = self.fetch_reddit_discussions()
        
        for post in reddit_posts[:5]:
            summary += f"- [{post['title']}]({post['url']}) (Score: {post['score']})\n"
        
        summary += "\n---\n\n## Latest News\n\n"
        
        news = self.fetch_card_news()
        for item in news:
            summary += f"- {item['title']} ({item['date']})\n"
        
        summary += "\n---\n\n*Data aggregated by [Credit Card Optimizer](https://github.com/starkarthikr/credit-card-optimizer)*\n"
        
        return summary


if __name__ == "__main__":
    print("=" * 80)
    print("    Credit Card Data Fetcher")
    print("=" * 80)
    
    fetcher = CardDataFetcher()
    
    print("\nFetching latest credit card data...")
    summary = fetcher.generate_data_summary()
    
    # Save summary
    output_dir = Path('recommendations')
    output_dir.mkdir(exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filepath = output_dir / f"{timestamp}-card-data-summary.md"
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(summary)
    
    print(f"\n✅ Data summary saved: {filepath}")
    print("\nSummary Preview:")
    print(summary[:800])
