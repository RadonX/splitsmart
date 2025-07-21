# Splitwise API Integration

## Authentication
- API uses OAuth 1.0a or Consumer Key/Secret
- Base URL: `https://secure.splitwise.com/api/v3.0/`
- All requests require authentication headers

## Core Endpoints

### Create Expense
**POST** `/create_expense`

Required fields:
- `cost`: Total amount (string)
- `description`: Expense description
- `currency_code`: 3-letter currency code (USD, EUR, etc.)

Key optional fields:
- `date`: YYYY-MM-DDTHH:MM:SSZ format
- `group_id`: Group to add expense to
- `category_id`: Expense category (15=General, 5=Entertainment, etc.)
- `users`: Array of user split details

User split structure:
```json
{
  "user_id": 12345,
  "paid_share": "25.00",  // What they paid
  "owed_share": "12.50"   // What they owe
}
```

### Get Groups
**GET** `/get_groups`
Returns all groups user belongs to with group_id and member details.

### Get Group
**GET** `/get_group/{id}`
Returns specific group details including members.

### Get Current User
**GET** `/get_current_user`
Returns user details including user_id needed for expense creation.

## Common Patterns

### Equal Split Among All
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

### Custom Split
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
- Check for HTTP status codes
- Parse error messages from response body
- Common errors: invalid user_id, invalid group_id, authentication failures

## Helper Functions to Write
- `post_to_splitwise(endpoint, data)` - Generic API caller
- `create_expense_payload(description, amount, payer, participants, split_method)` - Convert natural language to API format
- `get_group_members(group_id)` - Fetch current group participants