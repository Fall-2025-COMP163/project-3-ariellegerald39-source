"""
COMP 163 - Project 3: Quest Chronicles
Game Data Module - Starter Code

Name: Arielle Gerald

AI Usage: This project was completed with full assistance from Chat GPT. 
I have reviewed and studied the project to ensure understanding.


This module handles loading and validating game data from text files.
"""

import os
from custom_exceptions import (
    InvalidDataFormatError,  # Raised when data in a file is formatted wrong
    MissingDataFileError,    # Raised when a required file does not exist
    CorruptedDataError       # Raised when a file cannot be read or written
)

# ============================================================================
# DATA LOADING FUNCTIONS
# ============================================================================

def load_quests(filename="data/quests.txt"):
    """
    Load all quests from a text file.

    Each quest is separated by a blank line in the file.

    Returns:
        dict: Dictionary of quests where keys are quest IDs
    Raises:
        MissingDataFileError: If the quests file does not exist
        CorruptedDataError: If the file cannot be read
        InvalidDataFormatError: If the data in the file is invalid
    """
    if not os.path.exists(filename):
        raise MissingDataFileError("Quest file not found: " + filename)

    try:
        with open(filename, "r") as f:
            lines = f.readlines()
    except Exception:
        raise CorruptedDataError("Unable to read quest file")

    quests = {}  # Dictionary to hold all quests
    block = []   # Temporary list to hold lines for a single quest

    # Process each line in the file
    for line in lines:
        stripped = line.strip()  # Remove extra spaces

        if stripped == "":
            # Blank line means end of current quest block
            if block:
                quest = parse_quest_block(block)
                validate_quest_data(quest)
                quests[quest["quest_id"]] = quest
                block = []
        else:
            block.append(stripped)

    # Process last block if file does not end with a blank line
    if block:
        quest = parse_quest_block(block)
        validate_quest_data(quest)
        quests[quest["quest_id"]] = quest

    return quests

def load_items(filename="data/items.txt"):
    """
    Load all items from a text file.

    Each item is separated by a blank line in the file.

    Returns:
        dict: Dictionary of items where keys are item IDs
    Raises:
        MissingDataFileError: If the items file does not exist
        CorruptedDataError: If the file cannot be read
        InvalidDataFormatError: If the data in the file is invalid
    """
    if not os.path.exists(filename):
        raise MissingDataFileError("Item file not found: " + filename)

    try:
        with open(filename, "r") as f:
            lines = f.readlines()
    except Exception:
        raise CorruptedDataError("Unable to read item file")

    items = {}
    block = []

    for line in lines:
        stripped = line.strip()
        if stripped == "":
            if block:
                item = parse_item_block(block)
                validate_item_data(item)
                items[item["item_id"]] = item
                block = []
        else:
            block.append(stripped)

    if block:
        item = parse_item_block(block)
        validate_item_data(item)
        items[item["item_id"]] = item

    return items

# ============================================================================
# VALIDATION FUNCTIONS
# ============================================================================

def validate_quest_data(quest_dict):
    """
    Check that a quest has all required fields and correct types.
    """
    required = ["quest_id", "title", "description",
                "reward_xp", "reward_gold", "required_level", "prerequisite"]

    for key in required:
        if key not in quest_dict:
            raise InvalidDataFormatError("Quest missing field: " + key)

    numeric = ["reward_xp", "reward_gold", "required_level"]
    for n in numeric:
        if not isinstance(quest_dict[n], int):
            raise InvalidDataFormatError("Quest field must be a number: " + n)

    return True

def validate_item_data(item_dict):
    """
    Check that an item has all required fields, correct types, and valid type.
    """
    required = ["item_id", "name", "type", "effect", "cost", "description"]

    for key in required:
        if key not in item_dict:
            raise InvalidDataFormatError("Item missing field: " + key)

    if item_dict["type"] not in ["weapon", "armor", "consumable"]:
        raise InvalidDataFormatError("Invalid item type: " + item_dict["type"])

    if not isinstance(item_dict["cost"], int):
        raise InvalidDataFormatError("Item cost must be a number")

    return True

# ============================================================================
# DEFAULT DATA FILE CREATION
# ============================================================================

