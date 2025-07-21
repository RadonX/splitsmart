# Bank-Statement-First Workflow Patterns

## Primary Workflow: Bank Statement → Clarification → Splitwise

### Step 1: Bank Statement Upload & Parse
```
User uploads bank statement (PDF/CSV)
↓
Claude: Parse all transactions
↓  
Claude: Filter by date range and amount thresholds
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

### Step 3: Batch Splitwise Creation
```
Once all transactions are clarified:
Claude: "Ready to create 12 expenses in Splitwise. Proceed?"
↓
User: Confirms
↓  
Claude: Batch create expenses via API
↓
Claude: Report success/failures and update balances
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

## User Input Patterns

### Transaction Clarification Questions
- "What was this $X charge at [Merchant] for?"
- "Who should be included in splitting this expense?"
- "Did everyone participate equally, or custom amounts?"
- "Should this be categorized as [category]?"

### Expected User Responses
- "Dinner for 4 people, split equally"
- "Gas, split between me and John only"
- "Hotel, I paid, split among everyone"
- "Skip this one, it's personal"
- "That's a refund, ignore it"

### Receipt Context Integration
- "Here's the receipt for the Mario's charge"
- "The hotel receipt shows $240 total including tax"
- "This receipt has drinks that only 2 people had"

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