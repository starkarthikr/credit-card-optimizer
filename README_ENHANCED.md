# Credit Card Optimizer 💳 - Enhanced Edition

## 🎉 **Major Enhancements Added - February 2026**

AI-powered credit card analysis with **advanced features** for personalized recommendations, portfolio optimization, and real-time data integration.

---

## 🚀 New Features Overview

### 1. **User Spending Profiles** 📁
Create personalized spending profiles for accurate recommendations.

**File:** `user_profile.py`

**Features:**
- Track spending across 10 categories
- Set preferences (max fee, reward type, lounge access)
- Store financial profile (income, age, occupation)
- Auto-generate AI prompts from your data
- Save/load profiles as JSON

**Usage:**
```python
from user_profile import SpendingProfile

# Create profile
profile = SpendingProfile("My Profile")
profile.set_spending('dining', 15000)
profile.set_spending('online_shopping', 25000)
profile.set_spending('travel', 20000)

# Set preferences
profile.preferences['max_annual_fee'] = 5000
profile.preferences['reward_type'] = 'cashback'

# Save profile
profile.save()  # Saves to profiles/my_profile.json

# Generate personalized prompt
prompt = profile.generate_analysis_prompt()
```

---

### 2. **Expense Importer** 📊
Import bank statements and expense tracker data automatically.

**File:** `expense_importer.py`

**Features:**
- Import CSV files from any source
- Parse common bank statement formats (HDFC, SBI, ICICI, Axis)
- Automatic transaction categorization
- Convert to spending profiles
- Support for multiple date/amount formats

**Usage:**
```python
from expense_importer import ExpenseImporter

# Import transactions
importer = ExpenseImporter()
transactions = importer.import_csv('bank_statement.csv')

# Auto-categorize
categorized = importer.categorize_transactions()

# Create profile from data
profile = importer.export_to_profile("Imported Profile", num_months=3)
profile.save()
```

**Supported Banks:**
- HDFC Bank
- State Bank of India (SBI)
- ICICI Bank
- Axis Bank
- Generic CSV format

---

### 3. **Structured Output Analyzer** 📝
Generate analysis with structured JSON + markdown output.

**File:** `structured_analyzer.py`

**Features:**
- JSON export for programmatic use
- Structured recommendations with ROI data
- Automatic comparison table extraction
- Dual output: JSON + Enhanced Markdown
- Parse card features from AI analysis

**Usage:**
```python
from structured_analyzer import StructuredAnalyzer
from user_profile import SpendingProfile

profile = SpendingProfile.load("My Profile")
analyzer = StructuredAnalyzer()

# Run analysis
result = analyzer.analyze_with_profile(profile)

# Save both formats
json_path, md_path = analyzer.save_both()
print(f"JSON: {json_path}")
print(f"Markdown: {md_path}")

# Access structured data
print(result['structured_recommendations'])
print(result['roi_calculations'])
```

**Output Structure:**
```json
{
  "timestamp": "2026-02-11T15:30:00",
  "profile_name": "User Profile",
  "model_used": "meta-llama/llama-3.2-3b-instruct:free",
  "spending_profile": {...},
  "raw_analysis": "...",
  "structured_recommendations": {
    "primary_card": {
      "name": "HDFC Infinia",
      "annual_fee": 12500,
      "reward_rate": 3.3
    },
    "supplementary_cards": [...]
  },
  "roi_calculations": {
    "total_annual_fees": 12500,
    "estimated_rewards": 45000,
    "net_value": 32500
  }
}
```

---

### 4. **Portfolio Optimizer** 🎯
Find optimal multi-card combinations for maximum rewards.

**File:** `portfolio_optimizer.py`

**Features:**
- Compare all card combinations (1-5 cards)
- Calculate optimal spending strategy per category
- Consider annual fee budgets
- Generate ROI analysis for each portfolio
- Pre-loaded with 8 popular Indian cards
- Customizable card database

**Usage:**
```python
from portfolio_optimizer import PortfolioOptimizer
from user_profile import SpendingProfile

profile = SpendingProfile.load("My Profile")
optimizer = PortfolioOptimizer()

# Find best portfolios
portfolios = optimizer.find_optimal_portfolio(
    profile, 
    max_cards=3, 
    max_total_fee=25000
)

# Generate report
report = optimizer.generate_report(profile, max_cards=3)
print(report)
```

**Pre-loaded Cards:**
1. HDFC Infinia
2. HDFC Diners Club Black
3. Axis Magnus
4. Axis Vistara Infinite
5. SBI Cashback
6. ICICI Amazon Pay
7. AMEX Platinum Travel
8. IndusInd Legend

