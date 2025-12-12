#!/usr/bin/env python3
import requests
import os
from datetime import datetime

# OpenRouter API configuration
API_URL = "https://openrouter.ai/api/v1/chat/completions"
API_KEY = "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"

print("=" * 100)
print("💳 COMPREHENSIVE CREDIT CARD REWARD MAXIMIZATION ANALYSIS 💳")
print("=" * 100)
print()

# The ultimate credit card analysis prompt
prompt = """Create the ULTIMATE comprehensive credit card reward maximization guide for India in 2025. Include:

## PART 1: TOP CARDS DEEP ANALYSIS
Analyze these top Indian credit cards with DETAILED breakdowns:
1. HDFC Infinia - Metal edition benefits, reward rates, annual value calculation
2. Axis Magnus (post devaluation) - Current benefits, workarounds, optimal usage
3. AMEX Platinum Travel - Membership Rewards transfer partners, best redemptions
4. HDFC Diners Club Black - Priority Pass, Golf, exclusive benefits
5. SBI Cashback - 5% online shopping, caps, restrictions
6. ICICI Amazon Pay - Cashback rates, Amazon vs non-Amazon
7. Axis Vistara Infinite - CV points, tier benefits, flight value
8. IndusInd Legend - Reward points, redemption options

For EACH card include:
- Annual fee and fee waiver criteria
- Base reward rate (% or points per ₹100)
- Accelerated categories and rates
- Annual caps and monthly limits
- Milestone benefits and spend requirements
- Lounge access (domestic/international counts)
- Complimentary benefits (insurance, concierge, golf)
- Best use cases and spend categories
- Breakeven spend calculation
- Total annual value estimate for ₹10L, ₹20L, ₹50L spend

## PART 2: REWARD MAXIMIZATION HACKS

### Earning Hacks:
1. **Multi-card strategy** - Which cards to combine for different categories
2. **Milestone gaming** - How to hit milestones efficiently
3. **Manufactured spending** - Legal ways to increase spend (rent, insurance prepay, gift cards)
4. **Accelerated merchant codes** - Which MCCs give bonus rewards
5. **Referral bonuses** - Friend referral reward stacking
6. **Welcome offers** - Timing card applications for maximum bonuses
7. **Upgrade path** - Moving from entry to premium cards strategically
8. **Add-on cards** - Using family cards for combined milestones

### Redemption Hacks:
1. **Transfer partners** - Best value transfer ratios (AMEX MR, Axis Edge, etc.)
2. **Flight bookings** - Maximizing airline miles value (domestic: ₹0.5-1, international: ₹1-3 per point)
3. **Hotel bookings** - ITC, Taj, Marriott transfer sweet spots
4. **Statement credit vs points** - When to redeem which way
5. **Gift vouchers** - Best value vouchers (Amazon, Flipkart, dining)
6. **Shopping portals** - Stacking rewards on brand websites
7. **Accelerated redemption windows** - Bonus point redemption periods
8. **Point pooling** - Combining points across cards

### Advanced Hacks:
1. **Forex markup optimization** - Zero markup cards for international spend
2. **Wallet loading** - Which wallets credit as purchases (Amazon Pay, PayZapp)
3. **UPI credit cards** - Using RuPay credit on UPI for rewards
4. **EMI conversion** - Interest-free EMI without losing rewards
5. **Insurance stacking** - Combining travel insurance from multiple cards
6. **Lounge access gaming** - Multiple same-day entries across cards
7. **Golf privileges** - Free rounds across premium cards
8. **Airport transfers** - Complimentary chauffeur services

## PART 3: CATEGORY-WISE BEST CARDS

### Travel & Aviation:
- International flights
- Domestic flights
- Hotels
- Forex transactions
- Airport lounge
- Travel insurance

### Daily Spending:
- Online shopping
- Groceries
- Dining/restaurants
- Fuel
- Utilities
- Insurance

### Premium Categories:
- Luxury shopping
- Fine dining
- Golf
- Concierge services

## PART 4: PORTFOLIO STRATEGIES

Create optimal 2-card, 3-card, and 5-card portfolios for:
1. **Budget conscious** (₹0-5,000 total annual fees)
2. **Mid-tier** (₹5,000-20,000 total annual fees)
3. **Premium** (₹20,000-50,000 total annual fees)
4. **Ultra-premium** (₹50,000+ total annual fees)

For each portfolio include:
- Total annual fees
- Combined annual benefits value
- Spend distribution strategy
- Expected annual rewards
- Breakeven spend required
- Net annual value

## PART 5: PITFALLS TO AVOID

1. **Fee traps** - Cards with fees higher than benefits
2. **Devaluation risks** - Recent program changes (Magnus, etc.)
3. **Exclusion merchants** - Where rewards don't apply
4. **Expiry deadlines** - Point validity periods
5. **Hidden charges** - Processing fees, GST, etc.
6. **Over-spending** - Chasing rewards beyond needs

## PART 6: 2025 TRENDS & PREDICTIONS

- Upcoming card launches
- Expected devaluations
- RuPay credit on UPI expansion
- AI-powered spending insights
- Co-branded card opportunities

## PART 7: EXPERT TIPS

1. **Tax optimization** - How rewards affect taxation
2. **Credit score impact** - Multiple card strategy
3. **Credit utilization** - Optimal usage ratios
4. **Payment timing** - Statement date vs due date strategies
5. **CIBIL management** - Applying for multiple cards smartly

Provide SPECIFIC numbers, REAL examples, EXACT calculations, and ACTIONABLE strategies. Make it comprehensive enough to be a complete guide worth ₹10,000+ in consulting value!"""

