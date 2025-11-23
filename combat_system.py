"""
COMP 163 - Project 3: Quest Chronicles
Combat System Module - Starter Code

Name: Arielle Gerald

AI Usage: This project was completed with full assistance from Chat GPT. 
I have reviewed and studied the project to ensure understanding.


Handles combat mechanics
"""
import random # Used for random numbers

from custom_exceptions import (
    InvalidTargetError,
    CombatNotActiveError,
    CharacterDeadError,
    AbilityOnCooldownError
)

# ============================================================================
# ENEMY DEFINITIONS
# ============================================================================

def create_enemy(enemy_type):
    """
    Make a new enemy with health, strength, magic, XP, and gold.
    
    Arguments:
        enemy_type (str): Type of enemy ("goblin", "orc", "dragon")
    
    Returns:
        dict: Enemy info in a dictionary
    
    Raises:
        InvalidTargetError: If the enemy type is unknown
    """
    # Set stats depending on the type of enemy
    if enemy_type == "goblin":
        health, strength, magic, xp, gold = 50, 8, 2, 25, 10
    elif enemy_type == "orc":
        health, strength, magic, xp, gold = 80, 12, 5, 50, 25
    elif enemy_type == "dragon":
        health, strength, magic, xp, gold = 200, 25, 15, 200, 100
    else:
        raise InvalidTargetError("Unknown enemy type: " + enemy_type)

    # Save enemy info in a dictionary
    enemy = {
        "name": enemy_type.capitalize(),  # Capitalize first letter
        "health": health,
        "max_health": health,
        "strength": strength,
        "magic": magic,
        "xp_reward": xp,
        "gold_reward": gold
    }

    return enemy

def get_random_enemy_for_level(character_level):
    """
    Choose an enemy depending on the player's level.
    
    Arguments:
        character_level (int): Level of the character
    
    Returns:
        dict: Random enemy info
    """
    if character_level <= 2:
        return create_enemy("goblin")
    elif character_level <= 5:
        return create_enemy("orc")
    else:
        return create_enemy("dragon")

# ============================================================================
# COMBAT SYSTEM
# ============================================================================