**Example Output:**
```
### #1. HDFC Infinia + SBI Cashback

- Total Annual Fees: ₹13,499
- Total Annual Rewards: ₹58,750
- Net Value: ₹45,251
- ROI: 335.2%

Spending Strategy:
- Dining (₹15,000/month): HDFC Infinia
- Online Shopping (₹25,000/month): SBI Cashback
- Travel (₹20,000/month): HDFC Infinia
```

---

### 5. **Milestone Tracker** 🏆
Track progress toward bonus rewards and milestone benefits.

**File:** `milestone_tracker.py`

**Features:**
- Track spending milestones for multiple cards
- Calculate progress percentages
- Show days remaining to deadlines
- Visual progress bars
- Pre-configured with major card milestones

**Usage:**
```python
from milestone_tracker import MilestoneTracker

tracker = MilestoneTracker()

# Update spending
tracker.update_spend('HDFC Infinia', 250000)
tracker.update_spend('Axis Magnus', 75000)

# Check progress
progress = tracker.get_card_progress('HDFC Infinia')

# Generate report
report = tracker.generate_report()
tracker.save_report()
```

**Tracked Milestones:**
- **HDFC Infinia:** Quarterly bonus (₹4L), Annual bonus (₹8L), Fee waiver
- **Axis Magnus:** Monthly 10K edge reward, Annual 25K bonus
- **HDFC Diners Black:** Fee reversal, 10X rewards
- **SBI Cashback:** Annual fee waiver
- **Axis Vistara:** Silver/Gold tier status, Fee waiver

---

### 6. **Card Data Fetcher** 🔄
Fetch latest card information from multiple sources.

**File:** `card_data_fetcher.py`

**Features:**
- Fetch Reddit discussions from r/CreditCardsIndia
- Cache data to reduce API calls
- Aggregate card news
- Generate data summaries
- Configurable cache duration

**Usage:**
```python
from card_data_fetcher import CardDataFetcher

fetcher = CardDataFetcher()

# Fetch Reddit discussions
posts = fetcher.fetch_reddit_discussions(subreddit='CreditCardsIndia', limit=10)

# Get cached data
data = fetcher.get_cached_data('reddit_posts', max_age_hours=24)

# Generate summary
summary = fetcher.generate_data_summary()
```

---

## 📦 Complete File Structure

```
credit-card-optimizer/
├── main.py                      # Core AI engine (original)
├── run_analysis.py              # Ultimate guide generator
├── user_profile.py              # ✨ NEW: Spending profiles
├── expense_importer.py          # ✨ NEW: Import bank statements
├── structured_analyzer.py       # ✨ NEW: JSON + Markdown output
├── portfolio_optimizer.py       # ✨ NEW: Multi-card optimization
├── milestone_tracker.py         # ✨ NEW: Track reward milestones
├── card_data_fetcher.py         # ✨ NEW: Fetch latest card data
├── requirements.txt
├── README.md
├── README_ENHANCED.md           # This file
├── .github/workflows/
│   ├── card-optimizer.yml
│   ├── credit-card-monitor.yml
│   └── ultimate-guide.yml
├── profiles/                    # ✨ NEW: Saved user profiles
│   └── sample_user.json
├── recommendations/
│   ├── structured/              # ✨ NEW: JSON outputs
│   └── INDEX.md
└── cache/                       # ✨ NEW: Data cache
```

---

## 🚀 Quick Start Guide

### Installation

```bash
git clone https://github.com/starkarthikr/credit-card-optimizer
cd credit-card-optimizer
pip install -r requirements.txt
```

### Basic Workflow

#### Option 1: Quick Analysis (Original Method)
```bash
python main.py
```

#### Option 2: Import Your Expenses
```bash
# 1. Export bank statement as CSV
# 2. Import and analyze
python -c "
from expense_importer import ExpenseImporter
from structured_analyzer import StructuredAnalyzer

importer = ExpenseImporter()
importer.import_csv('bank_statement.csv')
profile = importer.export_to_profile('My Profile', num_months=3)
profile.save()

analyzer = StructuredAnalyzer()
result = analyzer.analyze_with_profile(profile)
analyzer.save_both()
"
```

#### Option 3: Create Custom Profile
```python
from user_profile import SpendingProfile
from structured_analyzer import StructuredAnalyzer

# Create profile
profile = SpendingProfile("My Profile")
profile.set_spending('dining', 15000)
profile.set_spending('online_shopping', 25000)
profile.set_spending('groceries', 12000)
profile.set_spending('travel', 20000)

profile.preferences['max_annual_fee'] = 10000
profile.preferences['reward_type'] = 'points'
profile.save()

# Get AI recommendations
analyzer = StructuredAnalyzer()
result = analyzer.analyze_with_profile(profile)
json_path, md_path = analyzer.save_both()

print(f"Analysis saved:")
print(f"  JSON: {json_path}")
print(f"  Markdown: {md_path}")
```

