"""
COMP 163 - Project 3: Quest Chronicles
Combat System Module - Starter Code

Name: Arielle Gerald

AI Usage: [Document any AI assistance used]

Handles combat mechanics
"""
import random

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
    Create an enemy based on type
    """
    if enemy_type == "goblin":
        health = 50
        strength = 8
        magic = 2
        xp = 25
        gold = 10
    elif enemy_type == "orc":
        health = 80
        strength = 12
        magic = 5
        xp = 50
        gold = 25
    elif enemy_type == "dragon":
        health = 200
        strength = 25
        magic = 15
        xp = 200
        gold = 100
    else:
        raise InvalidTargetError("Unknown enemy type: " + enemy_type)

    enemy = {}
    enemy["name"] = enemy_type
    enemy["health"] = health
    enemy["max_health"] = health
    enemy["strength"] = strength
    enemy["magic"] = magic
    enemy["xp_reward"] = xp
    enemy["gold_reward"] = gold

    return enemy


def get_random_enemy_for_level(character_level):
    """
    Select enemy type based on character level.
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
    Simple turn-based combat system
    
    Manages combat between character and enemy
    """
    
    def __init__(self, character, enemy):
        """Initialize battle with character and enemy"""
        self.character = character
        self.enemy = enemy
        self.combat_active = True
        self.turn_count = 0
    
    
    def start_battle(self):
        if self.character["health"] <= 0:
            raise CharacterDeadError("Character is dead")

        while self.combat_active:
            display_combat_stats(self.character, self.enemy)

            # Player turn
            self.player_turn()
            if not self.combat_active:
                break

            winner = self.check_battle_end()
            if winner is not None:
                self.combat_active = False
                break

            # Enemy turn
            self.enemy_turn()

            winner = self.check_battle_end()
            if winner is not None:
                self.combat_active = False
                break

        # Determine results
        winner = self.check_battle_end()
        if winner == "player":
            rewards = get_victory_rewards(self.enemy)
            return {"winner": "player", 
                    "xp_gained": rewards["xp"], 
                    "gold_gained": rewards["gold"]}

        return {"winner": "enemy", "xp_gained": 0, "gold_gained": 0}
    
    def player_turn(self):
        if not self.combat_active:
            raise CombatNotActiveError("Combat not active")

        display_battle_log("Your turn!")
        display_battle_log("1. Basic Attack")
        display_battle_log("2. Special Ability")
        display_battle_log("3. Run")

        choice = input("Choose action: ")

        if choice == "1":
            damage = self.calculate_damage(self.character, self.enemy)
            self.apply_damage(self.enemy, damage)
            display_battle_log("You dealt " + str(damage) + " damage!")
        elif choice == "2":
            result = use_special_ability(self.character, self.enemy)
            display_battle_log(result)
        elif choice == "3":
            escaped = self.attempt_escape()
            if escaped:
                display_battle_log("You escaped the battle!")
                self.combat_active = False
        else:
            display_battle_log("Invalid choice!")

    def enemy_turn(self):
       if not self.combat_active:
            raise CombatNotActiveError("Combat not active")

       display_battle_log("Enemy attacks!")
       dmg = self.calculate_damage(self.enemy, self.character)
       self.apply_damage(self.character, dmg)
       display_battle_log(self.enemy["name"] + " dealt " + str(dmg) + " damage!")

    
    def calculate_damage(self, attacker, defender):
        """
        Calculate damage from attack
        
        Damage formula: attacker['strength'] - (defender['strength'] // 4)
        Minimum damage: 1
        
        Returns: Integer damage amount
        """
        damage = attacker["strength"] - (defender["strength"] // 4)
        if damage < 1:
            damage = 1
        return damage

    
    def apply_damage(self, target, damage):
        new_hp = target["health"] - damage
        if new_hp < 0:
            new_hp = 0
        target["health"] = new_hp
    
    def check_battle_end(self):
        if self.enemy["health"] <= 0:
            return "player"
        if self.character["health"] <= 0:
            return "enemy"
        return None
    
    def attempt_escape(self):
        roll = random.randint(1, 100)
        if roll <= 50:
            self.combat_active = False
            return True
        return False

# ============================================================================
# SPECIAL ABILITIES
# ============================================================================

def use_special_ability(character, enemy):
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
    base = character["strength"] * 2
    dmg = base
    enemy["health"] = max(0, enemy["health"] - dmg)
    return "You used Power Strike for " + str(dmg) + " damage!"

def mage_fireball(character, enemy):
    dmg = character["magic"] * 2
    enemy["health"] = max(0, enemy["health"] - dmg)
    return "You cast Fireball for " + str(dmg) + " damage!"


def rogue_critical_strike(character, enemy):
    roll = random.randint(1, 100)
    if roll <= 50:
        dmg = character["strength"] * 3
        msg = "Critical hit!"
    else:
        dmg = character["strength"]
        msg = "Normal strike."
    enemy["health"] = max(0, enemy["health"] - dmg)
    return msg + " You dealt " + str(dmg) + " damage!"

def cleric_heal(character):
   heal = 30
   new_hp = character["health"] + heal
   if new_hp > character["max_health"]:
        new_hp = character["max_health"]
   amount = new_hp - character["health"]
   character["health"] = new_hp
   return "You healed for " + str(amount) + " HP!"

# ============================================================================
# COMBAT UTILITIES
# ============================================================================

def can_character_fight(character):
    if character["health"] > 0:
        return True
    return False

def get_victory_rewards(enemy):
    return {"xp": enemy["xp_reward"], "gold": enemy["gold_reward"]}

def display_combat_stats(character, enemy):
     print("\n" + character["name"] + ": HP=" + str(character["health"]) + "/" + str(character["max_health"]))
     print(enemy["name"] + ": HP=" + str(enemy["health"]) + "/" + str(enemy["max_health"]))

def display_battle_log(message):
    print(">>> " + message)

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

