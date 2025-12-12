# Credit Card Optimizer 💳

AI-powered credit card analysis, comparison, and optimization tool using **100% FREE** OpenRouter AI models. Get personalized recommendations, reward maximization strategies, and comprehensive card comparisons tailored to your spending patterns.

## 🚀 Features

- **Card Comparisons** - Side-by-side analysis of multiple credit cards
- **Reward Optimization** - Maximize cashback, points, and miles
- **Annual Fee Analysis** - Fee vs benefits breakeven calculations
- **Category Optimization** - Best cards for travel, dining, shopping, etc.
- **Milestone Tracking** - Benefit unlock strategies
- **Devaluation Alerts** - Track reward program changes
- **New Card Reviews** - Latest card launches and features
- **100% FREE AI Models** - No API costs, unlimited analysis
- **Automated Scheduling** - Weekly optimization reports
- **Smart Retry Logic** - Auto-fallback across 5 AI models

## 📁 Repository Structure

```
credit-card-optimizer/
├── main.py                          # AI-powered card analysis engine
├── .github/workflows/
│   └── card-optimizer.yml           # Automated workflow
├── recommendations/                 # Generated analyses
│   ├── INDEX.md                     # Chronological index
│   └── YYYY-MM-DD_HH-MM-SS-card-analysis.md
└── README.md                        # This file
```

## 🔧 Quick Start

### Run Locally

```bash
# Clone the repository
git clone https://github.com/starkarthikr/credit-card-optimizer
cd credit-card-optimizer

# Install dependencies
pip install requests

# Run card analysis
python main.py
```

### Run via GitHub Actions

1. Go to **Actions** tab
2. Select **"Credit Card Optimizer"**
3. Click **"Run workflow"**
4. Choose your analysis type or enter custom query
5. Click **"Run workflow"**

## 💡 Example Queries

### Travel Cards Comparison
```
Compare the top 5 Indian credit cards for international travel in 2025, analyzing forex markup, lounge access, travel insurance, reward rates on foreign spends, and annual fee justification
```

### Cashback Analysis
```
Analyze the best cashback credit cards in India across different spending categories, including base cashback rates, accelerated categories, monthly caps, and annual value calculations for ₹50,000 monthly spend
```

### Premium Cards Evaluation
```
Evaluate ultra-premium credit cards (₹10,000+ annual fee) comparing lifestyle benefits, concierge services, golf privileges, reward value, and breakeven spend requirements
```

### Category Optimization
```
Create an optimal credit card portfolio strategy for maximizing rewards across dining (30%), groceries (25%), fuel (15%), online shopping (20%), and utilities (10%) spending distribution
```

### Reward Redemption
```
Compare reward redemption options across major credit card programs including transfer partners, flight bookings, hotel stays, shopping vouchers, and statement credits with value-per-point analysis
```

### Fee Analysis
```
Analyze whether upgrading from a free credit card to a ₹5000 annual fee card is worth it based on ₹1L monthly spending across travel, dining, and online shopping categories
```

## 🤖 Available AI Models

All models are **100% FREE** on OpenRouter:

| Model | Best For | Speed | Quality |
|-------|----------|-------|----------|
| **Llama 3.2 3B** | Quick comparisons | ⚡⚡⚡ Fast | ⭐⭐⭐ Good |
| **Gemma 2 9B** | Reward analysis | ⚡⚡ Medium | ⭐⭐⭐⭐ Great |
| **Qwen 2.5 7B** | Financial calculations | ⚡⚡ Medium | ⭐⭐⭐⭐ Great |
| **Mistral 7B** | Detailed advice | ⚡⚡ Medium | ⭐⭐⭐⭐ Great |
| **Phi-3 Mini** | Comprehensive reports | ⚡ Slower | ⭐⭐⭐ Good |

## 💳 Analysis Format

Each generated report includes:

- **Timestamp** - Date and time of analysis
- **AI Model Used** - Which model generated the recommendations
- **Query** - Original question or comparison request
- **Recommendations** - Detailed card analysis and suggestions
- **Metadata** - Source attribution

