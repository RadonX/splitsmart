# Conversation Parsing Patterns

## Menu-Driven Interaction Mode

### Quick Response Parsing
**Single character responses for efficiency:**
- "y", "yes", "1" → Equal split among all active participants
- "n", "no", "2", "personal" → Skip as personal expense  
- "3", "custom" → Request custom split amounts
- "skip", "defer", "later" → Add to pending/review list

### Ratio-Based Custom Splits
- "2 shares for [user], 1 for [traveler]" → Calculate 2:1 ratio split
- "[user] gets 2/3, [traveler] gets 1/3" → Direct fraction split
- "60/40 split" → Percentage-based split

### Batch Decision Confirmation
- "yes" (after expense summary) → Proceed with all approved expenses
- "review first" → Show detailed breakdown before creating
- "skip expense 3" → Remove specific item from batch

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

#### Group Selection
- Splitwise URL format: `https://secure.splitwise.com/#/groups/{group_id}`
- Extract group_id from URL: `83515836` from `https://secure.splitwise.com/#/groups/83515836`
- Update active-session.md with selected group context

#### Date Preference Selection
- "transaction dates" or "actual dates" → Use dates from bank statements/receipts
- "today" or "log date" or "current date" → Use today's date for all expenses
- "transaction" → Use actual transaction dates
- Update active-session.md with date preference setting

#### Bank Statement Processing (Primary Source)
- "Here's my bank statement from the trip" → Parse all transactions, filter by dates/amounts
- "Process these transactions" → Extract expense candidates, ask for clarification
- Bank statement line → Match with receipt if provided, or ask user for context

#### Receipt/User Input (Secondary Clarification)
- "Here's the receipt for the $47.83 Mario's Pizza charge" → Match to bank statement line
- "The $240 charge was for hotel, split 3 ways" → Add context to bank statement transaction
- "Skip the ATM withdrawals" → Filter out non-expense transactions
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

#### Initial Session Setup
1. **Trip Context**: "What trip are we processing expenses for?" → trip name, dates, travelers
2. **Splitwise Group**: "Which Splitwise group should I use?" → group selection and member matching
3. **Date Preference**: "For expense dates, should I use transaction dates from statements or today's date?" → date preference setting
4. **Validation**: Check traveler-to-group-member matching, flag discrepancies
5. **Ready**: "Great! Ready to process expenses for [trip] with [travelers]."

#### Expense Processing (After Context Set)
1. **Bank Statement**: Upload and filter by trip dates
2. **Transaction Review**: Present candidates within date range
3. **Clarification**: "What was this $X charge at [Merchant] for?" 
4. **Staging**: Add to staging area with confidence score

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

#### Staging Confirmation
- "I'll stage a $X expense for [description], paid by [payer], split [method] among [participants]"
- Show confidence score: "95% confidence - will auto-submit" vs "67% confidence - staging for review"
- Ask "Should I adjust anything before staging?"

#### Error Handling
- "I couldn't find that person in the group. Current members are: [list]"
- "The amounts don't add up to the total. Let me recalculate..."
- "Splitwise returned an error: [error message]. Let's try again."

#### Staging Response
- "✓ Expense staged successfully (95% confidence)"
- "✓ 3 expenses auto-submitted to Splitwise, 2 staged for review"
- "Current staging area: 5 expenses totaling $234.67"

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

**Session Start (No Context):**
SPLITSMART: "Hi! Let's process your trip expenses. What trip are we working on?"
User: "Montreal trip last weekend"
SPLITSMART: "Got it! Can you give me the specific dates and who went on the trip?"
User: "January 15-18, 2024. Me, John, Mary, and Bob."
SPLITSMART: "Perfect! Which Splitwise group should I use for these expenses?"
User: [Provides group URL]
SPLITSMART: "For expense dates, should I use the actual transaction dates from your bank statements, or today's date?"
User: "Use the actual transaction dates"
SPLITSMART: "Great! I'll use transaction dates from your statements. Ready to process expenses."

**Bank Statement Processing (With Context):**
User: "Process this bank statement from our Montreal trip"
SPLITSMART: "I found 23 transactions. Filtering for Jan 15-18 Montreal trip expenses... I see 12 relevant charges like $47.83 at Mario's Pizza, $240 at Marriott Hotel. Should I process all restaurant and hotel charges for you, John, Mary, and Bob?"

**Bank Transaction Clarification:**
User: "The $47.83 Mario's Pizza was dinner for 3 people"
SPLITSMART: "Got it! I'll create a $47.83 dinner expense at Mario's Pizza, split equally among 3 people ($15.94 each). Who paid this charge?"

**Receipt Matching:**
User: "Here's the receipt for that $47.83 Mario's charge"
SPLITSMART: "Perfect! I can see itemized details: Large Pizza $18.99, Salads $12.00, Drinks $8.50, Tax/Tip $8.34. Should everyone split everything equally, or did people order specific items?"

**Manual Entry with Context:**
User: "Add $60 gas expense, John paid, split between me and John only"
SPLITSMART: "Adding $60 gas expense paid by John, split equally between you and John ($30 each). This will be added to Splitwise."

**Receipt Processing:**
User: [Uploads PDF receipt]
SPLITSMART: "I can see this is a $47.83 receipt from Mario's Pizza on 2024-01-15. I found these items:
- Large Pepperoni Pizza: $18.99
- Caesar Salad: $8.50  
- 2 Drinks: $6.00
- Tax & Tip: $14.34

How would you like to split this? Equally among everyone, or should specific people pay for specific items?"

**Multi-item Receipt:**
User: "John and I shared the pizza, but only I had the salad"
SPLITSMART: "Got it! So:
- Pizza ($18.99): Split between you and John = $9.50 each
- Salad ($8.50): Just you
- Drinks ($6.00): Split equally among all 3 = $2.00 each  
- Tax & Tip ($14.34): Split equally = $4.78 each

Your total: $24.78, John's total: $14.28, Mary's total: $6.78. Should I create this expense?"

**Bank Statement Processing:**
User: [Uploads bank statement PDF]
SPLITSMART: "I found 12 transactions during your trip dates (Jan 15-17). Here are the candidates for splitting:

✓ Jan 15: Mario's Pizza - $47.83
✓ Jan 15: Shell Gas Station - $45.67
✓ Jan 16: Marriott Hotel - $240.00
✗ Jan 15: ATM Withdrawal - $100.00 (excluded)
✗ Jan 17: Personal Grocery Store - $23.45 (after trip)

Should I create expenses for the 3 selected transactions? How should each be split?"

**Multiple Receipt Photo:**
User: [Uploads photo with 3 receipts]
SPLITSMART: "I can see 3 receipts in this photo:

Receipt 1: Coffee shop - $12.45 (top left)
Receipt 2: Gas station - $52.30 (center)  
Receipt 3: Restaurant - $89.67 (bottom right)

Which of these should be split among the group? I can process each one individually or handle them all at once."