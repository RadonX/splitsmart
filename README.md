# SplitSmart >à=°

**Your AI Travel Expense Manager - Just Talk, We'll Handle the Math**

Turn your messy receipts and confusing bank statements into perfectly organized Splitwise expenses. SplitSmart understands natural language and does all the heavy lifting automatically.

## <¯ Perfect For

- **Group Travelers** - Friends planning trips together
- **Family Vacations** - Parents managing complex family expenses  
- **Business Trips** - Colleagues sharing work travel costs
- **Event Organizers** - Anyone coordinating group expenses

## ( What Makes SplitSmart Special

### =ã Natural Conversation
```
You: "I paid $47 for dinner at Mario's, split it between me, John, and Sarah"
SplitSmart: "Got it! I'll add a $47 dinner expense, split 3 ways ($15.67 each). 
95% confidence - submitting to Splitwise now!"
```

### <æ Bank Statement Magic
Upload your bank statement and watch SplitSmart:
- Filter transactions to your trip dates automatically
- Identify expense candidates (restaurants, hotels, gas)
- Ask smart clarifying questions
- Match receipts to bank charges

### <¯ Confidence-Based Processing
- **95%+ confidence** ’ Auto-submit to Splitwise
- **70-94% confidence** ’ Stage for your review
- **<70% confidence** ’ Ask for confirmation
- Never guess with your money!

### >à Context-Aware Intelligence
Tell SplitSmart about your trip once:
- Trip dates and travelers
- Splitwise group to use
- Then everything becomes smarter and more accurate

## =€ Quick Start

### 1. Setup (One Time)
```bash
# Clone and setup
git clone https://github.com/your-username/splitsmart
cd splitsmart
uv init && uv add requests python-dotenv

# Get Splitwise API credentials at https://secure.splitwise.com/apps
cp .env.example .env
# Fill in your API keys in .env

# Test connection
uv run python tools/splitwise_client.py
```

### 2. Start a Session
```
You: "Let's process expenses for our Montreal trip"
SplitSmart: "Great! What were the trip dates and who went?"
You: "January 15-18, 2024. Me, John, Mary, and Bob."
SplitSmart: "Perfect! Which Splitwise group should I use?"
You: "https://secure.splitwise.com/#/groups/83515836"
SplitSmart: "All set! Ready to process Montreal expenses for 4 travelers."
```

### 3. Process Expenses

**Upload Bank Statement:**
```
You: [Upload bank statement PDF]
SplitSmart: "Found 23 transactions, 12 within trip dates. 
I see $47.83 at Mario's Pizza, $240 at Marriott Hotel, $65 at Shell Gas.
Should I process all restaurant, hotel, and gas charges?"
```

**Add Individual Expenses:**
```
You: "John paid $60 for gas, split between just me and him"
SplitSmart: "Adding $60 gas expense paid by John, split equally 
between you and John ($30 each). 98% confidence - submitting!"
```

**Receipt Processing:**
```
You: [Upload receipt photo]
SplitSmart: "I see this is a $47.83 receipt from Mario's Pizza. 
Large pizza $18.99, salads $12.00, drinks $8.50, tax $8.34.
Should everyone split everything equally?"
```

## =' Advanced Features

### Staging Area
- Review expenses before they hit Splitwise
- Edit amounts, participants, or descriptions
- Batch submit when you're confident
- Commands: `show staged`, `submit ready`, `edit expense`

### Smart Matching
- Automatically match receipts to bank statement charges
- Handle multiple receipts in one photo
- Filter out ATM withdrawals and personal charges
- Validate expense amounts and participants

### Error Prevention
- Catch math errors before Splitwise submission
- Validate group membership
- Handle currency conversions
- Prevent duplicate expenses

## <¨ Example Workflows

### Scenario: Weekend Ski Trip
```
SplitSmart: "What trip are we processing?"
You: "Ski weekend in Vermont, Dec 10-12, with Alex, Jamie, and me"
You: [Upload bank statement]
SplitSmart: "Found 8 relevant charges: 
- $320 Airbnb (Dec 10)
- $95 grocery store (Dec 10) 
- $180 ski rental (Dec 11)
- $67 dinner (Dec 11)
Should I split these equally among all 3 people?"
You: "Yes, but the ski rental should exclude me - I brought my own"
SplitSmart: "Got it! Updating ski rental to split between Alex and Jamie only.
Ready to submit 4 expenses totaling $662. Proceed?"
```

### Scenario: Business Dinner
```
You: "Add expense: I paid $180 for team dinner at The Steakhouse"
SplitSmart: "Who should split this expense?"
You: "Me, Sarah from marketing, and the two developers"
SplitSmart: "I need to match names to your Splitwise group. 
Is 'Sarah from marketing' Sarah Johnson (user ID 12345)?"
You: "Yes, and the developers are Mike and Lisa"
SplitSmart: "Perfect! $180 dinner split 4 ways ($45 each). 
Creating expense now!"
```

## = Privacy & Security

- **API keys** stored locally in `.env` (never committed to git)
- **No data collection** - everything stays on your machine
- **Splitwise integration** - your expenses go directly to your account
- **Open source** - inspect the code yourself

## > Contributing

SplitSmart is built with Claude Code and welcomes contributions!

- **Memory Bank Architecture** - AI context persistence system
- **Confidence Scoring** - Smart automation with human oversight
- **Natural Language Processing** - Conversation-driven interface

See `docs/memory_bank/README.md` for architecture details.

## <˜ Troubleshooting

**"Authentication failed"**
- Check your `.env` file has valid Splitwise API credentials
- Test with: `uv run python tools/splitwise_client.py`

**"Can't find group members"**
- Verify Splitwise group URL is correct
- Make sure all travelers are in the Splitwise group

**"Expenses not submitting"**
- Check `show staged` to see pending expenses
- Use `submit ready` to submit high-confidence expenses
- Review low-confidence expenses with `review low confidence`

**"Bank statement not parsing"**
- Ensure PDF is readable (not image-based)
- Try uploading CSV export instead
- Check trip dates match statement date range

## =Ý License

MIT License - Use freely for personal and commercial projects!

---

**Ready to never split expenses manually again?** 

Start with `git clone` and tell SplitSmart about your next trip! <¿÷<Ô