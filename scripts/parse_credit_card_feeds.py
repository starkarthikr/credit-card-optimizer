#!/usr/bin/env python3
"""
Credit Card Optimizer for India
Tracks offers, rewards, redemption tips, and optimization strategies
Focused on Indian credit cards and banking ecosystem
"""

import feedparser
import json
import re
from datetime import datetime, timedelta
from pathlib import Path
import requests
from bs4 import BeautifulSoup

# Indian Credit Card News & Offers Sources
FEEDS = {
    # Credit Card Expert Blogs
    'cardexpert': 'https://www.cardexpert.in/feed/',
    'cardinsider': 'https://cardinsider.com/blog/feed/',
    '1finance': 'https://1finance.co.in/feed/',
    
    # Financial News
    'moneycontrol_cards': 'https://www.moneycontrol.com/rss/creditcards.xml',
    'economic_times': 'https://economictimes.indiatimes.com/wealth/spend/rssfeeds/837555174.cms',
    
    # Banking Blogs
    'paisabazaar': 'https://www.paisabazaar.com/blog/feed/',
    'bankbazaar': 'https://www.bankbazaar.com/rss/finance.xml',
    
    # Fintech
    'finology': 'https://select.finology.in/feed',
}

# Manual curated sources (scraped periodically)
MANUAL_SOURCES = {
    'sbi_offers': 'https://www.sbicard.com/en/personal/offers.page',
    'hdfc_offers': 'https://www.hdfcbank.com/personal/pay/cards/credit-cards/credit-card-offers',
    'icici_offers': 'https://www.icicibank.com/credit-card/offers',
    'axis_offers': 'https://www.axisbank.com/retail/cards/credit-card/offers',
}

OUTPUT_DIR = Path('credit_card_updates')
OUTPUT_DIR.mkdir(exist_ok=True)

def fetch_feed(feed_url, feed_name):
    """Fetch and parse RSS feed"""
    try:
        print(f"Fetching {feed_name} from {feed_url}")
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        feed = feedparser.parse(feed_url, request_headers=headers)
        
        if feed.bozo:
            print(f"Warning: Feed parsing issue for {feed_name}")
        return feed
    except Exception as e:
        print(f"Error fetching {feed_name}: {e}")
        return None

def is_recent(published_date, days=7):
    """Check if article is from last N days"""
    try:
        if hasattr(published_date, 'timetuple'):
            pub_date = datetime(*published_date.timetuple()[:6])
        else:
            return True
        cutoff = datetime.now() - timedelta(days=days)
        return pub_date >= cutoff
    except:
        return True

