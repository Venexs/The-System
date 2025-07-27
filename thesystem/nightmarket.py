import ujson
from datetime import datetime, timedelta
import os
import random

def get_weekly_night_market_data():
    """
    Get weekly night market data with automatic weekly management.
    
    This function handles the complete weekly data lifecycle:
    - Checks if it's a new week (Monday-based)
    - Creates new data if it's a new week
    - Returns existing data if it's the same week
    - Stores data in Player Data directory as JSON
    
    Weekly Reset Logic:
    - New week = Monday (weekday 0)
    - Week key format: "YYYY-MM-DD" (Monday's date)
    - Data structure includes rank items (S, B, C, D) with rarity info
    - Items are filtered by rarity (Common, Rare, Epic, Legendary)
    
    Returns:
        dict: Weekly night market data with structure:
        {
            "week_key": "YYYY-MM-DD",           # Monday's date as week identifier
            "created_date": "YYYY-MM-DD HH:MM:SS", # When this week's data was created
            "week_start": "YYYY-MM-DD",         # Monday's date
            "last_updated": "YYYY-MM-DD HH:MM:SS", # Last time data was accessed
            "rank_items": {
                "S": {"item_name": {"rarity": "Common/Rare/Epic/Legendary", "data": {...}}},
                "B": {...},
                "C": {...},
                "D": {...}
            }
        }
    """
    # File path for storing weekly data in Player Data directory
    file_path = "Files/Player Data/Night_Market_Weekly.json"
    
    # Calculate current week's Monday date for week identification
    today = datetime.now()
    days_since_monday = today.weekday()  # 0=Monday, 1=Tuesday, etc.
    monday = today - timedelta(days=days_since_monday)
    monday = monday.replace(hour=0, minute=0, second=0, microsecond=0)
    current_week_key = monday.strftime("%Y-%m-%d")
    
    # Check if weekly data file exists
    if os.path.exists(file_path):
        try:
            # Load existing weekly data
            with open(file_path, 'r') as f:
                stored_data = ujson.load(f)
            
            # Check if current week matches stored week
            stored_week_key = stored_data.get("week_key")
            
            if stored_week_key == current_week_key:
                # Same week - return existing data and update timestamp
                stored_data["last_updated"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                with open(file_path, 'w') as f:
                    ujson.dump(stored_data, f, indent=4)
                return stored_data
            else:
                # New week - create fresh data
                return _create_new_weekly_data(current_week_key, monday)
                
        except Exception as e:
            print(f"Error loading night market data: {e}")
            return _create_new_weekly_data(current_week_key, monday)
    else:
        # File doesn't exist - create new data
        return _create_new_weekly_data(current_week_key, monday)

def _create_new_weekly_data(week_key, monday_date):
    """
    Internal function to create new weekly night market data.
    
    Args:
        week_key (str): Week identifier (Monday's date)
        monday_date (datetime): Monday's datetime object
    
    Returns:
        dict: New weekly data with rank items and metadata
    """
    # Load inventory data to get rank items
    try:
        with open("Files/Data/Inventory_List.json", 'r') as f:
            inventory_data = ujson.load(f)
    except Exception as e:
        print(f"Error loading inventory data: {e}")
        inventory_data = {}
    
    # Initialize rank items structure
    rank_items = {"S": {}, "B": {}, "C": {}, "D": {}}
    
    # Rarity-based selection configuration - 1 item per rank with flexible rarity
    rarity_config = {
        "S": {"Common": 0, "Rare": 0, "Epic": 0, "Legendary": 1},  # S-rank: 1 Legendary item
        "B": {"Common": 0, "Rare": 0, "Epic": 1, "Legendary": 0},  # B-rank: 1 Epic item
        "C": {"Common": 0, "Rare": 1, "Epic": 0, "Legendary": 0},  # C-rank: 1 Rare item
        "D": {"Common": 1, "Rare": 0, "Epic": 0, "Legendary": 0}   # D-rank: 1 Common item
    }
    
    # Process each rank separately
    for rank in ["S", "B", "C", "D"]:
        # Collect all items for this rank
        rank_candidates = {}
        for item_name, item_data in inventory_data.items():
            if item_data and len(item_data) > 0:
                item = item_data[0]
                item_rank = item.get("rank")
                
                if item_rank == rank:
                    rarity = item.get("rarity", "Common")
                    if item_name not in rank_candidates:
                        rank_candidates[item_name] = {
                            "rarity": rarity,
                            "data": item
                        }
        
        # Select items based on percentage-based rarity system
        selected_items = _select_items_by_rarity(rank_candidates, rarity_config[rank])
        rank_items[rank] = selected_items
    
    # Create comprehensive weekly data structure
    weekly_data = {
        "week_key": week_key,
        "created_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "week_start": monday_date.strftime("%Y-%m-%d"),
        "rank_items": rank_items,
        "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    # Save to Player Data directory
    try:
        with open("Files/Player Data/Night_Market_Weekly.json", 'w') as f:
            ujson.dump(weekly_data, f, indent=4)
    except Exception as e:
        print(f"Error saving night market data: {e}")
    
    return weekly_data

def _select_items_by_rarity(candidates, rarity_config):
    """
    Select items based on percentage-based rarity system.
    Ensures each rank gets exactly 1 item by falling back to Common if needed.
    
    Args:
        candidates (dict): All available items for a rank
        rarity_config (dict): How many items to select per rarity
    
    Returns:
        dict: Selected items based on rarity
    """
    selected_items = {}
    
    # Group candidates by rarity
    rarity_groups = {"Common": [], "Rare": [], "Epic": [], "Legendary": []}
    
    for item_name, item_info in candidates.items():
        rarity = item_info["rarity"]
        if rarity in rarity_groups:
            rarity_groups[rarity].append((item_name, item_info))
    
    # Rarity percentages (total = 100%)
    rarity_percentages = {
        "Common": 50,    # 50% chance
        "Rare": 30,      # 30% chance
        "Epic": 15,      # 15% chance
        "Legendary": 5   # 5% chance
    }
    
    # Generate random number for rarity selection
    rand_value = random.randint(1, 100)
    
    # Determine which rarity to select based on percentages
    cumulative_percentage = 0
    selected_rarity = "Common"  # Default fallback
    
    for rarity, percentage in rarity_percentages.items():
        cumulative_percentage += percentage
        if rand_value <= cumulative_percentage:
            selected_rarity = rarity
            break
    
    # Try to select 1 item from the chosen rarity
    available_items = rarity_groups.get(selected_rarity, [])
    
    if available_items:
        # Select 1 item from the chosen rarity
        selected = random.sample(available_items, 1)
        
        # Add selected item to result
        for item_name, item_info in selected:
            selected_items[item_name] = item_info
    else:
        # Fallback to Common if chosen rarity has no items
        common_items = rarity_groups.get("Common", [])
        if common_items:
            selected = random.sample(common_items, 1)
            for item_name, item_info in selected:
                selected_items[item_name] = item_info
        else:
            # If even Common is empty, take any available item
            all_items = []
            for items in rarity_groups.values():
                all_items.extend(items)
            
            if all_items:
                selected = random.sample(all_items, 1)
                for item_name, item_info in selected:
                    selected_items[item_name] = item_info
    
    return selected_items

# Legacy function for backward compatibility
def get_rank_items_with_rarity():
    """
    Legacy function - use get_weekly_night_market_data() instead.
    Returns only the rank items without weekly management.
    """
    weekly_data = get_weekly_night_market_data()
    return weekly_data["rank_items"]

# Main execution block moved into the function
if __name__ == "__main__":
    # Get current weekly data (handles all weekly logic automatically)
    weekly_data = get_weekly_night_market_data()
    
    # Display weekly metadata
    print(f"Week Key: {weekly_data['week_key']}")
    print(f"Created: {weekly_data['created_date']}")
    print(f"Week Start: {weekly_data['week_start']}")
    print(f"Last Updated: {weekly_data['last_updated']}")
    
    # Display rank items summary with rarity breakdown
    rank_items = weekly_data['rank_items']
    print(rank_items)
    for rank in ["S", "B", "C", "D"]:
        print(f"\n=== {rank}-Rank Items ===")
        rank_data = rank_items[rank]
        print(f"Total {rank}-rank items: {len(rank_data)}")
        
        # Count items by rarity
        rarity_counts = {"Common": 0, "Rare": 0, "Epic": 0, "Legendary": 0}
        for item_info in rank_data.values():
            rarity = item_info["rarity"]
            rarity_counts[rarity] = rarity_counts.get(rarity, 0) + 1
        
        print(f"Rarity breakdown: {rarity_counts}")
        
        # Show examples
        count = 0
        for item_name, item_info in rank_data.items():
            if count < 3:  # Show first 3 examples
                rarity = item_info["rarity"]
                value = item_info["data"].get("Value", 0)
                print(f"  - {item_name} ({rarity}, Value: {value})")
                count += 1
            else:
                break 