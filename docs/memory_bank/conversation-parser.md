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

### Conversation Flow Patterns

#### Initial Expense Entry
1. **Capture basics**: "What was the expense for?" → description
2. **Get amount**: "How much?" → cost
3. **Identify payer**: "Who paid?" → paid_share assignment
4. **Determine split**: "How should this be split?" → owed_share calculation

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