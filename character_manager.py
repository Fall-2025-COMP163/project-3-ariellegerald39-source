"""
COMP 163 - Project 3: Quest Chronicles
Character Manager Module - Starter Code

Name: [Your Name Here]

AI Usage: [Document any AI assistance used]

This module handles character creation, loading, and saving.
"""

import os
from custom_exceptions import (
    InvalidCharacterClassError,
    CharacterNotFoundError,
    SaveFileCorruptedError,
    InvalidSaveDataError,
    CharacterDeadError
)

# ============================================================================
# CHARACTER MANAGEMENT FUNCTIONS
# ============================================================================

def create_character(name, character_class):
    """
    Create a new character with stats based on class
    
    Valid classes: Warrior, Mage, Rogue, Cleric
    """
    if character_class == "Warrior":
        health = 120
        strength = 15
        magic = 5
    elif character_class == "Mage":
        health = 80
        strength = 8
        magic = 20
    elif character_class == "Rogue":
        health = 90
        strength = 12
        magic = 10
    elif character_class == "Cleric":
        health = 100
        strength = 10
        magic = 15
    else:
        raise InvalidCharacterClassError("Invalid class: " + character_class)

    character = {}
    character["name"] = name
    character["class"] = character_class
    character["level"] = 1
    character["health"] = health
    character["max_health"] = health
    character["strength"] = strength
    character["magic"] = magic
    character["experience"] = 0
    character["gold"] = 100
    character["inventory"] = []
    character["active_quests"] = []
    character["completed_quests"] = []

    return character


def save_character(character, save_directory="data/save_games"):
    if not os.path.exists(save_directory):
        os.makedirs(save_directory)

    filename = os.path.join(save_directory, character["name"] + "_save.txt")

    try:
        f = open(filename, "w")

        f.write("NAME: " + character["name"] + "\n")
        f.write("CLASS: " + character["class"] + "\n")
        f.write("LEVEL: " + str(character["level"]) + "\n")
        f.write("HEALTH: " + str(character["health"]) + "\n")
        f.write("MAX_HEALTH: " + str(character["max_health"]) + "\n")
        f.write("STRENGTH: " + str(character["strength"]) + "\n")
        f.write("MAGIC: " + str(character["magic"]) + "\n")
        f.write("EXPERIENCE: " + str(character["experience"]) + "\n")
        f.write("GOLD: " + str(character["gold"]) + "\n")

        inventory_str = ""
        for i in range(len(character["inventory"])):
            if i > 0:
                inventory_str += ","
            inventory_str += character["inventory"][i]

        active_str = ""
        for i in range(len(character["active_quests"])):
            if i > 0:
                active_str += ","
            active_str += character["active_quests"][i]

        completed_str = ""
        for i in range(len(character["completed_quests"])):
            if i > 0:
                completed_str += ","
            completed_str += character["completed_quests"][i]

        f.write("INVENTORY: " + inventory_str + "\n")
        f.write("ACTIVE_QUESTS: " + active_str + "\n")
        f.write("COMPLETED_QUESTS: " + completed_str + "\n")

        f.close()

    except Exception:
        raise

    return True


def load_character(character_name, save_directory="data/save_games"):
    filename = os.path.join(save_directory, character_name + "_save.txt")

    if not os.path.exists(filename):
        raise CharacterNotFoundError("No save file for " + character_name)

    try:
        f = open(filename, "r")
        lines = f.readlines()
        f.close()
    except Exception:
        raise SaveFileCorruptedError("Could not read save file")

    data = {}

    # Parse manually with loops
    for line in lines:
        if ":" not in line:
            raise InvalidSaveDataError("Invalid line: " + line)

        parts = line.strip().split(":", 1)
        key = parts[0]
        value = parts[1].strip()

        if key in ["INVENTORY", "ACTIVE_QUESTS", "COMPLETED_QUESTS"]:
            if value == "":
                data[key.lower()] = []
            else:
                items = value.split(",")
                real = []
                for it in items:
                    real.append(it)
                data[key.lower()] = real
        else:
            data[key.lower()] = value

    # Convert types manually
    numeric = ["level", "health", "max_health", "strength",
               "magic", "experience", "gold"]

    for n in numeric:
        try:
            data[n] = int(data[n])
        except Exception:
            raise InvalidSaveDataError("Invalid number for " + n)

    character = {}
    character["name"] = data["name"]
    character["class"] = data["class"]
    character["level"] = data["level"]
    character["health"] = data["health"]
    character["max_health"] = data["max_health"]
    character["strength"] = data["strength"]
    character["magic"] = data["magic"]
    character["experience"] = data["experience"]
    character["gold"] = data["gold"]
    character["inventory"] = data["inventory"]
    character["active_quests"] = data["active_quests"]
    character["completed_quests"] = data["completed_quests"]

    return character


