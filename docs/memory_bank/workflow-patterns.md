# Bank-Statement-First Workflow Patterns

## Primary Workflow: Trip Context → Bank Statement → Clarification → Splitwise

**Progress Tracking**: Each step updates `conversation-progress.md` with completion status, decisions made, and next actions.

### Step 0: Trip Context Collection
```
Session Start:
Claude: "Let's set up your trip context first. What trip are we processing expenses for?"
↓
User: Provides trip name, dates, travelers
↓
Claude: "Got it! Montreal trip, Jan 15-18, 2024, with John, Mary, Bob. Which Splitwise group should I use?"
↓
User: Provides Splitwise group URL or selects from list
↓
Claude: Match trip travelers to Splitwise group members, flag any mismatches
```

### Step 1: Bank Statement Upload & Parse
```
User uploads bank statement (PDF/CSV)
↓
Claude: Parse all transactions
↓  
Claude: Filter by trip date range and amount thresholds
↓
Claude: "Found 23 transactions, 12 within trip dates (Jan 15-18). Processing trip expenses only."
↓
Claude: Present expense candidates for review
```

### Step 2: Transaction Clarification Loop
```
For each transaction needing clarification:
Claude: "I see $47.83 at Mario's Pizza on Jan 15. What was this for?"
↓
User: "Dinner for 3 people" OR [uploads matching receipt]
↓
Claude: "Split equally among 3, or custom amounts?"
↓
User: Confirms split method and participants
↓
Claude: Queue for Splitwise creation
```

### Step 3: Staging Area with Confidence Scoring
```
Once transactions are processed:
Claude: Add to staging with confidence scores
↓
Claude: "I have 12 expenses staged. 8 are high confidence (95%+), 4 need review"
↓
User: Reviews low-confidence expenses, makes corrections
↓
Claude: Auto-submit high-confidence expenses, hold others for approval
```

### Step 4: Batch Splitwise Submission
```
Menu-driven review creates approved expense list:
✅ Airbnb $575.87 - Equal split
✅ Cafe $12.21 - Equal split  
✅ Viator Tours $369.62 - Custom split (2/3 vs 1/3)
❌ Personal expenses - Skipped
↓
Claude: "Ready to create these 5 Splitwise expenses totaling $1,081.72?"
↓
User: "yes" 
↓
Claude: Batch create all approved expenses with proper dates
Claude: "✅ Successfully created 5 expenses. All logged to Splitwise!"
```

### Confidence-Based Submission
```
When confidence threshold met:
High confidence (≥95%): Auto-submit to Splitwise
Medium confidence (70-94%): Stage for review
Low confidence (<70%): Require explicit user confirmation
↓
Claude: "Submitted 8 expenses automatically. 4 pending your review."
```

## Bank Statement Processing Rules

### Transaction Filtering
**Include by Default:**
- Restaurant/food charges
- Gas stations  
- Hotels/lodging
- Transportation (Uber, taxi, parking)
- Entertainment/activities
- Shopping (if during trip dates)

**Exclude by Default:**
- ATM withdrawals
- Bank fees/interest
- Transfers between accounts
- Personal charges outside trip dates
- Duplicate/refund transactions
- Charges below $5 threshold

**Ask User to Confirm:**
- Large charges (>$500)
- Unclear merchant names
- Charges on trip boundary dates
- Multiple charges at same merchant

### Transaction Categorization
```
Merchant patterns → Splitwise categories:
- *RESTAURANT*, *PIZZA*, *CAFE* → Food & Dining (5)
- *HOTEL*, *MARRIOTT*, *AIRBNB* → Lodging (17) 
- *SHELL*, *EXXON*, *GAS* → Transportation (18)
- *UBER*, *TAXI*, *PARKING* → Transportation (18)
- *GROCERY*, *WALMART*, *TARGET* → General (15)
```

## Receipt Processing (Secondary)

### Receipt-to-Bank-Statement Matching
1. **Amount Matching**: Match receipt total to bank transaction
2. **Date Matching**: Within 1-2 days of bank transaction
3. **Merchant Matching**: Fuzzy match merchant names
4. **Manual Linking**: User specifies "this receipt is for the $47.83 Mario's charge"

### Itemized Receipt Handling
```
Receipt with multiple items:
Claude: "I see 4 items on this receipt. Should I:
A) Split everything equally among everyone
B) Let people claim specific items  
C) Exclude certain items (alcohol, etc.)"
```

### Multi-Receipt Photos
```
Single photo with multiple receipts:
Claude: "I see 3 separate receipts in this photo:
1. Mario's Pizza - $47.83
2. Coffee Shop - $12.50  
3. Gas Station - $65.00
Should I process all three?"
```

## Trip Context Collection

### Initial Setup Questions
**Trip Identification:**
- "What trip are we processing expenses for?"
- "Where did you go and when?"
- "What should I call this trip?"

**Date Range:**
- "What were the trip dates?" (start and end)
- "Include travel days?" (flights, arrival/departure)
- "Any pre-trip shopping to include?"

**Travelers:**
- "Who went on this trip?"
- "Are there any people who joined partway through?"
- "Anyone who left early?"

**Splitwise Integration:**
- "Which Splitwise group should I use?"
- "Do all travelers have Splitwise accounts?"
- "Should I create expenses for everyone or just group members?"

### Trip Context Validation
**Traveler Matching:**
```
Trip travelers: [John, Mary, Bob, Sarah]
Splitwise group: [John Smith, Mary Johnson, Bob Wilson]
↓
Claude: "I notice Sarah isn't in the Splitwise group. Should I:
A) Add expenses for her anyway (you'll settle outside Splitwise)
B) Exclude her from shared expenses
C) Help you invite her to the group first?"
```