class SimpleBattle:
    """
    This is a turn-based battle system.

    Player and enemy take turns attacking each other until one dies.
    """
    
    def __init__(self, character, enemy):
        """
        Prepare the battle with a character and an enemy.
        """
        self.character = character  # The player
        self.enemy = enemy  # The enemy
        self.combat_active = True  # Battle is ongoing
        self.turn_count = 0  # Count of turns
    
    def start_battle(self):
        """
        Start the battle loop.
        Player and enemy attack each other until one dies or player escapes.

        Returns:
            dict: Battle results including winner, XP gained, gold gained
        """
        # Player cannot fight if already dead
        if self.character["health"] <= 0:
            raise CharacterDeadError("Character is dead")

        # Main loop: continue until combat ends
        while self.combat_active:
            display_combat_stats(self.character, self.enemy)

            # Player's turn
            self.player_turn()
            if not self.combat_active:
                break

            if self.check_battle_end() is not None:
                self.combat_active = False
                break

            # Enemy's turn
            self.enemy_turn()
            if self.check_battle_end() is not None:
                self.combat_active = False
                break

        # Determine winner and rewards
        winner = self.check_battle_end()
        if winner == "player":
            rewards = get_victory_rewards(self.enemy)
            return {"winner": "player", "xp_gained": rewards["xp"], "gold_gained": rewards["gold"]}
        return {"winner": "enemy", "xp_gained": 0, "gold_gained": 0}
    
    def player_turn(self):
        """
        Let the player take an action: attack, use special ability, or run.
        """
        if not self.combat_active:
            raise CombatNotActiveError("Combat not active")

        display_battle_log("Your turn!")
        display_battle_log("1. Basic Attack")
        display_battle_log("2. Special Ability")
        display_battle_log("3. Run")

        choice = input("Choose action: ")

        if choice == "1":
            # Basic attack
            damage = self.calculate_damage(self.character, self.enemy)
            self.apply_damage(self.enemy, damage)
            display_battle_log(f"You dealt {damage} damage!")
        elif choice == "2":
            # Special ability
            result = use_special_ability(self.character, self.enemy)
            display_battle_log(result)
        elif choice == "3":
            # Try to run away
            if self.attempt_escape():
                display_battle_log("You escaped the battle!")
                self.combat_active = False
        else:
            display_battle_log("Invalid choice!")

    def enemy_turn(self):
        """
        Enemy attacks the player.
        """
        if not self.combat_active:
            raise CombatNotActiveError("Combat not active")

        display_battle_log("Enemy attacks!")
        damage = self.calculate_damage(self.enemy, self.character)
        self.apply_damage(self.character, damage)
        display_battle_log(f"{self.enemy['name']} dealt {damage} damage!")

    def calculate_damage(self, attacker, defender):
        """
        Calculate damage: attacker's strength minus 1/4 of defender's strength.
        Minimum damage is always 1.
        """
        damage = attacker["strength"] - (defender["strength"] // 4)
        return max(damage, 1)

    def apply_damage(self, target, damage):
        """
        Subtract damage from target's health. Health cannot go below 0.
        """
        target["health"] = max(target["health"] - damage, 0)

    def check_battle_end(self):
        """
        Check if someone died.
        Returns "player" if player won, "enemy" if enemy won, None otherwise.
        """
        if self.enemy["health"] <= 0:
            return "player"
        if self.character["health"] <= 0:
            return "enemy"
        return None

    def attempt_escape(self):
        """
        Player tries to run away. 50% chance to succeed.
        """
        return random.randint(1, 100) <= 50

# ============================================================================
# SPECIAL ABILITIES
# ============================================================================

def use_special_ability(character, enemy):
    """
    Use the special ability depending on character class.
    """
    cclass = character["class"]

    if cclass == "Warrior":
        return warrior_power_strike(character, enemy)
    elif cclass == "Mage":
        return mage_fireball(character, enemy)
    elif cclass == "Rogue":
        return rogue_critical_strike(character, enemy)
    elif cclass == "Cleric":
        return cleric_heal(character)
    else:
        return "No special ability available."

def warrior_power_strike(character, enemy):
    """
    Warrior deals double strength damage.
    """
    damage = character["strength"] * 2
    enemy["health"] = max(enemy["health"] - damage, 0)
    return f"You used Power Strike for {damage} damage!"

def mage_fireball(character, enemy):
    """
    Mage deals double magic damage.
    """
    damage = character["magic"] * 2
    enemy["health"] = max(enemy["health"] - damage, 0)
    return f"You cast Fireball for {damage} damage!"

def rogue_critical_strike(character, enemy):
    """
    Rogue has 50% chance to deal triple damage, otherwise normal damage.
    """
    if random.randint(1, 100) <= 50:
        damage = character["strength"] * 3
        msg = "Critical hit!"
    else:
        damage = character["strength"]
        msg = "Normal strike."
    enemy["health"] = max(enemy["health"] - damage, 0)
    return f"{msg} You dealt {damage} damage!"

def cleric_heal(character):
    """
    Cleric heals self for 30 HP, cannot exceed max health.
    """
    heal = min(30, character["max_health"] - character["health"])
    character["health"] += heal
    return f"You healed for {heal} HP!"

# ============================================================================
# COMBAT UTILITIES
# ============================================================================

def can_character_fight(character):
    """
    Return True if character has health above 0.
    """
    return character["health"] > 0

def get_victory_rewards(enemy):
    """
    Return the XP and gold from a defeated enemy.
    """
    return {"xp": enemy["xp_reward"], "gold": enemy["gold_reward"]}

def display_combat_stats(character, enemy):
    """
    Print the current health of both player and enemy.
    """
    print(f"\n{character['name']}: HP={character['health']}/{character['max_health']}")
    print(f"{enemy['name']}: HP={enemy['health']}/{enemy['max_health']}")

def display_battle_log(message):
    """
    Print a message for the player to see.
    """
    print(f">>> {message}")
# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":
    print("=== COMBAT SYSTEM TEST ===")
    
    # Test enemy creation
    # try:
    #     goblin = create_enemy("goblin")
    #     print(f"Created {goblin['name']}")
    # except InvalidTargetError as e:
    #     print(f"Invalid enemy: {e}")
    
    # Test battle
    # test_char = {
    #     'name': 'Hero',
    #     'class': 'Warrior',
    #     'health': 120,
    #     'max_health': 120,
    #     'strength': 15,
    #     'magic': 5
    # }
    #
    # battle = SimpleBattle(test_char, goblin)
    # try:
    #     result = battle.start_battle()
    #     print(f"Battle result: {result}")
    # except CharacterDeadError:
    #     print("Character is dead!")

