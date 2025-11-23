"""
COMP 163 - Project 3: Quest Chronicles
Inventory System Module - Starter Code

Name: Arielle Gerald

AI Usage: [Document any AI assistance used]

This module handles inventory management, item usage, and equipment.
"""

from custom_exceptions import (
    InventoryFullError,
    ItemNotFoundError,
    InsufficientResourcesError,
    InvalidItemTypeError
)

# Maximum inventory size
MAX_INVENTORY_SIZE = 20

# ============================================================================
# INVENTORY MANAGEMENT
# ============================================================================

def add_item_to_inventory(character, item_id):
   if len(character['inventory']) >= MAX_INVENTORY_SIZE:
        raise InventoryFullError("Inventory is full")
   character['inventory'].append(item_id)
   return True

def remove_item_from_inventory(character, item_id):
    if item_id not in character['inventory']:
        raise ItemNotFoundError(f"Item {item_id} not in inventory")
    character['inventory'].remove(item_id)
    return True

def has_item(character, item_id):
    return item_id in character['inventory']

def count_item(character, item_id):
   return character['inventory'].count(item_id)

def get_inventory_space_remaining(character):
     return MAX_INVENTORY_SIZE - len(character['inventory'])

def clear_inventory(character):
    items = character['inventory'][:]
    character['inventory'].clear()
    return items


# ============================================================================
# ITEM USAGE
# ============================================================================

def use_item(character, item_id, item_data):
    if item_id not in character["inventory"]:
        raise ItemNotFoundError("Cannot use item not in inventory")

    if item_data["type"] != "consumable":
        raise InvalidItemTypeError("Item is not consumable: " + item_id)

    effect = item_data["effect"]
    stat_name, value = parse_item_effect(effect)

    apply_stat_effect(character, stat_name, value)

    character["inventory"].remove(item_id)

    item_name = item_data.get("name", item_id)

    return "Used " + item_name + " (+" + str(value) + " " + stat_name + ")"


def equip_weapon(character, item_id, item_data):
    if item_id not in character["inventory"]:
        raise ItemNotFoundError("Weapon not in inventory")

    if item_data["type"] != "weapon":
        raise InvalidItemTypeError("Not a weapon")

    # Unequip current weapon
    if "equipped_weapon" in character and character["equipped_weapon"] is not None:
        old = character["equipped_weapon"]
        old_data = character["equipped_weapon_data"]

        stat, val = parse_item_effect(old_data["effect"])
        apply_stat_effect(character, stat, -val)

        if len(character["inventory"]) >= MAX_INVENTORY_SIZE:
            raise InventoryFullError("No space to return unequipped weapon")

        character["inventory"].append(old)

    # Equip new weapon
    stat, val = parse_item_effect(item_data["effect"])
    apply_stat_effect(character, stat, val)

    character["equipped_weapon"] = item_id
    character["equipped_weapon_data"] = item_data

    character["inventory"].remove(item_id)

    # FIXED: handle missing name
    item_name = item_data.get("name", item_id)

    return "Equipped weapon: " + item_name

def equip_armor(character, item_id, item_data):
     if item_id not in character["inventory"]:
        raise ItemNotFoundError("Armor not in inventory")

     if item_data["type"] != "armor":
        raise InvalidItemTypeError("Not armor")

    # Unequip current armor
     if "equipped_armor" in character and character["equipped_armor"] is not None:
        old = character["equipped_armor"]
        old_data = character["equipped_armor_data"]

        stat, val = parse_item_effect(old_data["effect"])
        apply_stat_effect(character, stat, -val)

        if len(character["inventory"]) >= MAX_INVENTORY_SIZE:
            raise InventoryFullError("No space to return unequipped armor")

        character["inventory"].append(old)

    # Equip new armor
     stat, val = parse_item_effect(item_data["effect"])
     apply_stat_effect(character, stat, val)

     character["equipped_armor"] = item_id
     character["equipped_armor_data"] = item_data

     character["inventory"].remove(item_id)

    # FIXED: handle missing name
     item_name = item_data.get("name", item_id)

     return "Equipped armor: " + item_name

