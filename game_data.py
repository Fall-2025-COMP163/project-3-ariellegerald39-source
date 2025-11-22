"""
COMP 163 - Project 3: Quest Chronicles
Game Data Module - Starter Code

Name: Arielle Gerald

AI Usage: [Document any AI assistance used]

This module handles loading and validating game data from text files.
"""

import os
from custom_exceptions import (
    InvalidDataFormatError,
    MissingDataFileError,
    CorruptedDataError
)

# ============================================================================
# DATA LOADING FUNCTIONS
# ============================================================================

def load_quests(filename="data/quests.txt"):
    """
    Load quest data from file.
    """
    if not os.path.exists(filename):
        raise MissingDataFileError("Quest file not found: " + filename)

    try:
        f = open(filename, "r")
        lines = f.readlines()
        f.close()
    except Exception:
        raise CorruptedDataError("Unable to read quest file")

    quests = {}
    block = []

    # Process blocks of text separated by blank lines
    for line in lines:
        stripped = line.strip()

        if stripped == "":
            if len(block) > 0:
                quest = parse_quest_block(block)
                validate_quest_data(quest)
                quests[quest["quest_id"]] = quest
                block = []
        else:
            block.append(stripped)

    # Last block if file does not end with blank line
    if len(block) > 0:
        quest = parse_quest_block(block)
        validate_quest_data(quest)
        quests[quest["quest_id"]] = quest

    return quests


def load_items(filename="data/items.txt"):
    """
    Load item data from file.
    """
    if not os.path.exists(filename):
        raise MissingDataFileError("Item file not found: " + filename)

    try:
        f = open(filename, "r")
        lines = f.readlines()
        f.close()
    except Exception:
        raise CorruptedDataError("Unable to read item file")

    items = {}
    block = []

    for line in lines:
        stripped = line.strip()

        if stripped == "":
            if len(block) > 0:
                item = parse_item_block(block)
                validate_item_data(item)
                items[item["item_id"]] = item
                block = []
        else:
            block.append(stripped)

    if len(block) > 0:
        item = parse_item_block(block)
        validate_item_data(item)
        items[item["item_id"]] = item

    return items

def validate_quest_data(quest_dict):
    required = [
        "quest_id", "title", "description",
        "reward_xp", "reward_gold",
        "required_level", "prerequisite"
    ]

    # Check required keys
    for key in required:
        if key not in quest_dict:
            raise InvalidDataFormatError("Quest missing field: " + key)

    # Check numeric values
    numeric = ["reward_xp", "reward_gold", "required_level"]
    for n in numeric:
        if not isinstance(quest_dict[n], int):
            raise InvalidDataFormatError("Quest field must be number: " + n)

    return True

def validate_item_data(item_dict):
    required = ["item_id", "name", "type", "effect", "cost", "description"]

    for key in required:
        if key not in item_dict:
            raise InvalidDataFormatError("Item missing field: " + key)

    # Validate item type
    if not (item_dict["type"] == "weapon" or
            item_dict["type"] == "armor" or
            item_dict["type"] == "consumable"):
        raise InvalidDataFormatError("Invalid item type: " + item_dict["type"])

    if not isinstance(item_dict["cost"], int):
        raise InvalidDataFormatError("Item cost must be a number")

    return True

def create_default_data_files():
      if not os.path.exists("data"):
        try:
            os.makedirs("data")
        except Exception:
            raise CorruptedDataError("Cannot create data directory")

    # Default quests
      if not os.path.exists("data/quests.txt"):
        try:
            f = open("data/quests.txt", "w")
            f.write(
                "QUEST_ID: start\n"
                "TITLE: First Steps\n"
                "DESCRIPTION: Your adventure begins.\n"
                "REWARD_XP: 50\n"
                "REWARD_GOLD: 20\n"
                "REQUIRED_LEVEL: 1\n"
                "PREREQUISITE: NONE\n\n"
            )
            f.close()
        except Exception:
            raise CorruptedDataError("Could not write quests.txt")

    # Default items
      if not os.path.exists("data/items.txt"):
        try:
            f = open("data/items.txt", "w")
            f.write(
                "ITEM_ID: potion_small\n"
                "NAME: Small Potion\n"
                "TYPE: consumable\n"
                "EFFECT: health:20\n"
                "COST: 25\n"
                "DESCRIPTION: Restores 20 HP.\n\n"
            )
            f.close()
        except Exception:
            raise CorruptedDataError("Could not write items.txt")

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def parse_quest_block(lines):
    quest = {}

    for line in lines:
        if ":" not in line:
            raise InvalidDataFormatError("Invalid quest line: " + line)

        parts = line.split(":", 1)
        key = parts[0].strip()
        value = parts[1].strip()

        # Convert keys to lowercase-friendly field names
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
                raise InvalidDataFormatError("REWARD_XP must be number")
        elif key == "REWARD_GOLD":
            try:
                quest["reward_gold"] = int(value)
            except:
                raise InvalidDataFormatError("REWARD_GOLD must be number")
        elif key == "REQUIRED_LEVEL":
            try:
                quest["required_level"] = int(value)
            except:
                raise InvalidDataFormatError("REQUIRED_LEVEL must be number")
        elif key == "PREREQUISITE":
            quest["prerequisite"] = value
        else:
            raise InvalidDataFormatError("Unknown quest field: " + key)

    return quest


def parse_item_block(lines):
     item = {}

     for line in lines:
        if ":" not in line:
            raise InvalidDataFormatError("Invalid item line: " + line)

        parts = line.split(":", 1)
        key = parts[0].strip()
        value = parts[1].strip()

        if key == "ITEM_ID":
            item["item_id"] = value
        elif key == "NAME":
            item["name"] = value
        elif key == "TYPE":
            item["type"] = value
        elif key == "EFFECT":
            # effect stored as raw string "stat:value"
            item["effect"] = value
        elif key == "COST":
            try:
                item["cost"] = int(value)
            except:
                raise InvalidDataFormatError("COST must be number")
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

