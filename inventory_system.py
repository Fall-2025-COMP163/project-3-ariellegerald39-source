"""
COMP 163 - Project 3: Quest Chronicles
Inventory System Module - Starter Code

Name: Arielle Gerald

AI Usage: [Document any AI assistance used]

This module handles inventory management, item usage, and equipment.
"""

from custom_exceptions import (
    InventoryFullError,      #Raised if trying to add to a full inventory
    ItemNotFoundError,       # Raised if an item is not in inventory
    InsufficientResourcesError,# Raised if character cannot afford an item
    InvalidItemTypeError        # Raised if item type is wrong for an action
)

# Maximum inventory size
MAX_INVENTORY_SIZE = 20

# ============================================================================
# INVENTORY MANAGEMENT
# ============================================================================

def add_item_to_inventory(character, item_id):
    """
    Use a consumable item, applying its effect to the character.

    Raises:
        ItemNotFoundError: if the item is not in inventory.
        InvalidItemTypeError: if item is not consumable.
    """
    if item_id not in character["inventory"]:
        raise ItemNotFoundError("Cannot use item not in inventory")

    if item_data["type"] != "consumable":
        raise InvalidItemTypeError("Item is not consumable: " + item_id)

    stat_name, value = parse_item_effect(item_data["effect"])
    apply_stat_effect(character, stat_name, value)

    character["inventory"].remove(item_id)
    item_name = item_data.get("name", item_id)
    return f"Used {item_name} (+{value} {stat_name})"

def equip_weapon(character, item_id, item_data):
    """
    Equip a weapon, applying its stat bonuses and unequipping old weapon if any.

    Raises:
        ItemNotFoundError: if weapon is not in inventory.
        InvalidItemTypeError: if item is not a weapon.
        InventoryFullError: if inventory has no space to return old weapon.
    """
    if item_id not in character["inventory"]:
        raise ItemNotFoundError("Weapon not in inventory")

    if item_data["type"] != "weapon":
        raise InvalidItemTypeError("Not a weapon")

    # Unequip old weapon
    if character.get("equipped_weapon"):
        old_id = character["equipped_weapon"]
        old_data = character["equipped_weapon_data"]
        stat, val = parse_item_effect(old_data["effect"])
        apply_stat_effect(character, stat, -val)

        if len(character["inventory"]) >= MAX_INVENTORY_SIZE:
            raise InventoryFullError("No space to return unequipped weapon")

        character["inventory"].append(old_id)

    # Equip new weapon
    stat, val = parse_item_effect(item_data["effect"])
    apply_stat_effect(character, stat, val)
    character["equipped_weapon"] = item_id
    character["equipped_weapon_data"] = item_data
    character["inventory"].remove(item_id)

    item_name = item_data.get("name", item_id)
    return "Equipped weapon: " + item_name

def equip_armor(character, item_id, item_data):
    """
    Equip armor, applying its stat bonuses and unequipping old armor if any.

    Raises:
        ItemNotFoundError: if armor is not in inventory.
        InvalidItemTypeError: if item is not armor.
        InventoryFullError: if inventory has no space to return old armor.
    """
    if item_id not in character["inventory"]:
        raise ItemNotFoundError("Armor not in inventory")

    if item_data["type"] != "armor":
        raise InvalidItemTypeError("Not armor")

    # Unequip old armor
    if character.get("equipped_armor"):
        old_id = character["equipped_armor"]
        old_data = character["equipped_armor_data"]
        stat, val = parse_item_effect(old_data["effect"])
        apply_stat_effect(character, stat, -val)

        if len(character["inventory"]) >= MAX_INVENTORY_SIZE:
            raise InventoryFullError("No space to return unequipped armor")

        character["inventory"].append(old_id)

    # Equip new armor
    stat, val = parse_item_effect(item_data["effect"])
    apply_stat_effect(character, stat, val)
    character["equipped_armor"] = item_id
    character["equipped_armor_data"] = item_data
    character["inventory"].remove(item_id)

    item_name = item_data.get("name", item_id)
    return "Equipped armor: " + item_name

def unequip_weapon(character):
    """
    Unequip current weapon and return it to inventory.

    Returns weapon ID or None if no weapon equipped.
    """
    if not character.get("equipped_weapon"):
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
    """
    Unequip current armor and return it to inventory.

    Returns armor ID or None if no armor equipped.
    """
    if not character.get("equipped_armor"):
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
    """
    Buy an item from a shop, deduct gold, and add to inventory.

    Raises:
        InsufficientResourcesError: if not enough gold.
        InventoryFullError: if inventory is full.
    """
    cost = item_data["cost"]
    if character["gold"] < cost:
        raise InsufficientResourcesError("Not enough gold")
    if len(character["inventory"]) >= MAX_INVENTORY_SIZE:
        raise InventoryFullError("Inventory full")

    character["gold"] -= cost
    character["inventory"].append(item_id)
    return True

def sell_item(character, item_id, item_data):
    """
    Sell an item from inventory for half its cost.

    Raises:
        ItemNotFoundError: if item is not in inventory.
    """
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
    """
    Convert an effect string like "health:20" into a stat and a value.
    """
    if ":" not in effect_string:
        raise InvalidItemTypeError("Invalid effect format")
    stat, value_str = effect_string.split(":")
    try:
        value = int(value_str)
    except:
        raise InvalidItemTypeError("Effect value must be an integer")
    return stat, value

def apply_stat_effect(character, stat_name, value):
    """
    Apply an effect to a character's stat (e.g., health, strength).
    Ensures health does not exceed max_health.
    """
    character[stat_name] = character.get(stat_name, 0) + value
    if stat_name == "health" and character["health"] > character["max_health"]:
        character["health"] = character["max_health"]

def display_inventory(character, item_data_dict):
    """
    Print all items in the character's inventory with quantities and types.
    """
    print("\n=== INVENTORY ===")
    if not character["inventory"]:
        print("(empty)")
        print("=================\n")
        return

    seen = []
    for item_id in character["inventory"]:
        if item_id not in seen:
            qty = character["inventory"].count(item_id)
            seen.append(item_id)
            item_info = item_data_dict.get(item_id, {})
            name = item_info.get("name", item_id)
            type_name = item_info.get("type", "unknown")
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

