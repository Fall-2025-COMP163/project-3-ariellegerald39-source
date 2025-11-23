"""
COMP 163 - Project 3: Quest Chronicles
Character Manager Module - Starter Code

Name: Arielle Gerald

AI Usage: This entire file was written with the assistance of AI.

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
    Make a new character with starting stats based on their class.

    Arguments:
        name (str): The character's name.
        character_class (str): Type of character (Warrior, Mage, Rogue, Cleric).

    Returns:
        dict: A box (dictionary) that holds all the character's info.

    Raises:
        InvalidCharacterClassError: If you pick a class that does not exist.
    """
    # Decide starting health, strength, and magic based on the class
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

    # Put all character information into a dictionary
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
        "inventory": [],  # List of items
        "active_quests": [],  # Quests they are currently doing
        "completed_quests": []  # Quests they finished
    }

    return character  # Give back the new character

# ============================================================================
# SAVING A CHARACTER
# ============================================================================

def save_character(character, save_directory="data/save_games"):
    """
    Save your character to a file so you can play later.

    Arguments:
        character (dict): The character info.
        save_directory (str): Folder to store the file.

    Returns:
        bool: True if saved successfully.
    """
    # Make the folder if it doesn't exist
    if not os.path.exists(save_directory):
        os.makedirs(save_directory)

    filename = os.path.join(save_directory, character["name"] + "_save.txt")

    # Open the file for writing
    f = open(filename, "w")

    # Write all character info to the file, one line at a time
    f.write("NAME: " + character["name"] + "\n")
    f.write("CLASS: " + character["class"] + "\n")
    f.write("LEVEL: " + str(character["level"]) + "\n")
    f.write("HEALTH: " + str(character["health"]) + "\n")
    f.write("MAX_HEALTH: " + str(character["max_health"]) + "\n")
    f.write("STRENGTH: " + str(character["strength"]) + "\n")
    f.write("MAGIC: " + str(character["magic"]) + "\n")
    f.write("EXPERIENCE: " + str(character["experience"]) + "\n")
    f.write("GOLD: " + str(character["gold"]) + "\n")

    # Save inventory and quests as comma-separated strings
    f.write("INVENTORY: " + ",".join(character["inventory"]) + "\n")
    f.write("ACTIVE_QUESTS: " + ",".join(character["active_quests"]) + "\n")
    f.write("COMPLETED_QUESTS: " + ",".join(character["completed_quests"]) + "\n")

    f.close()  # Close the file
    return True

# ============================================================================
# LOADING A CHARACTER
# ============================================================================

def load_character(character_name, save_directory="data/save_games"):
    """
    Load a character from a file to play again.

    Arguments:
        character_name (str): Name of the character to load.
        save_directory (str): Folder where files are stored.

    Returns:
        dict: The character information.

    Raises:
        CharacterNotFoundError: File does not exist.
        SaveFileCorruptedError: File can't be read.
        InvalidSaveDataError: File is missing data.
    """
    filename = os.path.join(save_directory, character_name + "_save.txt")

    if not os.path.exists(filename):
        raise CharacterNotFoundError("No save file for " + character_name)

    try:
        f = open(filename, "r")
        lines = f.readlines()
        f.close()
    except Exception:
        raise SaveFileCorruptedError("Could not read save file")

    # Create a dictionary to hold the character info
    data = {}
    for line in lines:
        if ":" not in line:
            raise InvalidSaveDataError("Invalid line: " + line)
        key, value = line.strip().split(":", 1)
        value = value.strip()

        # Convert lists from comma-separated strings
        if key in ["INVENTORY", "ACTIVE_QUESTS", "COMPLETED_QUESTS"]:
            data[key.lower()] = value.split(",") if value else []
        else:
            data[key.lower()] = value

    # Convert numbers from strings to integers
    for n in ["level", "health", "max_health", "strength", "magic", "experience", "gold"]:
        try:
            data[n] = int(data[n])
        except Exception:
            raise InvalidSaveDataError("Invalid number for " + n)

    # Return the final character dictionary
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

# ============================================================================
# OTHER USEFUL FUNCTIONS
# ============================================================================

def gain_experience(character, xp_amount):
    """
    Give experience points to the character.
    Automatically levels up if enough XP.

    Returns:
        int: New level of the character.

    Raises:
        CharacterDeadError: Can't give XP to dead characters.
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
    Give or take gold from the character.
    """
    new_gold = character["gold"] + amount
    if new_gold < 0:
        raise ValueError("Gold cannot be negative")
    character["gold"] = new_gold
    return new_gold

def heal_character(character, amount):
    """
    Heal the character, but not above max health.
    Returns actual health restored.
    """
    before = character["health"]
    after = min(before + amount, character["max_health"])
    character["health"] = after
    return after - before

def is_character_dead(character):
    """
    Return True if the character's health is 0 or less.
    """
    return character["health"] <= 0

def revive_character(character):
    """
    Revive the character to half health (at least 1 HP).
    """
    character["health"] = max(character["max_health"] // 2, 1)
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

