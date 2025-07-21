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
- `receipt`: Base64-encoded image or file attachment (for receipt photos)
- `details`: Additional notes (can include receipt parsing details)

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

### Receipt Processing Pattern
For receipt-based expenses:
```json
{
  "cost": "47.83",
  "description": "Mario's Pizza - itemized",
  "date": "2024-01-15T19:30:00Z",
  "details": "Large Pepperoni Pizza: $18.99, Caesar Salad: $8.50, 2 Drinks: $6.00, Tax & Tip: $14.34",
  "users": [
    {"user_id": 1, "paid_share": "47.83", "owed_share": "24.78"},
    {"user_id": 2, "paid_share": "0.00", "owed_share": "14.28"},
    {"user_id": 3, "paid_share": "0.00", "owed_share": "6.78"}
  ]
}
```

## Receipt Handling
- Use Read tool to extract text from uploaded PDF receipts
- Parse key information: vendor, date, total amount, line items
- Guide user through item-by-item splitting decisions
- Include itemized breakdown in `details` field for transparency
- Attach original receipt file if supported by API

### Batch Expense Creation Pattern
For bank statements or multiple receipts:
```python
# Process multiple expenses efficiently
expenses_data = [
    {"cost": "47.83", "description": "Mario's Pizza", "date": "2024-01-15T19:30:00Z"},
    {"cost": "45.67", "description": "Shell Gas Station", "date": "2024-01-15T14:20:00Z"},
    {"cost": "240.00", "description": "Marriott Hotel", "date": "2024-01-16T15:00:00Z"}
]

for expense in expenses_data:
    # Add user splits to each expense
    expense["users"] = calculate_split_for_expense(expense, participants, split_method)
    # Create individual Splitwise expense
    response = post_to_splitwise("/create_expense", expense)
```

### Bank Statement Filtering
Common transaction types to exclude:
- ATM withdrawals
- Bank fees
- Transfers between accounts
- Personal charges outside trip dates
- Duplicate/refund transactions

Include candidates:
- Restaurant/food charges
- Gas stations
- Hotels/accommodation
- Transportation (Uber, taxi, parking)
- Entertainment/activities

## Helper Functions to Write
- `post_to_splitwise(endpoint, data)` - Generic API caller
- `create_expense_payload(description, amount, payer, participants, split_method)` - Convert natural language to API format
- `get_group_members(group_id)` - Fetch current group participants
- `parse_receipt_pdf(file_path)` - Extract structured data from receipt PDFs
- `calculate_itemized_splits(items, participant_assignments)` - Calculate individual owed shares from line items
- `parse_bank_statement(file_path, trip_dates)` - Extract and filter relevant transactions
- `identify_receipt_regions(image_path)` - Separate multiple receipts in single photo
- `batch_create_expenses(expenses_list)` - Efficiently create multiple Splitwise expenses