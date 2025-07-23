# SplitSmart 🌎

**AI-Powered Travel Expense Manager - Turn Bank Statements into Splitwise Expenses**

Convert messy bank statements and trip receipts into perfectly organized Splitwise expenses through natural conversation. SplitSmart understands your travel context and handles all the tedious expense splitting automatically.

## 🎯 Perfect For

- **Group Travelers** - Friends splitting vacation costs
- **Family Trips** - Parents managing dependent expenses
- **Business Travel** - Colleagues sharing work trip costs  
- **Event Organizers** - Anyone coordinating group expenses

## ⚡ Core Features

### 🗣️ Natural Conversation Interface
Set up your trip context through conversation:
- Trip dates, destination, and travelers
- Splitwise group connection
- Special splitting rules (dependents, custom ratios)

### 🎛️ Menu-Driven Expense Review
Streamlined transaction processing with quick decisions:
- One-by-one expense presentation with clear details
- Single-character responses ("y", "n", "1", "2") for speed
- Batch processing after all decisions are made
- Visual confirmations with checkmarks and summaries

### 📊 Multi-Source Expense Processing
- **Bank Statements** - CSV/PDF processing with date filtering
- **Individual Receipts** - PDF text extraction and itemized splitting
- **Receipt Photos** - Multi-receipt identification and processing
- **Manual Entry** - Natural language expense creation

### 🧠 Persistent Memory Bank
- **Trip Context** - Maintains session state across conversations
- **Group Matching** - Maps travelers to Splitwise members
- **Conversation Progress** - Tracks session progress and decisions made
- **Expense History** - Tracks created expenses and patterns
- **API Integration** - Splitwise authentication and error handling

### 🎯 Confidence-Based Staging
- **High Confidence (≥95%)** - Auto-submit to Splitwise
- **Medium Confidence (70-94%)** - Stage for review
- **Low Confidence (<70%)** - Request user approval

## 🚀 Quick Start

### 1. Setup
```bash
git clone https://github.com/your-username/splitsmart
cd splitsmart
uv install

# Configure Splitwise API credentials
cp .env.example .env
# Fill in your API keys from https://secure.splitwise.com/apps

# Test connection
uv run python tools/splitwise_client.py
```

### 2. Start with Claude Code
```
You: "guide me"
SplitSmart: [Reads memory bank, presents trip setup options]

You: [Provide trip details and Splitwise group]
SplitSmart: [Sets up context, matches travelers to group members]

You: [Upload bank statements/receipts or manual entry]
SplitSmart: [Menu-driven review: "Transaction #1: $575.87 Airbnb - Split equally?"]

You: "y" [Quick single-character responses]
SplitSmart: [✅ Approved, continues to next transaction]

You: "yes" [After reviewing all transactions]
SplitSmart: [Batch creates all approved expenses with proper dates]
```

## 🏗️ Architecture

### Memory Bank System
SplitSmart uses a persistent memory architecture to maintain context:

- **`active-session.md`** - Trip context, group info, authentication status
- **`expense-progress.md`** - Documents processed, expenses created, user decisions
- **`splitwise-api.md`** - API integration patterns and authentication
- **`conversation-parser.md`** - Natural language and menu-driven parsing rules
- **`workflow-patterns.md`** - Bank-statement-first and menu-driven processing workflows

### Workflow Types
1. **Menu-Driven Review** - Streamlined one-by-one expense decisions
2. **Bank-Statement-First** - Primary workflow for comprehensive expense capture
3. **Receipt Processing** - Detailed itemized expense handling
4. **Multi-Receipt Photos** - Batch processing of receipt collections
5. **Manual Entry** - Conversational expense creation

## 🔧 Key Capabilities

### Smart Expense Parsing
- Date-aware transaction filtering
- Merchant and category identification
- Amount validation and split calculation
- Currency handling and conversion

### Flexible Splitting Methods
- Equal splits with proper rounding
- Custom ratios and proportional splits
- Participant selection per expense
- Dependent expense handling

### Error Prevention
- API response validation
- Amount reconciliation
- Duplicate expense detection
- Group membership verification

## 🔒 Privacy & Security

- **Local Processing** - All data stays on your machine
- **Direct API Integration** - Expenses go straight to your Splitwise
- **No Data Collection** - Zero external tracking or storage
- **Open Source** - Full code transparency

## 📖 Memory Bank Commands

The memory bank enables SplitSmart to understand context:

- `"follow your custom instructions"` - Read memory bank and start
- `"set group [name]"` - Switch Splitwise groups
- `"show balances"` - Fetch current group balances
- `"upload receipt"` - Process PDF receipts
- `"upload bank statement"` - Process statements for multiple expenses

## 📋 Real Example

Check out the `mexico_trip` branch for a complete working example:
- Processing $1,050+ in Mexico trip expenses from bank statements
- Both equal splits and custom 2:1 ratios demonstrated  
- Full conversation transcript in `docs/conversation.txt`
- Updated memory bank showing all 7 created expenses

```bash
git checkout mexico_trip
```

## 🛠️ Development

Built for Claude Code interaction with:
- Persistent session state management
- Natural language expense parsing
- Splitwise API integration with proper date handling
- Confidence-based automation with human oversight

## 🚨 Troubleshooting

**Authentication Issues**
- Verify Splitwise API credentials in `.env`
- Test connection: `uv run python tools/splitwise_client.py`

**Group/Member Issues**
- Ensure Splitwise group URL is correct
- Verify all travelers are group members
- Check user ID matching in active session

**Processing Issues**
- Review staging area: expenses may need approval
- Check confidence scores for automated decisions
- Verify file formats and date ranges

## 📄 License

MIT License - Use freely for personal and commercial projects!

---

**Ready to automate your group expense splitting?**

Start with Claude Code and let SplitSmart handle the math! 🎒✈️