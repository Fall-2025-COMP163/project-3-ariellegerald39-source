My Game README
Module	Purpose
main.py: Launches the game and handles the main menu and game loop
character_manager.py: Handles character creation, loading, saving, stats, and revives
inventory_system.py: Manages inventory, item usage, equipping weapons/armor, buying/selling
quest_handler.py: Manages quests, prerequisites, completion, and quest statistics
combat_system.py: Handles enemy generation and battle mechanics
game_data.py: Loads game data, validates item and quest files, provides default data
custom_exceptions.py: Defines all custom exceptions used across modules

This modular structure keeps functionality separate, making the code easier to maintain, extend, and test.

Exception Strategy

Custom exceptions are used to clearly signal errors and edge cases:

Inventory Errors:

InventoryFullError → raised when trying to add an item but inventory is full.

ItemNotFoundError → raised when trying to use, equip, sell, or remove an item that isn’t in the inventory.

InvalidItemTypeError → raised when an action is attempted on an incompatible item type.

Resource Errors:

InsufficientResourcesError → raised when a character does not have enough gold or other required resources.

Quest Errors:

QuestNotFoundError → raised when referencing a quest that does not exist in the data.

QuestRequirementsNotMetError → raised when prerequisites or level requirements are unmet.

QuestAlreadyCompletedError → raised if a completed quest is attempted again.

QuestNotActiveError → raised when trying to abandon or complete a quest that isn’t active.

Using exceptions ensures strong error handling and communicates issues clearly to the player or developer.

Design Choices

Modular Architecture: Each module has a single responsibility (combat, inventory, quests), which improves maintainability and readability.

Data-Driven Approach: Items and quests are stored in dictionaries with IDs as keys, allowing easy addition of new content without code changes.

Stat Effects as Strings: Item effects are stored as strings ("health:20") and parsed, allowing flexible stat modifications.

Global Game State: The main.py file maintains the current character and game state, simplifying the main game loop.

Simple Terminal Interface: Prioritized clarity and accessibility for a text-based experience.

AI Usage:

This project was completed with full assistance from ChatGPT. Specific AI assistance included:

Writing starter and complete code for the inventory, quest, and main game modules.

Designing exception handling strategies and modular architecture.

Creating helper functions for quest and item management.

The code was carefully reviewed and tested to ensure full understanding.

How to Play:

Clone the repository and navigate into it:

git clone <repository_url>
cd project-3-ariellegerald39-source


Run the game:

python main.py