print("🔄 Generating comprehensive analysis...")
print("📊 This is a DEEP analysis with 2000+ words of actionable insights...")
print()

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
    "HTTP-Referer": "https://github.com/starkarthikr/credit-card-optimizer",
    "X-Title": "Credit Card Optimizer - Ultimate Guide"
}

payload = {
    "model": "meta-llama/llama-3.2-3b-instruct:free",
    "messages": [{"role": "user", "content": prompt}],
    "temperature": 0.7,
    "max_tokens": 4000  # Maximum for comprehensive response
}

try:
    response = requests.post(API_URL, json=payload, headers=headers, timeout=120)
    
    if response.status_code == 200:
        data = response.json()
        content = data["choices"][0]["message"]["content"]
        
        # Save to file
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"recommendations/{timestamp}-ULTIMATE-REWARD-GUIDE.md"
        
        os.makedirs("recommendations", exist_ok=True)
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(f"""# 💳 ULTIMATE CREDIT CARD REWARD MAXIMIZATION GUIDE

**Generated:** {datetime.now().strftime("%B %d, %Y at %I:%M %p IST")}
**Comprehensive Analysis:** 2000+ words of expert strategies
**Value:** ₹10,000+ consulting equivalent

---

{content}

---

## 🎯 Quick Action Steps

1. **Audit your current cards** - Calculate actual rewards earned vs fees paid
2. **Identify gaps** - Which spending categories are not optimized
3. **Plan applications** - Apply for cards strategically (3-6 months apart)
4. **Set milestones** - Track spend requirements for bonus rewards
5. **Review quarterly** - Adjust strategy based on devaluations/new launches

## 📱 Useful Resources

- [CardExpert](https://cardexpert.in) - Indian credit card database
- [r/CreditCardsIndia](https://reddit.com/r/CreditCardsIndia) - Community discussions  
- [TechnoFino](https://technofino.in) - Card reviews and tips
- [Reward Calculators](https://rewardcalculator.in) - Value calculations

---

*Generated by [Credit Card Optimizer](https://github.com/starkarthikr/credit-card-optimizer)*  
*Powered by OpenRouter AI - 100% FREE*
""")
        
        print("✅ SUCCESS! Comprehensive analysis generated!")
        print()
        print("=" * 100)
        print("📄 SAVED TO:", filename)
        print("=" * 100)
        print()
        print("📊 PREVIEW:")
        print("=" * 100)
        print(content[:2000])  # Show first 2000 characters
        print("...")
        print(f"\n[Full analysis: {len(content)} characters]")
        print("=" * 100)
        print()
        print("🎉 Complete guide saved! Check the file for full analysis.")
        
    elif response.status_code == 429:
        print("⚠️ Rate limited. Trying backup model...")
        payload["model"] = "google/gemma-2-9b-it:free"
        response = requests.post(API_URL, json=payload, headers=headers, timeout=120)
        if response.status_code == 200:
            data = response.json()
            content = data["choices"][0]["message"]["content"]
            print("✅ Generated with backup model!")
            print(content[:1000])
        else:
            print(f"❌ Error: {response.status_code}")
            print(response.text)
    else:
        print(f"❌ Error: {response.status_code}")
        print(response.text)
        
except Exception as e:
    print(f"❌ Exception: {e}")

print()
print("=" * 100)
print("💡 TIP: Run this weekly to stay updated on latest card changes!")
print("=" * 100)
