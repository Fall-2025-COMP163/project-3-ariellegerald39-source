"""
COMP 163 - Project 3: Quest Chronicles
Main Game Module - Starter Code

Name: Arielle Gerald

AI Usage: This project was completed with full assistance from Chat GPT. 
I have reviewed and studied the project to ensure understanding.


This is the main game file that ties all modules together.
Demonstrates module integration and complete game flow.
"""

# Import all our custom modules
import character_manager
import inventory_system
import quest_handler
import combat_system
import game_data
from custom_exceptions import *

# ============================================================================
# GAME STATE
# ============================================================================

# Global variables for game data
current_character = None
all_quests = {}
all_items = {}
game_running = False

# ============================================================================
# MAIN MENU
# ============================================================================

def main_menu():
    """Display the main menu and get player's choice"""
    print("\n=== MAIN MENU ===")
    print("1. New Game")
    print("2. Load Game")
    print("3. Exit")

    # Get input from the player
    choice = input("Enter choice (1-3): ")

    # Keep asking if input is invalid
    while choice not in ["1", "2", "3"]:
        choice = input("Invalid. Enter 1-3: ")

    # Return the choice as a number
    return int(choice)


def new_game():
    """Start a new game and create a new character"""
    global current_character

    print("\n=== NEW GAME ===")

    # Ask the player for a character name
    name = input("Enter character name: ")

    # Ask the player to choose a class
    print("\nChoose class:")
    print("1. Warrior")
    print("2. Mage")
    print("3. Rogue")

    cls_choice = input("Enter choice (1-3): ")

    # Validate input
    while cls_choice not in ["1", "2", "3"]:
        cls_choice = input("Invalid. Enter 1-3: ")

    # Convert number to class name
    if cls_choice == "1":
        character_class = "warrior"
    elif cls_choice == "2":
        character_class = "mage"
    else:
        character_class = "rogue"

    # Try to create the character
    try:
        current_character = character_manager.create_character(name, character_class)
        print("\nCharacter created successfully!\n")
        game_loop()  # Start the game loop
    except InvalidCharacterClassError:
        print("\nInvalid class selected.\n")


def load_game():
    """Load an existing saved game"""
    global current_character

    print("\n=== LOAD GAME ===")

    # Get list of saved characters
    saves = character_manager.list_saved_characters()

    # If no saves found
    if len(saves) == 0:
        print("No saved games found.")
        return

    # Display saved characters
    print("\nSaved characters:")
    index = 1
    for s in saves:
        print(str(index) + ". " + s)
        index += 1

    # Ask player to choose a save
    choice = input("Choose a character: ")

    # Validate input
    while not choice.isdigit() or int(choice) < 1 or int(choice) > len(saves):
        choice = input("Invalid. Choose again: ")

    # Load the selected character
    name = saves[int(choice) - 1]
    try:
        current_character = character_manager.load_character(name)
        print("\nGame loaded!\n")
        game_loop()  # Start the game loop
    except CharacterNotFoundError:
        print("Save not found.")
    except SaveFileCorruptedError:
        print("Save file corrupted.")


# ============================================================================ 
# GAME LOOP FUNCTIONS
# ============================================================================

def game_loop():
    """The main in-game loop where the player chooses actions"""
    global game_running

    game_running = True

    while game_running:
        choice = game_menu()

        # Perform actions based on player's choice
        if choice == 1:
            view_character_stats()
        elif choice == 2:
            view_inventory()
        elif choice == 3:
            quest_menu()
        elif choice == 4:
            explore()
        elif choice == 5:
            shop()
        elif choice == 6:
            save_game()
            print("Game saved. Returning to main menu.")
            game_running = False


def game_menu():
    """Display the in-game menu and get player's choice"""
    print("\n=== GAME MENU ===")
    print("1. View Character Stats")
    print("2. View Inventory")
    print("3. Quest Menu")
    print("4. Explore")
    print("5. Shop")
    print("6. Save and Quit")

    choice = input("Enter choice: ")

    # Validate input
    while choice not in ["1","2","3","4","5","6"]:
        choice = input("Invalid. Enter 1-6: ")

    return int(choice)


# ============================================================================ 
# GAME ACTION FUNCTIONS
# ============================================================================

def view_character_stats():
    """Display the character's stats and quest progress"""
    global current_character

    print("\n=== CHARACTER STATS ===")
    character_manager.display_character(current_character)

    print("\nActive quests:")
    quest_handler.display_active_quests(current_character, all_quests)

    print("\nCompleted quests:")
    quest_handler.display_completed_quests(current_character, all_quests)


def view_inventory():
    """Display inventory and allow the player to interact with items"""
    global current_character, all_items

    print("\n=== INVENTORY ===")
    inventory_system.display_inventory(current_character, all_items)

    # Inventory options
    print("Options:")
    print("1. Use item")
    print("2. Equip weapon")
    print("3. Equip armor")
    print("4. Drop item")
    print("5. Back")

    choice = input("Enter choice: ")

    # Handle player's choice
    if choice == "1":
        item = input("Enter item ID to use: ")
        if item in all_items:
            try:
                result = inventory_system.use_item(current_character, item, all_items[item])
                print(result)
            except Exception as e:
                print("Error:", e)
        else:
            print("Unknown item.")
    elif choice == "2":
        item = input("Enter weapon ID: ")
        if item in all_items:
            try:
                print(inventory_system.equip_weapon(current_character, item, all_items[item]))
            except Exception as e:
                print("Error:", e)
    elif choice == "3":
        item = input("Enter armor ID: ")
        if item in all_items:
            try:
                print(inventory_system.equip_armor(current_character, item, all_items[item]))
            except Exception as e:
                print("Error:", e)
    elif choice == "4":
        item = input("Enter item ID to drop: ")
        try:
            inventory_system.remove_item_from_inventory(current_character, item)
            print("Item dropped.")
        except Exception as e:
            print("Error:", e)