def unequip_weapon(character):
   if "equipped_weapon" not in character or character["equipped_weapon"] is None:
        return None

   if len(character["inventory"]) >= MAX_INVENTORY_SIZE:
        raise InventoryFullError("No room to unequip weapon")

   weapon_id = character["equipped_weapon"]
   weapon_data = character["equipped_weapon_data"]

   stat, val = parse_item_effect(weapon_data["effect"])
   apply_stat_effect(character, stat, -val)

   character["inventory"].append(weapon_id)

   character["equipped_weapon"] = None
   character["equipped_weapon_data"] = None

   return weapon_id

def unequip_armor(character):
    if "equipped_armor" not in character or character["equipped_armor"] is None:
        return None

    if len(character["inventory"]) >= MAX_INVENTORY_SIZE:
        raise InventoryFullError("No room to unequip armor")

    armor_id = character["equipped_armor"]
    armor_data = character["equipped_armor_data"]

    stat, val = parse_item_effect(armor_data["effect"])
    apply_stat_effect(character, stat, -val)

    character["inventory"].append(armor_id)

    character["equipped_armor"] = None
    character["equipped_armor_data"] = None

    return armor_id


# ============================================================================
# SHOP SYSTEM
# ============================================================================

def purchase_item(character, item_id, item_data):
    cost = item_data["cost"]

    if character["gold"] < cost:
        raise InsufficientResourcesError("Not enough gold")

    if len(character["inventory"]) >= MAX_INVENTORY_SIZE:
        raise InventoryFullError("Inventory full")

    character["gold"] -= cost
    character["inventory"].append(item_id)

    return True


def sell_item(character, item_id, item_data):
     if item_id not in character["inventory"]:
        raise ItemNotFoundError("Item to sell not found")

     sell_price = item_data["cost"] // 2

     character["inventory"].remove(item_id)
     character["gold"] += sell_price

     return sell_price

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def parse_item_effect(effect_string):
    if ":" not in effect_string:
        raise InvalidItemTypeError("Invalid effect format")

    parts = effect_string.split(":")
    stat = parts[0]
    value_str = parts[1]

    try:
        value = int(value_str)
    except:
        raise InvalidItemTypeError("Effect value must be integer")

    return stat, value

def apply_stat_effect(character, stat_name, value):
    if stat_name not in character:
        character[stat_name] = 0

    character[stat_name] += value

    if stat_name == "health":
        if character["health"] > character["max_health"]:
            character["health"] = character["max_health"]

def display_inventory(character, item_data_dict):
     print("\n=== INVENTORY ===")

     if len(character["inventory"]) == 0:
        print("(empty)")
        print("=================\n")
        return

     seen = []

     for item_id in character["inventory"]:
        if item_id not in seen:
            qty = character["inventory"].count(item_id)
            seen.append(item_id)

            item_info = item_data_dict.get(item_id, None)

            if item_info is None:
                name = "(unknown item)"
                type_name = "unknown"
            else:
                name = item_info.get("name", item_id)
                type_name = item_info["type"]

            print(f"{name} (x{qty}) - {type_name}")

     print("=================\n")

# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":
    print("=== INVENTORY SYSTEM TEST ===")
    
    # Test adding items
    # test_char = {'inventory': [], 'gold': 100, 'health': 80, 'max_health': 80}
    # 
    # try:
    #     add_item_to_inventory(test_char, "health_potion")
    #     print(f"Inventory: {test_char['inventory']}")
    # except InventoryFullError:
    #     print("Inventory is full!")
    
    # Test using items
    # test_item = {
    #     'item_id': 'health_potion',
    #     'type': 'consumable',
    #     'effect': 'health:20'
    # }
    # 
    # try:
    #     result = use_item(test_char, "health_potion", test_item)
    #     print(result)
    # except ItemNotFoundError:
    #     print("Item not found")