**Date Range Validation:**
```
Trip dates: Jan 15-18, 2024
Bank statement shows charges on Jan 14 and Jan 19
↓
Claude: "I see charges on Jan 14 ($45 Uber) and Jan 19 ($30 breakfast). 
Should I include travel day expenses?"
```

## User Input Patterns

### Menu-Driven Transaction Review
Present one transaction at a time with numbered menu options for quick decisions.

```
Claude: "## Transaction #1: Airbnb Accommodation
**Date**: 06/28/2025
**Amount**: $575.87  
**Description**: AIRBNB * HMRZY5A9NX
**Category**: Accommodation

Should this be split equally between [User] and [Traveler2] ($287.94 each)?"

User: "y" (or "1" for equally, "2" for personal, "3" for custom)
↓
Claude: "✅ **Approved**: Airbnb $575.87 (06/28/2025) - Split equally

## Transaction #2: [Next transaction...]"
```

### Open-Ended Transaction Clarification
- "What was this $X charge at [Merchant] for?"
- "Who should be included in splitting this expense?"
- "Did everyone participate equally, or custom amounts?"
- "Should this be categorized as [category]?"

### Expected User Responses

**Menu-Driven Quick Responses**:
- "y" or "equally" → Split equally among all travelers
- "2" or "personal" → Skip as personal expense
- "2 shares for [user], 1 for [traveler]" → Custom ratio split
- "leave them for now" → Defer for receipt cross-check
- "cross check with receipt later" → Add to pending list

**Open-Ended Detailed Responses**:
- "Dinner for 4 people, split equally"
- "Gas, split between me and John only"  
- "Hotel, I paid, split among everyone"
- "Skip this one, it's personal"
- "That's a refund, ignore it"

### Receipt Context Integration
- "Here's the receipt for the Mario's charge"
- "The hotel receipt shows $240 total including tax"
- "This receipt has drinks that only 2 people had"

## Python Tool Execution

### UV Requirement Check
```bash
# Check if uv is installed
if ! command -v uv >/dev/null 2>&1; then
    echo "UV is required for expense management. Please install:"
    echo "curl -LsSf https://astral.sh/uv/install.sh | sh"
    echo "Then restart your terminal."
    exit 1
fi
```

### Standard Tool Execution Pattern
```bash
# All Python tools use uv run
uv run python -c "
from tools.splitwise_client import create_equal_split_expense
result = create_equal_split_expense('Dinner', 60.0, 12345, [12345, 67890])
print(result)
"
```

## Confidence Scoring System

### Confidence Factors (0-100%)

**High Confidence Indicators (+20-30% each):**
- Exact amount match between bank statement and receipt
- Clear merchant name with obvious category
- User explicitly confirmed split method
- Standard equal split among all known trip travelers
- Transaction within established trip date range
- Participant list matches trip context

**Medium Confidence Indicators (+10-20% each):**
- Fuzzy merchant name match
- Reasonable expense amount for category
- Default split method applied
- Transaction near trip dates

**Low Confidence Penalties (-10-30% each):**
- Unclear merchant name requiring guess
- Unusual amount for expense type
- Custom split with participants not on trip
- Transaction outside established trip dates
- Missing receipt for large expense (>$100)
- Participants unknown or not in Splitwise group

### Confidence Calculation Examples

**High Confidence (95%):**
```
Bank: $47.83 at MARIO'S PIZZA on 2024-01-15
Receipt: $47.83 Mario's Pizza receipt uploaded
User: "Dinner for 4 people, split equally"
Split: Equal among all 4 group members
→ 95% confidence, auto-submit
```

**Medium Confidence (78%):**
```
Bank: $65.00 at SHELL #1234 on 2024-01-16  
No receipt provided
User: "Gas, split between me and John"
Split: Custom (2 people only)
→ 78% confidence, stage for review
```

**Low Confidence (45%):**
```
Bank: $240.00 at UNKNOWN MERCHANT on 2024-01-14
No receipt, unclear merchant
User: No input yet
Split: Assumed equal among all
→ 45% confidence, require explicit approval
```

## Staging Area Management

### Staged Expense Data Structure
```json
{
  "expense_id": "temp_001",
  "confidence": 95,
  "status": "ready_to_submit",
  "bank_transaction": {
    "amount": 47.83,
    "merchant": "MARIO'S PIZZA",
    "date": "2024-01-15"
  },
  "splitwise_payload": {
    "cost": "47.83",
    "description": "Mario's Pizza dinner",
    "users": [...],
    "group_id": 83515836
  },
  "evidence": [
    "Receipt uploaded and matched",
    "User confirmed participants",
    "Equal split standard pattern"
  ]
}
```

### Staging Commands
- `show staged` - Display all staged expenses with confidence scores
- `review low confidence` - Show expenses needing review
- `submit ready` - Submit all high-confidence expenses
- `edit expense temp_001` - Modify specific staged expense
- `clear staging` - Remove all staged expenses

## Error Handling

### Bank Statement Issues
- Corrupted/unreadable files → Ask for re-upload
- Missing transaction details → Request manual input
- Currency conversion needed → Ask for exchange rate

### Transaction Ambiguity
- Multiple people could have paid → Ask who paid
- Unclear merchant → Ask for description
- Amount discrepancies → Show both amounts, ask which to use

### Splitwise API Errors
- Authentication failures → Guide credential setup
- Invalid group members → Show current members, ask to clarify
- Amount validation errors → Show calculation, ask to verify