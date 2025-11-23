"""
COMP 163 - Project 3: Quest Chronicles
Character Manager Module - Starter Code

Name: Arielle Gerald

AI Usage: This project was completed with full assistance from Chat GPT. 
I have reviewed and studied the project to ensure understanding.

This module handles character creation, loading, and saving.
"""

import os # This allows us to work with files on the computer
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
    Make a new character with starting stats based on class.

    Args:
        name (str): The name of the character.
        character_class (str): Type of character (Warrior, Mage, Rogue, Cleric).

    Returns:
        dict: All the character's info stored in a dictionary.

    Raises:
        InvalidCharacterClassError: If class is not valid.
    """
    # Set starting stats for each class
    if character_class == "Warrior":
        health, strength, magic = 120, 15, 5
    elif character_class == "Mage":
        health, strength, magic = 80, 8, 20
    elif character_class == "Rogue":
        health, strength, magic = 90, 12, 10
    elif character_class == "Cleric":
        health, strength, magic = 100, 10, 15
    else:
        # If the class is not valid, stop and tell the player
        raise InvalidCharacterClassError(f"Invalid class: {character_class}")

    # Put all information into a dictionary (like a box to hold everything)
    character = {
        "name": name,
        "class": character_class,
        "level": 1,
        "health": health,
        "max_health": health,
        "strength": strength,
        "magic": magic,
        "experience": 0,
        "gold": 100,
        "inventory": [],          # Items the character owns
        "active_quests": [],      # Quests the character is doing
        "completed_quests": []    # Quests the character finished
    }
    return character

# ============================================================================ 
# SAVE, LOAD, DELETE FUNCTIONS
# ============================================================================ 

def save_character(character, save_directory="data/save_games"):
    """
    Save the character to a file so we can load it later.

    Args:
        character (dict): Character info.
        save_directory (str): Folder to save the file.

    Returns:
        bool: True if saved successfully.
    """
    # Make the folder if it does not exist
    if not os.path.exists(save_directory):
        os.makedirs(save_directory)

    filename = os.path.join(save_directory, character["name"] + "_save.txt")

    try:
        # Open the file for writing (this will create the file)
        f = open(filename, "w")

        # Save each piece of info as text
        f.write("NAME: " + character["name"] + "\n")
        f.write("CLASS: " + character["class"] + "\n")
        f.write("LEVEL: " + str(character["level"]) + "\n")
        f.write("HEALTH: " + str(character["health"]) + "\n")
        f.write("MAX_HEALTH: " + str(character["max_health"]) + "\n")
        f.write("STRENGTH: " + str(character["strength"]) + "\n")
        f.write("MAGIC: " + str(character["magic"]) + "\n")
        f.write("EXPERIENCE: " + str(character["experience"]) + "\n")
        f.write("GOLD: " + str(character["gold"]) + "\n")

        # Save lists as comma-separated strings
        f.write("INVENTORY: " + ",".join(character["inventory"]) + "\n")
        f.write("ACTIVE_QUESTS: " + ",".join(character["active_quests"]) + "\n")
        f.write("COMPLETED_QUESTS: " + ",".join(character["completed_quests"]) + "\n")

        f.close()  # Close the file
        return True
    except Exception:
        return False

def load_character(character_name, save_directory="data/save_games"):
    """
    Load a character from a save file so we can play again.

    Args:
        character_name (str): Name of the character.
        save_directory (str): Folder where the file is.

    Returns:
        dict: Character info.

    Raises:
        CharacterNotFoundError: File does not exist.
        SaveFileCorruptedError: File cannot be read.
        InvalidSaveDataError: File has missing or wrong data.
    """
    filename = os.path.join(save_directory, character_name + "_save.txt")
    if not os.path.exists(filename):
        raise CharacterNotFoundError(f"No save file for {character_name}")

    try:
        f = open(filename, "r")
        lines = f.readlines()
        f.close()
    except Exception:
        raise SaveFileCorruptedError("Could not read save file")

    data = {}
    for line in lines:
        if ":" not in line:
            raise InvalidSaveDataError(f"Invalid line: {line}")
        key, value = line.strip().split(":", 1)
        value = value.strip()

        # Turn comma-separated lists back into lists
        if key in ["INVENTORY", "ACTIVE_QUESTS", "COMPLETED_QUESTS"]:
            data[key.lower()] = value.split(",") if value else []
        else:
            data[key.lower()] = value

    # Convert numbers from text to actual numbers
    for field in ["level", "health", "max_health", "strength", "magic", "experience", "gold"]:
        try:
            data[field] = int(data[field])
        except Exception:
            raise InvalidSaveDataError(f"Invalid number for {field}")

    return {
        "name": data["name"],
        "class": data["class"],
        "level": data["level"],
        "health": data["health"],
        "max_health": data["max_health"],
        "strength": data["strength"],
        "magic": data["magic"],
        "experience": data["experience"],
        "gold": data["gold"],
        "inventory": data["inventory"],
        "active_quests": data["active_quests"],
        "completed_quests": data["completed_quests"]
    }

def delete_character(character_name, save_directory="data/save_games"):
    """
    Delete a character's save file (used for cleanup).

    Args:
        character_name (str): Name of the character.
        save_directory (str): Folder where the file is.

    Returns:
        bool: True if file deleted, False if not found.
    """
    filename = os.path.join(save_directory, character_name + "_save.txt")
    if os.path.exists(filename):
        try:
            os.remove(filename)
            return True
        except Exception:
            return False
    return False

# ============================================================================ 
# CHARACTER PROGRESSION
# ============================================================================ 

def gain_experience(character, xp_amount):
    """
    Give experience points to a character and level up if needed.

    Args:
        character (dict): Character info.
        xp_amount (int): Amount of XP to add.

    Returns:
        int: New level of the character.

    Raises:
        CharacterDeadError: Cannot give XP to a dead character.
    """
    if character["health"] <= 0:
        raise CharacterDeadError("Character is dead")

    character["experience"] += xp_amount

    # Keep leveling up as long as XP is enough
    while character["experience"] >= character["level"] * 100:
        character["experience"] -= character["level"] * 100
        character["level"] += 1
        character["max_health"] += 10
        character["strength"] += 2
        character["magic"] += 2
        character["health"] = character["max_health"]

    return character["level"]

def add_gold(character, amount):
    """
    Add or remove gold from a character.

    Args:
        character (dict): Character info.
        amount (int): Gold to add (or remove if negative).

    Returns:
        int: Updated gold amount.

    Raises:
        ValueError: If gold would go below 0.
    """
    new_gold = character["gold"] + amount
    if new_gold < 0:
        raise ValueError("Gold cannot be negative")
    character["gold"] = new_gold
    return new_gold

def heal_character(character, amount):
    """
    Heal a character but not above their maximum health.

    Args:
        character (dict): Character info.
        amount (int): Amount to heal.

    Returns:
        int: How much health was actually restored.
    """
    before = character["health"]
    character["health"] = min(before + amount, character["max_health"])
    return character["health"] - before

def is_character_dead(character):
    """
    Check if a character is dead.

    Args:
        character (dict): Character info.

    Returns:
        bool: True if health is 0 or less.
    """
    return character["health"] <= 0

def revive_character(character):
    """
    Revive a dead character to half health (at least 1).

    Args:
        character (dict): Character info.

    Returns:
        bool: True if revival successful.
    """
    character["health"] = max(character["max_health"] // 2, 1)
    return True

# ============================================================================ 
# VALIDATION
# ============================================================================ 

def validate_character_data(character):
    """
    Make sure the character has all required fields with correct types.

    Args:
        character (dict): Character info.

    Returns:
        bool: True if valid.

    Raises:
        InvalidSaveDataError: If any field is missing or wrong type.
    """
    required_fields = [
        "name", "class", "level", "health", "max_health",
        "strength", "magic", "experience", "gold",
        "inventory", "active_quests", "completed_quests"
    ]

    for field in required_fields:
        if field not in character:
            raise InvalidSaveDataError(f"Missing field: {field}")

    for list_field in ["inventory", "active_quests", "completed_quests"]:
        if not isinstance(character[list_field], list):
            raise InvalidSaveDataError(f"{list_field} must be a list")

    for int_field in ["level", "health", "max_health", "strength", "magic", "experience", "gold"]:
        if not isinstance(character[int_field], int):
            raise InvalidSaveDataError(f"{int_field} must be a number")

    return True

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