## ⏰ Automated Scheduling

- **Weekly Reports:** Runs automatically **every Monday at 6:30 AM IST** (01:00 UTC)
- **Manual Trigger:** Run anytime via GitHub Actions
- **Smart Retry:** Automatically tries 5 models if one is rate-limited
- **Auto-Commit:** Analyses automatically saved to repository

## 📊 View Recommendations

### Browse on GitHub
1. Navigate to [`recommendations/`](./recommendations) folder
2. Check [`recommendations/INDEX.md`](./recommendations/INDEX.md) for chronological list
3. Click any report to view full analysis

### Clone and Read Locally
```bash
git pull origin main
cd recommendations
ls -lt  # View newest reports first
cat 2025-12-13_01-00-00-card-analysis.md
```

## 🎯 Use Cases

- **Personal Finance** - Optimize your credit card portfolio
- **Travel Hackers** - Maximize miles and points earning
- **Cashback Seekers** - Find best cashback cards for your spend
- **Premium Card Users** - Justify annual fees with benefit analysis
- **Financial Bloggers** - Generate card comparison content
- **Card Enthusiasts** - Stay updated on card features and changes

## 🔥 Advanced Usage

### Custom Spending Profiles

```python
# Example: Specific spending pattern
prompt = "Recommend the best credit card combination for: Travel (₹40K/month), Dining (₹25K/month), Online Shopping (₹20K/month), Groceries (₹15K/month). Include primary and supplementary card strategy."

# Example: First credit card
prompt = "Recommend the best first credit card for a salaried professional with ₹8L annual income, focusing on no annual fee, good reward rate, and wide acceptance"

# Example: Card upgrade decision
prompt = "Should I upgrade from HDFC Regalia to Infinia? Analyze benefits difference, incremental fee, breakeven spend, and value proposition for ₹2L monthly spend"
```

### Integration Ideas

- **Expense Tracker Integration** - Auto-suggest best cards based on actual spending
- **Reward Calculator** - Build calculator based on AI analysis
- **Telegram Bot** - Get card recommendations on messaging apps
- **Newsletter** - Weekly card tips and devaluation alerts
- **Comparison Website** - Generate comparison content automatically

## 🇮🇳 Indian Credit Card Focus

Optimized for **Indian credit card ecosystem** including:

- **Major Banks:** HDFC, SBI, ICICI, Axis, AMEX, IndusInd, Yes Bank, Kotak
- **Card Networks:** Visa, Mastercard, RuPay, American Express
- **Popular Cards:** Infinia, Magnus, Regalia, Vistara, Emeralde, etc.
- **Indian Categories:** UPI payments, fuel surcharge, railway bookings
- **Local Benefits:** Airport lounge access, movie tickets, dining discounts

## ⚠️ Disclaimer

This tool provides AI-generated credit card recommendations. Always:

- **Verify details** from official bank websites and terms & conditions
- **Check current offers** as benefits and fees change frequently
- **Calculate your own** spend patterns and breakeven points
- **Read fine print** for exclusions, caps, and restrictions
- **Consider your needs** - AI suggestions are general, personalize them

Credit card features, fees, and rewards are subject to change by issuers.

## 🔗 Resources

- [OpenRouter AI](https://openrouter.ai) - Free AI API provider
- [CardExpert](https://cardexpert.in) - Indian credit card database
- [OneCard Blog](https://getonecard.app/blog) - Card guides and tips
- [r/CreditCardsIndia](https://reddit.com/r/CreditCardsIndia) - Community discussions
- [Paisabazaar](https://paisabazaar.com) - Card comparison portal

## 🤝 Contributing

Contributions welcome! Ideas:

- Add more analysis templates
- Create spending category calculators
- Build reward redemption guides
- Add card-specific deep dives
- Integrate with expense tracking APIs

## 📜 License

MIT License - Free to use and modify

---

**💳 Optimize Smart. Save More. Earn Maximum Rewards.**

*Powered by [OpenRouter AI](https://openrouter.ai) - 100% FREE Credit Card Intelligence*
