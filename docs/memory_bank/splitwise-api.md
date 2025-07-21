# Splitwise API Integration

## Authentication
- API uses OAuth 1.0a or Consumer Key/Secret
- Base URL: `https://secure.splitwise.com/api/v3.0/`
- Credentials stored in `.env` file (see `.env.example`)
- All requests require authentication headers

## Programmatic Interface

### Python Client: `tools/splitwise_client.py`

The `SplitwiseClient` class handles all API interactions:

```python
from tools.splitwise_client import SplitwiseClient, create_equal_split_expense, create_custom_split_expense

# Initialize client (reads from .env automatically)
client = SplitwiseClient()

# Get user info
user = client.get_current_user()

# Get groups
groups = client.get_groups()

# Create equal split expense
result = create_equal_split_expense(
    description="Dinner at restaurant",
    total_amount=60.0,
    payer_user_id=12345,
    participant_user_ids=[12345, 67890, 54321],
    group_id=98765
)
```

### Core Client Methods

- `get_current_user()` - Get authenticated user details
- `get_groups()` - List all user's groups
- `get_group(group_id)` - Get specific group with members
- `get_expenses(group_id, limit)` - List expenses
- `create_expense(cost, description, users, ...)` - Create new expense
- `update_expense(expense_id, ...)` - Modify existing expense
- `delete_expense(expense_id)` - Remove expense

### Helper Functions

#### Equal Split
```python
create_equal_split_expense(
    description: str,
    total_amount: float,
    payer_user_id: int,
    participant_user_ids: List[int],
    currency: str = "USD",
    group_id: Optional[int] = None
)
```

#### Custom Split
```python
create_custom_split_expense(
    description: str,
    total_amount: float,
    payer_user_id: int,
    user_amounts: Dict[int, float],  # user_id -> amount_owed
    currency: str = "USD",
    group_id: Optional[int] = None
)
```

## Claude Integration Pattern

1. **Parse natural language** using conversation-parser.md patterns
2. **Extract parameters**: amount, description, payer, participants, split method
3. **Call Python function** via Bash tool:
   ```bash
   python3 -c "
   from tools.splitwise_client import create_equal_split_expense
   result = create_equal_split_expense('Dinner', 60.0, 12345, [12345, 67890])
   print(result)
   "
   ```
4. **Handle response** and update active-session.md
5. **Confirm to user** with expense details

## API Endpoints Reference

### Create Expense: POST `/create_expense`
Required: `cost`, `description`, `currency_code`
Optional: `date`, `group_id`, `category_id`, `users`

### User Split Structure
```json
{
  "user_id": 12345,
  "paid_share": "25.00",  // What they paid
  "owed_share": "12.50"   // What they owe
}
```

### Common API Patterns

#### Equal Split Among All
For "split $60 dinner equally among 4 people":
```json
{
  "cost": "60.00",
  "description": "Dinner",
  "users": [
    {"user_id": 1, "paid_share": "60.00", "owed_share": "15.00"},
    {"user_id": 2, "paid_share": "0.00", "owed_share": "15.00"},
    {"user_id": 3, "paid_share": "0.00", "owed_share": "15.00"},
    {"user_id": 4, "paid_share": "0.00", "owed_share": "15.00"}
  ]
}
```

#### Custom Split
For "John paid $50, split between John and Mary where John owes $20, Mary owes $30":
```json
{
  "cost": "50.00",
  "description": "Expense description",
  "users": [
    {"user_id": 1, "paid_share": "50.00", "owed_share": "20.00"},
    {"user_id": 2, "paid_share": "0.00", "owed_share": "30.00"}
  ]
}
```

## Error Handling
- Authentication errors: Check .env credentials
- Invalid user_id: Verify group membership
- Amount mismatches: Validate split calculations
- Network errors: Retry with exponential backoff

## Setup Requirements

1. Copy `.env.example` to `.env`
2. Register app at https://secure.splitwise.com/apps
3. Fill in consumer key/secret in `.env`
4. Install dependencies: `pip install requests python-dotenv`
5. Test with: `python3 tools/splitwise_client.py`

## Receipt Processing (Future Enhancement)
- Upload receipt photos via `receipt` parameter (base64-encoded)
- Parse receipt details into `details` field for transparency
- Guide users through itemized splitting decisions
- Support multiple receipt formats (PDF, JPG, PNG)