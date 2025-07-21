#!/usr/bin/env python3
"""
Splitwise API Client for Claude Expense Manager
Handles all programmatic interactions with Splitwise API
"""

import os
import requests
import json
from typing import Dict, List, Optional, Any
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class SplitwiseClient:
    """Client for interacting with Splitwise API"""
    
    def __init__(self):
        self.base_url = "https://secure.splitwise.com/api/v3.0"
        self.consumer_key = os.getenv("SPLITWISE_CONSUMER_KEY")
        self.consumer_secret = os.getenv("SPLITWISE_CONSUMER_SECRET")
        self.api_key = os.getenv("SPLITWISE_API_KEY")
        self.oauth_token = os.getenv("SPLITWISE_OAUTH_TOKEN")
        self.oauth_token_secret = os.getenv("SPLITWISE_OAUTH_TOKEN_SECRET")
        
        if not self.api_key and not all([self.consumer_key, self.consumer_secret]):
            raise ValueError("Missing required Splitwise API credentials in .env file")
    
    def _make_request(self, endpoint: str, method: str = "GET", data: Dict = None) -> Dict:
        """Make authenticated request to Splitwise API"""
        url = f"{self.base_url}/{endpoint}"
        
        # Use API key authentication (Bearer token)
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        try:
            if method == "GET":
                response = requests.get(url, headers=headers)
            elif method == "POST":
                response = requests.post(url, headers=headers, json=data)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")
            
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.RequestException as e:
            return {"error": str(e), "status_code": getattr(e.response, 'status_code', None)}
    
    def get_current_user(self) -> Dict:
        """Get current authenticated user information"""
        return self._make_request("get_current_user")
    
    def get_groups(self) -> Dict:
        """Get all groups for the current user"""
        return self._make_request("get_groups")
    
    def get_group(self, group_id: int) -> Dict:
        """Get specific group details"""
        return self._make_request(f"get_group/{group_id}")
    
    def get_expenses(self, group_id: Optional[int] = None, limit: int = 0) -> Dict:
        """Get expenses, optionally filtered by group"""
        endpoint = "get_expenses"
        params = []
        if group_id:
            params.append(f"group_id={group_id}")
        if limit > 0:
            params.append(f"limit={limit}")
        
        if params:
            endpoint += "?" + "&".join(params)
        
        return self._make_request(endpoint)
    
    def create_expense(self, 
                      cost: str,
                      description: str,
                      currency_code: str = "USD",
                      users: List[Dict] = None,
                      group_id: Optional[int] = None,
                      category_id: int = 15,  # General category
                      date: Optional[str] = None) -> Dict:
        """
        Create a new expense
        
        Args:
            cost: Total expense amount as string
            description: Expense description
            currency_code: 3-letter currency code
            users: List of user dictionaries with user_id, paid_share, owed_share
            group_id: Group to add expense to
            category_id: Expense category (15=General)
            date: Date in YYYY-MM-DDTHH:MM:SSZ format
        """
        data = {
            "cost": cost,
            "description": description,
            "currency_code": currency_code,
            "category_id": category_id
        }
        
        if group_id:
            data["group_id"] = group_id
        
        if date:
            data["date"] = date
        else:
            data["date"] = datetime.now().isoformat() + "Z"
        
        if users:
            data["users"] = users
        
        return self._make_request("create_expense", "POST", data)
    
    def update_expense(self, expense_id: int, **kwargs) -> Dict:
        """Update an existing expense"""
        return self._make_request(f"update_expense/{expense_id}", "POST", kwargs)
    
    def delete_expense(self, expense_id: int) -> Dict:
        """Delete an expense"""
        return self._make_request(f"delete_expense/{expense_id}", "POST")


def create_equal_split_expense(description: str, total_amount: float, 
                             payer_user_id: int, participant_user_ids: List[int],
                             currency: str = "USD", group_id: Optional[int] = None) -> Dict:
    """
    Helper function to create an equal split expense
    
    Args:
        description: What the expense was for
        total_amount: Total cost
        payer_user_id: Who paid the expense
        participant_user_ids: List of all people who should split the cost
        currency: Currency code
        group_id: Group to add to
    """
    client = SplitwiseClient()
    
    # Calculate equal split
    per_person = round(total_amount / len(participant_user_ids), 2)
    
    # Build users array
    users = []
    for user_id in participant_user_ids:
        if user_id == payer_user_id:
            users.append({
                "user_id": user_id,
                "paid_share": str(total_amount),
                "owed_share": str(per_person)
            })
        else:
            users.append({
                "user_id": user_id,
                "paid_share": "0.00",
                "owed_share": str(per_person)
            })
    
    return client.create_expense(
        cost=str(total_amount),
        description=description,
        currency_code=currency,
        users=users,
        group_id=group_id
    )


def create_custom_split_expense(description: str, total_amount: float,
                              payer_user_id: int, user_amounts: Dict[int, float],
                              currency: str = "USD", group_id: Optional[int] = None) -> Dict:
    """
    Helper function to create a custom split expense
    
    Args:
        description: What the expense was for
        total_amount: Total cost
        payer_user_id: Who paid the expense
        user_amounts: Dict mapping user_id to amount they owe
        currency: Currency code
        group_id: Group to add to
    """
    client = SplitwiseClient()
    
    # Validate amounts add up
    if abs(sum(user_amounts.values()) - total_amount) > 0.01:
        raise ValueError(f"User amounts {sum(user_amounts.values())} don't match total {total_amount}")
    
    # Build users array
    users = []
    for user_id, owed_amount in user_amounts.items():
        if user_id == payer_user_id:
            users.append({
                "user_id": user_id,
                "paid_share": str(total_amount),
                "owed_share": str(owed_amount)
            })
        else:
            users.append({
                "user_id": user_id,
                "paid_share": "0.00",
                "owed_share": str(owed_amount)
            })
    
    return client.create_expense(
        cost=str(total_amount),
        description=description,
        currency_code=currency,
        users=users,
        group_id=group_id
    )


if __name__ == "__main__":
    # Test the client
    try:
        client = SplitwiseClient()
        user_info = client.get_current_user()
        if "error" in user_info:
            print(f"Authentication failed: {user_info['error']}")
        else:
            print(f"Connected as: {user_info.get('user', {}).get('first_name', 'Unknown')}")
            
        groups = client.get_groups()
        if "error" not in groups:
            print(f"Found {len(groups.get('groups', []))} groups")
    
    except Exception as e:
        print(f"Error: {e}")