def create_default_data_files():
    """
    Create a default data folder and sample quests/items if they do not exist.
    """
    if not os.path.exists("data"):
        try:
            os.makedirs("data")
        except Exception:
            raise CorruptedDataError("Cannot create data directory")

    # Default quest file
    if not os.path.exists("data/quests.txt"):
        try:
            with open("data/quests.txt", "w") as f:
                f.write(
                    "QUEST_ID: start\n"
                    "TITLE: First Steps\n"
                    "DESCRIPTION: Your adventure begins.\n"
                    "REWARD_XP: 50\n"
                    "REWARD_GOLD: 20\n"
                    "REQUIRED_LEVEL: 1\n"
                    "PREREQUISITE: NONE\n\n"
                )
        except Exception:
            raise CorruptedDataError("Could not write quests.txt")

    # Default items file
    if not os.path.exists("data/items.txt"):
        try:
            with open("data/items.txt", "w") as f:
                f.write(
                    "ITEM_ID: potion_small\n"
                    "NAME: Small Potion\n"
                    "TYPE: consumable\n"
                    "EFFECT: health:20\n"
                    "COST: 25\n"
                    "DESCRIPTION: Restores 20 HP.\n\n"
                )
        except Exception:
            raise CorruptedDataError("Could not write items.txt")

# ============================================================================
# PARSING HELPER FUNCTIONS
# ============================================================================

def parse_quest_block(lines):
    """
    Convert a list of lines from the quest file into a dictionary.
    """
    quest = {}
    for line in lines:
        if ":" not in line:
            raise InvalidDataFormatError("Invalid quest line: " + line)

        key, value = line.split(":", 1)
        key = key.strip()
        value = value.strip()

        # Map file keys to dictionary keys
        if key == "QUEST_ID":
            quest["quest_id"] = value
        elif key == "TITLE":
            quest["title"] = value
        elif key == "DESCRIPTION":
            quest["description"] = value
        elif key == "REWARD_XP":
            try:
                quest["reward_xp"] = int(value)
            except:
                raise InvalidDataFormatError("REWARD_XP must be a number")
        elif key == "REWARD_GOLD":
            try:
                quest["reward_gold"] = int(value)
            except:
                raise InvalidDataFormatError("REWARD_GOLD must be a number")
        elif key == "REQUIRED_LEVEL":
            try:
                quest["required_level"] = int(value)
            except:
                raise InvalidDataFormatError("REQUIRED_LEVEL must be a number")
        elif key == "PREREQUISITE":
            quest["prerequisite"] = value
        else:
            raise InvalidDataFormatError("Unknown quest field: " + key)

    return quest

def parse_item_block(lines):
    """
    Convert a list of lines from the items file into a dictionary.
    """
    item = {}
    for line in lines:
        if ":" not in line:
            raise InvalidDataFormatError("Invalid item line: " + line)

        key, value = line.split(":", 1)
        key = key.strip()
        value = value.strip()

        if key == "ITEM_ID":
            item["item_id"] = value
        elif key == "NAME":
            item["name"] = value
        elif key == "TYPE":
            item["type"] = value
        elif key == "EFFECT":
            item["effect"] = value  # Store effect as raw string like "health:20"
        elif key == "COST":
            try:
                item["cost"] = int(value)
            except:
                raise InvalidDataFormatError("COST must be a number")
        elif key == "DESCRIPTION":
            item["description"] = value
        else:
            raise InvalidDataFormatError("Unknown item field: " + key)

    return item

# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":
    print("=== GAME DATA MODULE TEST ===")
    
    # Test creating default files
    # create_default_data_files()
    
    # Test loading quests
    # try:
    #     quests = load_quests()
    #     print(f"Loaded {len(quests)} quests")
    # except MissingDataFileError:
    #     print("Quest file not found")
    # except InvalidDataFormatError as e:
    #     print(f"Invalid quest format: {e}")
    
    # Test loading items
    # try:
    #     items = load_items()
    #     print(f"Loaded {len(items)} items")
    # except MissingDataFileError:
    #     print("Item file not found")
    # except InvalidDataFormatError as e:
    #     print(f"Invalid item format: {e}")