#### Option 4: Optimize Multi-Card Portfolio
```python
from user_profile import SpendingProfile
from portfolio_optimizer import PortfolioOptimizer

profile = SpendingProfile.load("My Profile")
optimizer = PortfolioOptimizer()

report = optimizer.generate_report(profile, max_cards=3)
print(report)
```

#### Option 5: Track Milestones
```python
from milestone_tracker import MilestoneTracker

tracker = MilestoneTracker()
tracker.update_spend('HDFC Infinia', 250000)  # ₹2.5L spent
tracker.update_spend('SBI Cashback', 150000)  # ₹1.5L spent

tracker.save_report()
```

---

## 📊 Advanced Use Cases

### 1. Complete Personal Finance Analysis

```python
#!/usr/bin/env python3
"""Complete credit card analysis workflow"""

from expense_importer import ExpenseImporter
from structured_analyzer import StructuredAnalyzer
from portfolio_optimizer import PortfolioOptimizer
from milestone_tracker import MilestoneTracker

# Step 1: Import your expenses
print("Step 1: Importing expenses...")
importer = ExpenseImporter()
importer.import_csv('january_statement.csv')
importer.import_csv('february_statement.csv')
importer.categorize_transactions()

# Step 2: Create spending profile
print("Step 2: Creating profile...")
profile = importer.export_to_profile("Q1 2026 Profile", num_months=2)
profile.preferences['max_annual_fee'] = 15000
profile.preferences['lounge_access_required'] = True
profile.save()

# Step 3: Get AI recommendations
print("Step 3: Getting AI recommendations...")
analyzer = StructuredAnalyzer()
result = analyzer.analyze_with_profile(profile)
analyzer.save_both()

# Step 4: Find optimal portfolio
print("Step 4: Optimizing portfolio...")
optimizer = PortfolioOptimizer()
report = optimizer.generate_report(profile, max_cards=3)
print(report)

# Step 5: Track milestones
print("Step 5: Setting up milestone tracking...")
tracker = MilestoneTracker()
# Add your current cards and spending
tracker.save_report()

print("\n✅ Complete analysis done! Check recommendations/ folder.")
```

### 2. Compare Specific Cards

```python
from structured_analyzer import StructuredAnalyzer

analyzer = StructuredAnalyzer()

cards = [
    "HDFC Infinia",
    "Axis Magnus",
    "AMEX Platinum Travel",
    "HDFC Diners Club Black"
]

result = analyzer.analyze_cards(
    cards=cards,
    spending_amount=100000  # ₹1L/month
)

analyzer.save_both()
print(result['comparison_table'])
```

### 3. Monthly Spending Review

```python
from expense_importer import ExpenseImporter
from milestone_tracker import MilestoneTracker

# Import this month's transactions
importer = ExpenseImporter()
importer.import_csv('march_2026_statement.csv')
monthly_summary = importer.get_monthly_summary(month=3, year=2026)

print("March 2026 Spending:")
for category, amount in monthly_summary.items():
    if amount > 0:
        print(f"  {category}: ₹{amount:,.0f}")

# Update milestone tracker
tracker = MilestoneTracker()
for category, amount in monthly_summary.items():
    tracker.update_spend('HDFC Infinia', amount)  # Update for your card

tracker.save_report()
```

---

## 🔧 Integration Ideas

### 1. **Automate with Cron**
```bash
# Add to crontab for monthly analysis
0 1 1 * * cd /path/to/credit-card-optimizer && python monthly_review.py
```

### 2. **Telegram Bot Integration**
```python
import telebot
from structured_analyzer import StructuredAnalyzer

bot = telebot.TeleBot("YOUR_TOKEN")

@bot.message_handler(commands=['analyze'])
def analyze_cards(message):
    # Get user spending from message
    # Run analysis
    # Send results back
    pass
```

### 3. **Web Dashboard**
```python
from flask import Flask, render_template
from portfolio_optimizer import PortfolioOptimizer

app = Flask(__name__)

@app.route('/optimize', methods=['POST'])
def optimize():
    # Get spending data from form
    # Run optimizer
    # Return visualization
    pass
```

### 4. **Google Sheets Integration**
```python
import gspread
from expense_importer import ExpenseImporter

# Export spending data to Google Sheets
# Update automatically with cron
```

