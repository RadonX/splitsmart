# Active Session Context

## Current Trip/Group
**Status**: No active group selected
**Group ID**: None
**Group Name**: None
**Base Currency**: None

## Group Members
**Members**: None loaded
**User IDs**: None

```
Format when active:
- John Doe (user_id: 12345) - Current User
- Mary Smith (user_id: 67890)  
- Bob Johnson (user_id: 54321)
```

## Recent Expenses
**Last 5 Expenses**: None recorded

```
Format when active:
1. 2024-01-15: $40.00 Dinner (John paid, split 3 ways)
2. 2024-01-15: $60.00 Gas (Mary paid, split between John & Mary)
3. 2024-01-14: $120.00 Hotel (Bob paid, split 3 ways)
```

## Session Preferences
**Default Split Method**: Equal among all members
**Default Category**: General (15)
**Timezone**: User's local timezone
**Date Format**: YYYY-MM-DD

## Authentication Status
**Splitwise API**: Not authenticated
**Credentials Source**: .env file
**Python Client**: Available at tools/splitwise_client.py
**Test Status**: Not tested

*To test authentication:*
```bash
uv run python tools/splitwise_client.py
```

## Document Processing Status
**Bank Statement**: None uploaded (primary source of truth)
**Pending Transactions**: None requiring clarification
**Receipts**: None uploaded (for transaction details/verification)
**Processing Mode**: Bank-statement-first workflow  
**Multi-Receipt Photos**: None uploaded

```
Receipt Format:
1. mario_pizza_receipt.pdf - $47.83 - Processed - Expense ID: 12345
2. hotel_receipt.pdf - $240.00 - Pending split decisions

Bank Statement Format:
1. chase_statement_jan.pdf - 12 transactions - 3 selected for splitting
2. visa_statement.pdf - 8 transactions - Processing

Multi-Receipt Photo Format:
1. trip_receipts_photo.jpg - 3 receipts identified - 2 processed, 1 pending
2. gas_station_receipts.png - 2 receipts - Both processed
```

## Quick Commands Reference
- "Set group [group_name]" - Switch to different group
- "Show balances" - Get current group balances from Splitwise
- "List groups" - Show all available groups
- "Add expense" - Start expense entry workflow
- "Upload receipt" - Process receipt PDF for expense creation
- "Upload bank statement" - Process bank statement for multiple expenses
- "Upload photo" - Process photo with multiple receipts

## Session Notes
- This file gets updated throughout the conversation
- Context persists until session ends or group changes
- Authentication required before expense operations
- Group selection required before adding expenses
- Receipt processing uses Read tool to extract PDF text
- Bank statement processing filters trip-related transactions
- Multi-receipt photos processed by identifying separate receipt regions
- Itemized breakdowns stored in expense details field
- Batch expense creation for multiple transactions from same source

---
*Last Updated*: Session start
*Active Since*: Not started