def quest_menu():
    """Display quest options and allow the player to manage quests"""
    global current_character, all_quests

    print("\n=== QUEST MENU ===")
    print("1. View Active Quests")
    print("2. View Available Quests")
    print("3. View Completed Quests")
    print("4. Accept Quest")
    print("5. Abandon Quest")
    print("6. Complete Quest (DEBUG)")
    print("7. Back")

    choice = input("Enter choice: ")

    # Perform actions based on choice
    if choice == "1":
        quest_handler.display_active_quests(current_character, all_quests)
    elif choice == "2":
        quest_handler.display_available_quests(current_character, all_quests)
    elif choice == "3":
        quest_handler.display_completed_quests(current_character, all_quests)
    elif choice == "4":
        q = input("Enter quest ID: ")
        try:
            quest_handler.accept_quest(current_character, q, all_quests)
            print("Quest accepted!")
        except Exception as e:
            print("Error:", e)
    elif choice == "5":
        q = input("Enter quest ID: ")
        try:
            quest_handler.abandon_quest(current_character, q)
            print("Quest abandoned.")
        except Exception as e:
            print("Error:", e)
    elif choice == "6":
        q = input("Enter quest ID: ")
        try:
            quest_handler.complete_quest(current_character, q, all_quests)
            print("Quest completed!")
        except Exception as e:
            print("Error:", e)


def explore():
    """Handle exploration and battles in the wild"""
    global current_character

    print("\nYou venture into the wilderness...")

    # Generate an enemy based on player's level
    enemy = combat_system.generate_enemy(current_character["level"])
    print("A wild " + enemy["name"] + " appears!")

    # Start a battle
    battle = combat_system.SimpleBattle(current_character, enemy)
    result = battle.start()

    print(result)

    # Check if character died
    if result == "defeat":
        handle_character_death()


def shop():
    """Allow the player to buy and sell items"""
    global current_character, all_items

    print("\n=== SHOP ===")

    print("Your gold:", current_character["gold"])
    print("\nItems for sale:")

    # Display all items for sale
    for item_id in all_items:
        item = all_items[item_id]
        print(item_id + " - " + item["name"] + " (" + str(item["cost"]) + "g)")

    # Shop options
    print("\nOptions:")
    print("1. Buy item")
    print("2. Sell item")
    print("3. Back")

    choice = input("Enter choice: ")

    # Handle buying items
    if choice == "1":
        item_id = input("Enter item ID to buy: ")
        if item_id in all_items:
            try:
                inventory_system.purchase_item(current_character, item_id, all_items[item_id])
                print("Purchased " + all_items[item_id]["name"])
            except Exception as e:
                print("Error:", e)
        else:
            print("Unknown item.")
    # Handle selling items
    elif choice == "2":
        item_id = input("Enter item ID to sell: ")
        if item_id in all_items:
            try:
                gold = inventory_system.sell_item(current_character, item_id, all_items[item_id])
                print("Sold for", gold, "gold.")
            except Exception as e:
                print("Error:", e)


# ============================================================================ 
# HELPER FUNCTIONS
# ============================================================================

def save_game():
    """Save the current character's progress"""
    global current_character

    try:
        character_manager.save_character(current_character)
        print("Game saved.")
    except Exception:
        print("Error saving game.")


def load_game_data():
    """Load all game quests and items"""
    global all_quests, all_items

    try:
        all_quests = game_data.load_quests()
        all_items = game_data.load_items()
    except MissingDataFileError:
        raise
    except InvalidDataFormatError:
        raise


def handle_character_death():
    """Handle what happens when the character dies"""
    global current_character, game_running

    print("\nYou have died!")

    # Offer options to revive or quit
    print("1. Revive (25 gold)")
    print("2. Quit")

    choice = input("Enter choice: ")

    if choice == "1":
        try:
            character_manager.revive_character(current_character)
            print("You have been revived!")
        except InsufficientResourcesError:
            print("Not enough gold. Game over.")
            game_running = False
    else:
        game_running = False


def display_welcome():
    """Display welcome message when game starts"""
    print("=" * 50)
    print("     QUEST CHRONICLES - A MODULAR RPG ADVENTURE")
    print("=" * 50)
    print("\nWelcome to Quest Chronicles!")
    print("Build your character, complete quests, and become a legend!\n")


# ============================================================================ 
# MAIN EXECUTION
# ============================================================================

def main():
    """Main game execution function"""
    # Display welcome message
    display_welcome()

    # Load game data
    try:
        load_game_data()
        print("Game data loaded successfully!")
    except MissingDataFileError:
        print("Creating default game data...")
        game_data.create_default_data_files()
        load_game_data()
    except InvalidDataFormatError as e:
        print(f"Error loading game data: {e}")
        print("Please check data files for errors.")
        return

    # Main menu loop
    while True:
        choice = main_menu()

        if choice == 1:
            new_game()
        elif choice == 2:
            load_game()
        elif choice == 3:
            print("\nThanks for playing Quest Chronicles!")
            break
        else:
            print("Invalid choice. Please select 1-3.")


if __name__ == "__main__":
    main()