def list_saved_characters(save_directory="data/save_games"):
    if not os.path.exists(save_directory):
        return []

    names = []
    files = os.listdir(save_directory)

    for filename in files:
        if filename.endswith("_save.txt"):
            clean = filename.replace("_save.txt", "")
            names.append(clean)

    return names


def delete_character(character_name, save_directory="data/save_games"):
    filename = os.path.join(save_directory, character_name + "_save.txt")

    if not os.path.exists(filename):
        raise CharacterNotFoundError("Character not found")

    os.remove(filename)
    return True

# ============================================================================
# CHARACTER OPERATIONS
# ============================================================================

def gain_experience(character, xp_amount):
    if character["health"] <= 0:
        raise CharacterDeadError("Character is dead")

    character["experience"] += xp_amount

    leveled = True
    while leveled:
        leveled = False
        needed = character["level"] * 100

        if character["experience"] >= needed:
            character["experience"] = character["experience"] - needed
            character["level"] = character["level"] + 1
            character["max_health"] = character["max_health"] + 10
            character["strength"] = character["strength"] + 2
            character["magic"] = character["magic"] + 2
            character["health"] = character["max_health"]
            leveled = True

    return character["level"]


def add_gold(character, amount):
    new_total = character["gold"] + amount

    if new_total < 0:
        raise ValueError("Gold cannot be negative")

    character["gold"] = new_total
    return new_total


def heal_character(character, amount):
    before = character["health"]
    after = before + amount

    if after > character["max_health"]:
        after = character["max_health"]

    character["health"] = after
    return after - before


def is_character_dead(character):
    if character["health"] <= 0:
        return True
    return False


def revive_character(character):
    half = character["max_health"] // 2
    if half < 1:
        half = 1
    character["health"] = half
    return True

# ============================================================================
# VALIDATION
# ============================================================================

def validate_character_data(character):
    """
    Validate that character dictionary has all required fields
    
    Required fields: name, class, level, health, max_health, 
                    strength, magic, experience, gold, inventory,
                    active_quests, completed_quests
    
    Returns: True if valid
    Raises: InvalidSaveDataError if missing fields or invalid types
    """
    # TODO: Implement validation
    # Check all required keys exist
    # Check that numeric values are numbers
    # Check that lists are actually lists
    pass

# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":
    print("=== CHARACTER MANAGER TEST ===")
    
    # Test character creation
    # try:
    #     char = create_character("TestHero", "Warrior")
    #     print(f"Created: {char['name']} the {char['class']}")
    #     print(f"Stats: HP={char['health']}, STR={char['strength']}, MAG={char['magic']}")
    # except InvalidCharacterClassError as e:
    #     print(f"Invalid class: {e}")
    
    # Test saving
    # try:
    #     save_character(char)
    #     print("Character saved successfully")
    # except Exception as e:
    #     print(f"Save error: {e}")
    
    # Test loading
    # try:
    #     loaded = load_character("TestHero")
    #     print(f"Loaded: {loaded['name']}")
    # except CharacterNotFoundError:
    #     print("Character not found")
    # except SaveFileCorruptedError:
    #     print("Save file corrupted")