---

## 📊 Output Formats

### JSON Output Structure
```json
{
  "timestamp": "2026-02-11T15:30:00",
  "profile_name": "User Profile",
  "spending_profile": {
    "monthly_spend": {
      "dining": 15000,
      "online_shopping": 25000,
      "travel": 20000
    },
    "preferences": {
      "max_annual_fee": 10000,
      "reward_type": "cashback"
    }
  },
  "structured_recommendations": {
    "primary_card": {
      "name": "HDFC Infinia",
      "annual_fee": 12500,
      "reward_rate": 3.3
    }
  },
  "roi_calculations": {
    "total_annual_fees": 12500,
    "estimated_rewards": 45000,
    "net_value": 32500,
    "breakeven_spend": 378787
  }
}
```

### Markdown Tables

All comparison outputs include properly formatted markdown tables:

```markdown
| Card | Annual Fee | Reward Rate | Lounge Access | Best For |
|------|------------|-------------|---------------|----------|
| HDFC Infinia | ₹12,500 | 3.3% | 12/quarter | Premium travel |
| Axis Magnus | ₹12,500 | 2.4% | 8/quarter | Reward points |
| SBI Cashback | ₹999 | 5% | 0 | Online shopping |
```

---

## 🧑‍💻 Developer Guide

### Adding New Cards to Portfolio Optimizer

```python
# Edit portfolio_optimizer.py

def _load_indian_cards(self):
    cards = []
    
    # Add your card
    my_card = CardData("My Custom Card", "Bank Name", 5000)
    my_card.category_rewards = {
        'dining': 2.0,
        'travel': 3.0,
        'online_shopping': 2.5,
        # ... other categories
    }
    my_card.reward_type = 'cashback'  # or 'points'
    my_card.point_value = 0.25  # if points
    cards.append(my_card)
    
    return cards
```

### Custom Category Mapping

```python
# Edit expense_importer.py

CATEGORY_KEYWORDS = {
    'dining': ['your', 'custom', 'keywords'],
    'custom_category': ['keyword1', 'keyword2']
}
```

### Custom AI Prompts

```python
# Edit user_profile.py - generate_analysis_prompt() method

def generate_analysis_prompt(self) -> str:
    prompt = "Your custom prompt structure"
    # Add your requirements
    return prompt
```

---

## ✨ Benefits of Enhanced Features

| Feature | Before | After |
|---------|--------|-------|
| **Accuracy** | Generic recommendations | Personalized to your spending |
| **Data Entry** | Manual | Import CSV automatically |
| **Output** | Text only | JSON + Markdown + Tables |
| **Cards** | Single card | Optimal 2-3 card portfolio |
| **Tracking** | None | Milestone progress tracking |
| **Updates** | Manual check | Auto-fetch from Reddit |
| **ROI** | Estimated | Exact calculations |
| **Usability** | CLI only | Programmable API |

---

## 📝 Examples

All examples are in the repository:

- `user_profile.py` - Run to see profile system demo
- `expense_importer.py` - Generates sample CSV and imports it
- `structured_analyzer.py` - Full analysis with JSON export
- `portfolio_optimizer.py` - Find best card combinations
- `milestone_tracker.py` - Track milestone progress
- `card_data_fetcher.py` - Fetch latest discussions

---

## 🔐 Security

All new features maintain the same security standards:

- ✅ No API keys in code
- ✅ Local data storage
- ✅ No sensitive data transmitted
- ✅ Input validation
- ✅ Safe file operations

---

## 🛣️ Roadmap

- [ ] Web dashboard (Flask/Streamlit)
- [ ] Mobile app export
- [ ] Real-time bank API integration
- [ ] Machine learning spend prediction
- [ ] Multi-currency support
- [ ] Family account aggregation
- [ ] Credit score impact analysis
- [ ] Tax benefit calculator

---

## 👥 Contributing

Contributions welcome! Priority areas:

1. Add more Indian credit cards to database
2. Improve expense categorization keywords
3. Add bank statement parsers
4. Create visualization dashboards
5. Build API integrations

---

## 💬 Support

- **Issues:** [GitHub Issues](https://github.com/starkarthikr/credit-card-optimizer/issues)
- **Discussions:** [r/CreditCardsIndia](https://reddit.com/r/CreditCardsIndia)
- **Email:** starkarthikr@gmail.com

---

## 🌟 Acknowledgments

- OpenRouter AI for free AI models
- r/CreditCardsIndia community
- All contributors

---

**🚀 Upgrade from basic analysis to complete credit card optimization system!**

*Last Updated: February 11, 2026*