def clean_html_text(html_text):
    """Remove HTML tags and clean text"""
    text = re.sub(r'<[^>]+>', '', html_text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def extract_key_info(title, content):
    """
    Extract structured information: Card Name, Offer Type, Redemption Value, Tips
    """
    analysis = {
        'card_name': None,
        'bank': None,
        'offer_type': None,
        'cashback_rate': None,
        'annual_fee': None,
        'reward_rate': None,
        'benefits': [],
        'optimization_tips': [],
        'redemption_info': None,
        'category': None
    }
    
    if not content:
        content = title
    
    content_lower = content.lower()
    title_lower = title.lower()
    
    # Extract Bank Name
    banks = ['hdfc', 'sbi', 'icici', 'axis', 'amex', 'american express', 
             'indusind', 'yes bank', 'kotak', 'standard chartered', 'citi', 'au',
             'rbl', 'idfc']
    
    for bank in banks:
        if bank in title_lower or bank in content_lower:
            analysis['bank'] = bank.upper()
            break
    
    # Extract Card Name
    card_patterns = [
        r'(\w+\s+\w+\s+credit\s+card)',
        r'(\w+\s+card)',
        r'([A-Z][a-z]+\s+[A-Z][a-z]+\s+Card)'
    ]
    
    for pattern in card_patterns:
        match = re.search(pattern, title + ' ' + content, re.IGNORECASE)
        if match:
            analysis['card_name'] = match.group(1)
            break
    
    # Categorize content type
    categories = {
        'New Offer': ['new offer', 'latest offer', 'exclusive offer', 'limited time'],
        'Devaluation': ['devaluation', 'reduced', 'benefit cut', 'lower rewards'],
        'Reward Points': ['reward points', 'redemption', 'points value', 'cashback'],
        'Best Card': ['best card', 'top card', 'recommended', 'comparison'],
        'Tricks & Tips': ['tips', 'tricks', 'hack', 'optimize', 'maximize'],
        'Annual Fee': ['annual fee', 'waiver', 'fee reversal'],
        'Travel Benefits': ['lounge', 'airport', 'travel', 'flight', 'hotel'],
        'Cashback': ['cashback', 'cash back', 'statement credit'],
    }
    
    for category, keywords in categories.items():
        for keyword in keywords:
            if keyword in content_lower or keyword in title_lower:
                analysis['category'] = category
                break
        if analysis['category']:
            break
    
    # Extract Cashback/Reward Rate
    cashback_patterns = [
        r'(\d+)%\s*cashback',
        r'(\d+)%\s*cash\s*back',
        r'(\d+)X\s*reward',
        r'(\d+)X\s*points'
    ]
    
    for pattern in cashback_patterns:
        match = re.search(pattern, content, re.IGNORECASE)
        if match:
            analysis['cashback_rate'] = match.group(0)
            break
    
    # Extract Annual Fee
    fee_patterns = [
        r'₹\s*(\d{1,5})\s*annual\s*fee',
        r'joining\s*fee.*?₹\s*(\d{1,5})',
        r'fee.*?₹\s*(\d{1,5})'
    ]
    
    for pattern in fee_patterns:
        match = re.search(pattern, content, re.IGNORECASE)
        if match:
            analysis['annual_fee'] = f"₹{match.group(1)}"
            break
    
    # Extract Benefits
    benefit_keywords = ['lounge access', 'fuel surcharge', 'movie ticket', 
                       'dining discount', 'milestone benefit', 'welcome bonus',
                       'complimentary', 'insurance', 'concierge']
    
    for keyword in benefit_keywords:
        if keyword in content_lower:
            analysis['benefits'].append(keyword.title())
    
    # Extract Optimization Tips
    tip_indicators = ['tip', 'trick', 'hack', 'optimize', 'maximize', 'best way']
    
    for indicator in tip_indicators:
        if indicator in content_lower:
            # Extract sentences containing tips
            sentences = re.split(r'[.!?]+', content)
            for sent in sentences:
                if indicator in sent.lower() and len(sent.strip()) > 30:
                    analysis['optimization_tips'].append(sent.strip()[:250])
                    if len(analysis['optimization_tips']) >= 3:
                        break
    
    # Extract Redemption Info
    redemption_keywords = ['redeem', 'redemption', 'value of point', 'points worth']
    
    for keyword in redemption_keywords:
        if keyword in content_lower:
            sentences = re.split(r'[.!?]+', content)
            for sent in sentences:
                if keyword in sent.lower() and len(sent.strip()) > 30:
                    analysis['redemption_info'] = sent.strip()[:300]
                    break
            if analysis['redemption_info']:
                break
    
    return analysis

def extract_article_content(link):
    """Extract article content from webpage"""
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        response = requests.get(link, headers=headers, timeout=15)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        content = None
        article = soup.find('article')
        if article:
            paragraphs = article.find_all('p')
            if paragraphs:
                content = ' '.join([p.get_text() for p in paragraphs[:12]])
        
        if not content:
            meta_desc = soup.find('meta', {'name': 'description'})
            if meta_desc:
                content = meta_desc.get('content')
        
        return content
    except Exception as e:
        print(f"  Warning: Could not extract content: {e}")
        return None

def generate_summary(title, description, content):
    """Generate concise summary"""
    if description:
        clean_desc = clean_html_text(description)
        sentences = re.split(r'[.!?]+', clean_desc)
        if sentences and len(sentences[0]) > 20:
            summary = sentences[0].strip()
            if len(summary) > 200:
                return summary[:197] + '...'
            return summary + '.'
    
    if content:
        clean_content = clean_html_text(content)
        sentences = re.split(r'[.!?]+', clean_content)
        if sentences and len(sentences[0]) > 20:
            summary = sentences[0].strip()
            if len(summary) > 200:
                return summary[:197] + '...'
            return summary + '.'
    
    return f"Credit card update: {title}"

def process_feeds():
    """Process all RSS feeds"""
    all_articles = []
    recent_articles = []
    
    for feed_name, feed_url in FEEDS.items():
        feed = fetch_feed(feed_url, feed_name)
        
        if not feed or not hasattr(feed, 'entries'):
            continue
        
        print(f"Found {len(feed.entries)} entries in {feed_name}")
        
        for entry in feed.entries[:15]:
            print(f"  Processing: {entry.get('title', 'No Title')[:60]}...")
            
            description = entry.get('summary', '')
            content = entry.get('content', [{}])[0].get('value', '') if 'content' in entry else ''
            
            full_content = None
            card_analysis = None
            
            if hasattr(entry, 'published_parsed') and is_recent(entry.published_parsed, days=7):
                full_content = extract_article_content(entry.get('link', ''))
                if full_content:
                    card_analysis = extract_key_info(
                        entry.get('title', ''),
                        full_content
                    )
            
            summary = generate_summary(
                entry.get('title', ''),
                description or full_content,
                content
            )
            
            article = {
                'source': feed_name.replace('_', ' ').title(),
                'title': entry.get('title', 'No Title'),
                'link': entry.get('link', ''),
                'published': entry.get('published', 'Unknown'),
                'summary': summary,
            }
            
            if card_analysis:
                article['card_info'] = card_analysis
            
            if hasattr(entry, 'published_parsed') and is_recent(entry.published_parsed, days=7):
                recent_articles.append(article)
            
            all_articles.append(article)
    
    return all_articles, recent_articles

def save_json_report(articles, filename):
    """Save articles as JSON"""
    filepath = OUTPUT_DIR / filename
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(articles, f, indent=2, ensure_ascii=False)
    print(f"Saved {len(articles)} articles to {filepath}")

def generate_markdown_report(recent_articles):
    """Generate Markdown report with card analysis"""
    md_content = f"""# 💳 Credit Card Optimizer - India

**Last Updated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S IST')}

## 🎯 Latest Offers & Updates (Last 7 Days)

"""
    
    if not recent_articles:
        md_content += "*No new updates in the last 7 days.*\n"
    else:
        # Group by category
        by_category = {}
        for article in recent_articles:
            cat = article.get('card_info', {}).get('category', 'General Updates')
            if cat not in by_category:
                by_category[cat] = []
            by_category[cat].append(article)
        
        for category in sorted(by_category.keys()):
            articles = by_category[category]
            
            category_emoji = {
                'New Offer': '🎁',
                'Devaluation': '⚠️',
                'Reward Points': '💰',
                'Best Card': '🏆',
                'Tricks & Tips': '💡',
                'Annual Fee': '💵',
                'Travel Benefits': '✈️',
                'Cashback': '💸'
            }.get(category, '📊')
            
            md_content += f"\n### {category_emoji} {category}\n\n"
            
            for idx, article in enumerate(articles[:5], 1):
                md_content += f"#### {idx}. [{article['title']}]({article['link']})\n\n"
                
                md_content += f"**📡 Source:** {article['source']}  \n"
                md_content += f"**📅 Published:** {article['published']}  \n"
                
                # Card Info
                if article.get('card_info'):
                    info = article['card_info']
                    
                    if info.get('bank'):
                        md_content += f"**🏦 Bank:** {info['bank']}  \n"
                    
                    if info.get('card_name'):
                        md_content += f"**💳 Card:** {info['card_name']}  \n"
                    
                    if info.get('cashback_rate'):
                        md_content += f"**💰 Reward:** {info['cashback_rate']}  \n"
                    
                    if info.get('annual_fee'):
                        md_content += f"**💵 Fee:** {info['annual_fee']}  \n"
                
                # Summary
                md_content += f"\n**📝 Summary:** {article['summary']}\n"
                
                # Detailed Analysis
                if article.get('card_info'):
                    info = article['card_info']
                    
                    if info.get('benefits'):
                        md_content += f"\n**✨ Benefits:** {', '.join(info['benefits'][:5])}\n"
                    
                    if info.get('redemption_info'):
                        md_content += f"\n**🔄 Redemption:** {info['redemption_info']}\n"
                    
                    if info.get('optimization_tips'):
                        md_content += "\n**💡 Optimization Tips:**\n\n"
                        for tip in info['optimization_tips'][:3]:
                            md_content += f"- {tip}\n"
                
                md_content += "\n---\n\n"
    
    # Add optimization guide
    md_content += f"""
## 💡 Credit Card Optimization Strategies

### 🎯 Maximize Rewards

**1. Category-Based Spending**
- Use specific cards for specific categories (5% on online, 10X on dining)
- Stack merchant offers with card rewards
- Rotate cards based on quarterly bonus categories

**2. Milestone Benefits**
- Track annual spend thresholds for fee waivers (typically ₹1-3 lakhs)
- Plan big purchases before milestone deadlines
- Combine family cards to reach thresholds faster

**3. Welcome Bonuses**
- Apply for cards with high welcome point offers (10,000-25,000 points)
- Meet minimum spend within 60-90 days
- Calculate if welcome bonus > annual fee

### 💸 Cashback Maximization

**Top Cashback Cards India 2025:**
- **SBI Cashback**: 5% online (capped ₹5,000/month)
- **Axis Ace**: 2% via Google Pay, 1% others
- **HDFC Swiggy**: 10% on Swiggy, 5% on partners

**Hacks:**
- Buy gift vouchers at 5-10% discount using reward points
- Use UPI credit cards for 1-2% additional cashback
- Stack bank offers (10% instant discount + regular rewards)

### 🔄 Reward Point Redemption

**Best Redemption Methods (by value):**

1. **Travel Portals** (₹0.40-0.50 per point)
   - Book flights/hotels via bank travel portals
   - Transfer to airline partners (Vistara, Emirates)

2. **Fuel Vouchers** (₹0.30-0.40 per point)
   - HP, Indian Oil, BPCL vouchers
   - No markup, direct value

3. **Statement Credit** (₹0.20-0.30 per point)
   - Instant credit to card account
   - Good for clearing dues

4. **Shopping Vouchers** (₹0.15-0.25 per point)
   - Amazon, Flipkart, brand vouchers
   - Check for markup/premium pricing

**Avoid:**
- Gift catalog items (poor value, 30-50% markup)
- Cash redemption (lowest rate, typically ₹0.10-0.15)

### ⚠️ Annual Fee Optimization

**Waiver Strategies:**
- Achieve spend-based reversal (₹1-3L annually)
- Call retention team before renewal for offers
- Downgrade to LTF variant if not using premium features
- Cancel 45+ days before renewal to avoid pro-rated charges

**Fee vs Benefit Calculation:**
```
Break-even = Annual Fee ÷ Reward Rate
Example: ₹1,000 fee ÷ 5% cashback = ₹20,000 minimum spend needed
```

### 🛡️ Avoid Common Mistakes

1. **Interest Charges**: Always pay full statement (30-42% APR destroys rewards)
2. **Late Fees**: Set auto-pay for minimum due at least
3. **Cash Advances**: Avoid completely (2.5-3% fee + interest from day 1)
4. **Forex Markup**: Use 0 forex cards abroad (Niyo, Fi, IndusInd)
5. **EMI Conversion**: Hidden charges, reduces reward eligibility

### 📈 Advanced Hacks

**Rent Payment:**
- Pay rent via credit card (1.5-2% fee)
- Earn 1-5% rewards = Net gain if reward > fee
- Cards: HDFC Millennia, Axis Magnus

**Fuel Surcharge:**
- 1% fuel surcharge waiver (₹100-500 cap/month)
- Combine with petrol station loyalty programs

**Wallet Loading:**
- Load Amazon Pay, Paytm with credit card
- Use for merchant payments (extra 1-2% cashback)
- Watch for reward caps and exclusions

**Multiple Cards Strategy:**
```
Online Shopping → SBI Cashback (5%)
Dining → HDFC Swiggy/Zomato (10%)
Travel → Axis Magnus/Atlas (10-25X)
Utilities → Axis Ace (2% + 10% extra)
General → HDFC Millennia (1%)
```

## 🏦 Bank-Specific Tips

### HDFC Bank
- **SmartBuy Portal**: 10X points on Amazon, Flipkart
- **Payzapp**: ₹3,000 cashback on new cards
- **Trick**: Use Diners Club variant for better acceptance abroad

### SBI Cards
- **SimplyCLICK**: 10X on partner merchants
- **Elite**: 1 reward point = ₹0.25
- **Trick**: Combine with SBI account for better milestone offers

### Axis Bank
- **Magnus/Reserve**: Transfer to airline partners at 5:4 ratio
- **Edge Rewards**: Use for Grab Deals marketplace
- **Trick**: Book via Axis Travel Edge for bonus accelerators

### ICICI Bank
- **Coral/Rubyx**: Book movie tickets monthly (₹300 value)
- **Amazon Pay**: 5% unlimited on Amazon
- **Trick**: Use ICICI Pockets for salary credit offers

### AMEX
- **Membership Rewards**: Transfer to Marriott (3:1), Vistara
- **Refer & Earn**: 10,000 points per referral (max 55K/year)
- **Trick**: Use Amex Offers for 10-30% extra savings

## 📡 Sources Monitored

"""
    
    for feed_name in FEEDS.keys():
        md_content += f"- **{feed_name.replace('_', ' ').title()}**: Credit card news and offers\n"
    
    md_content += f"""

---

*🤖 This report is automatically generated every 6 hours.*  
*📊 Includes: Latest offers, Devaluations, Reward optimization, Redemption strategies*  
*🇮🇳 Focused on Indian credit cards and banking ecosystem*  
*Repository: [Credit Card Optimizer](https://github.com/starkarthikr/credit-card-optimizer)*
"""
    
    with open('CREDIT_CARD_UPDATES.md', 'w', encoding='utf-8') as f:
        f.write(md_content)
    
    print(f"Generated report with {len(recent_articles)} recent articles")

def main():
    print("=" * 70)
    print("Credit Card Optimizer - India Edition")
    print("=" * 70)
    
    all_articles, recent_articles = process_feeds()
    
    save_json_report(all_articles, 'all_updates.json')
    save_json_report(recent_articles, 'recent_updates.json')
    
    generate_markdown_report(recent_articles)
    
    analyzed = sum(1 for a in recent_articles if a.get('card_info'))
    
    print("=" * 70)
    print(f"Total Articles: {len(all_articles)}")
    print(f"Recent Articles (7 days): {len(recent_articles)}")
    print(f"With Card Analysis: {analyzed}")
    print("=" * 70)

if __name__ == '__main__':
    main()
