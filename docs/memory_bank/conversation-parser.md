# Conversation Parsing Patterns

## Natural Language → Splitwise API Mapping

### Common Expense Phrases

#### Equal Split Patterns
- "Split $X dinner equally" → Equal split among all active participants
- "Split $X between John and Mary" → Equal split between specified people
- "Divide $X three ways" → Equal split among 3 people (need to clarify who)
- "Everyone pays $X each for tickets" → Each person paid their own share

#### Custom Split Patterns  
- "John paid $50, everyone owes $10" → John paid_share=50, others owed_share=10
- "I paid $60, split 40/20 with Sarah" → Payer owed_share=40, Sarah owed_share=20
- "Split proportionally by room occupancy" → Need to ask for specific amounts

#### Payer Identification
- "I paid..." → Use current user as payer
- "John paid..." → John is payer, others have paid_share=0
- "We each paid our own" → Each person paid_share = owed_share

#### Receipt Upload Patterns
- "Here's the receipt for dinner" → Extract amount, description, analyze for splitting
- "Can you process this receipt?" → Read PDF, identify line items, suggest splits
- "Split this receipt equally" → Parse receipt, divide total among group
- "This receipt has multiple items" → Ask which items to include/exclude per person

#### Bank Statement Patterns
- "Here's my bank statement from the trip" → Extract all travel-related transactions
- "Find the expenses from our weekend trip" → Filter transactions by date range
- "Which of these charges should be split?" → Review each transaction for group relevance
- "Ignore the ATM withdrawals" → Filter out non-splittable transaction types

#### Multiple Receipt Photo Patterns
- "This photo has 3 receipts" → Identify separate receipt regions, process each individually
- "Split all these receipts equally" → Process each receipt, create multiple expenses
- "Some of these are mine only" → Ask user to identify which receipts to split vs. personal

### Conversation Flow Patterns

#### Initial Expense Entry
1. **Capture basics**: "What was the expense for?" → description
2. **Get amount**: "How much?" → cost
3. **Identify payer**: "Who paid?" → paid_share assignment
4. **Determine split**: "How should this be split?" → owed_share calculation

#### Receipt Processing Flow
1. **Read Receipt**: Extract text from PDF using Read tool
2. **Parse Information**: Identify total amount, vendor, date, line items
3. **Confirm Details**: "I see a $X receipt from [vendor] on [date]. Is this correct?"
4. **Analyze Items**: List individual items if multiple line items present
5. **Guide Splitting**: "Which items should each person pay for?" or "Split the total equally?"
6. **Create Expense**: Convert to Splitwise API call with parsed details

#### Bank Statement Processing Flow
1. **Read Statement**: Extract transaction data from PDF/image using Read tool
2. **Filter Transactions**: Identify trip-related expenses vs. personal/unrelated charges
3. **Present Options**: "I found X transactions during your trip dates. Here are the candidates for splitting:"
4. **Transaction Review**: Show each transaction with date, merchant, amount
5. **Splitting Decisions**: For each selected transaction, determine split method and participants
6. **Batch Creation**: Create multiple Splitwise expenses efficiently

#### Multiple Receipt Photo Flow
1. **Analyze Image**: Use Read tool to process photo and identify separate receipt regions
2. **Separate Receipts**: "I can see 3 different receipts in this photo. Let me process each one:"
3. **Individual Processing**: Extract details from each receipt separately
4. **Batch Confirmation**: Present all receipts with totals and suggested splits
5. **Selective Splitting**: Allow user to choose which receipts to split vs. keep personal
6. **Create Multiple Expenses**: Generate separate Splitwise expenses for each shared receipt

#### Clarification Questions
- "Who should be included in this expense?" (if not all group members)
- "What date was this?" (if not today)
- "What category is this?" (if not obvious from description)
- "Which currency?" (if group has multiple currencies)

### Response Patterns

#### Confirmation
- "I'll add a $X expense for [description], paid by [payer], split [method] among [participants]"
- Show the breakdown before posting to Splitwise
- Ask "Does this look correct?"

#### Error Handling
- "I couldn't find that person in the group. Current members are: [list]"
- "The amounts don't add up to the total. Let me recalculate..."
- "Splitwise returned an error: [error message]. Let's try again."

#### Success Response
- "✓ Expense added successfully"
- "Current balances: [show updated balances if available]"
- "Anything else to add?"

### Context Tracking

#### Session State
- Current group_id and group name
- List of group members with user_ids
- Recent expenses for reference
- Default currency for group

#### Conversation Memory
- Remember who paid last (for "same person paid again")
- Track common split patterns for this group
- Remember preferred categories for types of expenses

### Example Conversations

**Simple Equal Split:**
User: "I paid $40 for dinner, split it equally"
Claude: "I'll add a $40 dinner expense paid by you, split equally among [group members]. That's $X each. Correct?"

**Custom Split:**
User: "John paid $60 for gas, but Mary wasn't in the car"
Claude: "So John paid $60 for gas, split between John and you (excluding Mary)? That's $30 each for John and you."

**Clarification Needed:**
User: "Split the hotel cost"
Claude: "I need a few details: How much was the hotel? Who paid? Should this be split among everyone or just certain people?"

**Receipt Processing:**
User: [Uploads PDF receipt]
Claude: "I can see this is a $47.83 receipt from Mario's Pizza on 2024-01-15. I found these items:
- Large Pepperoni Pizza: $18.99
- Caesar Salad: $8.50  
- 2 Drinks: $6.00
- Tax & Tip: $14.34

How would you like to split this? Equally among everyone, or should specific people pay for specific items?"

**Multi-item Receipt:**
User: "John and I shared the pizza, but only I had the salad"
Claude: "Got it! So:
- Pizza ($18.99): Split between you and John = $9.50 each
- Salad ($8.50): Just you
- Drinks ($6.00): Split equally among all 3 = $2.00 each  
- Tax & Tip ($14.34): Split equally = $4.78 each

Your total: $24.78, John's total: $14.28, Mary's total: $6.78. Should I create this expense?"

**Bank Statement Processing:**
User: [Uploads bank statement PDF]
Claude: "I found 12 transactions during your trip dates (Jan 15-17). Here are the candidates for splitting:

✓ Jan 15: Mario's Pizza - $47.83
✓ Jan 15: Shell Gas Station - $45.67
✓ Jan 16: Marriott Hotel - $240.00
✗ Jan 15: ATM Withdrawal - $100.00 (excluded)
✗ Jan 17: Personal Grocery Store - $23.45 (after trip)

Should I create expenses for the 3 selected transactions? How should each be split?"

**Multiple Receipt Photo:**
User: [Uploads photo with 3 receipts]
Claude: "I can see 3 receipts in this photo:

Receipt 1: Coffee shop - $12.45 (top left)
Receipt 2: Gas station - $52.30 (center)  
Receipt 3: Restaurant - $89.67 (bottom right)

Which of these should be split among the group? I can process each one individually or handle them all at once."