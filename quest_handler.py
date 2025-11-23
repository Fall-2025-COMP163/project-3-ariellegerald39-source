"""
COMP 163 - Project 3: Quest Chronicles
Quest Handler Module - Starter Code

Name: Arielle Gerald

AI Usage: [Document any AI assistance used]

This module handles quest management, dependencies, and completion.
"""

from custom_exceptions import (
    QuestNotFoundError,
    QuestRequirementsNotMetError,
    QuestAlreadyCompletedError,
    QuestNotActiveError,
    InsufficientLevelError
)

# ============================================================================
# QUEST MANAGEMENT
# ============================================================================

def accept_quest(character, quest_id, quest_data_dict):
    """Accept a new quest with all validations."""

    # Check if the quest exists in the data
    if quest_id not in quest_data_dict:
        raise QuestNotFoundError(f"Quest {quest_id} not found")

    quest = quest_data_dict[quest_id]

    # Check if character meets the level requirement
    if character.get('level', 1) < quest.get('required_level', 1):
        raise InsufficientLevelError(f"Level too low for quest {quest_id}")

    # Check if there is a prerequisite quest
    prereq = quest.get('prerequisite', 'NONE')
    if prereq != 'NONE' and prereq not in character.get('completed_quests', []):
        raise QuestRequirementsNotMetError(f"Prerequisite {prereq} not completed")

    # Check if the quest is already completed
    if quest_id in character.get('completed_quests', []):
        raise QuestAlreadyCompletedError(f"Quest {quest_id} already completed")

    # Check if the quest is already active
    if quest_id in character.get('active_quests', []):
        raise QuestAlreadyCompletedError(f"Quest {quest_id} is already active")

    # Add the quest to the character's active quests
    character.setdefault('active_quests', []).append(quest_id)
    return True


def complete_quest(character, quest_id, quest_data_dict):
    """Complete an active quest and grant rewards."""

    # Check if the quest exists
    if quest_id not in quest_data_dict:
        raise QuestNotFoundError(f"Quest {quest_id} not found")

    # Check if the quest is currently active
    if quest_id not in character.get('active_quests', []):
        raise QuestNotActiveError(f"Quest {quest_id} is not active")

    quest = quest_data_dict[quest_id]

    # Move quest from active to completed
    character['active_quests'].remove(quest_id)
    character.setdefault('completed_quests', []).append(quest_id)

    # Grant rewards to the character
    xp = quest.get('reward_xp', 0)
    gold = quest.get('reward_gold', 0)
    character['experience'] = character.get('experience', 0) + xp
    character['gold'] = character.get('gold', 0) + gold

    # Return rewards for reference
    return {'xp': xp, 'gold': gold}


def abandon_quest(character, quest_id):
    """Remove a quest from active quests without completing it."""

    # Make sure the quest is active
    if quest_id not in character.get('active_quests', []):
        raise QuestNotActiveError(f"Quest {quest_id} is not active")

    # Remove it from active quests
    character['active_quests'].remove(quest_id)
    return True


def get_active_quests(character, quest_data_dict):
    """Return full quest data for all active quests."""
    # Only return quests that exist in quest data
    return [quest_data_dict[qid] for qid in character.get('active_quests', []) if qid in quest_data_dict]


def get_completed_quests(character, quest_data_dict):
    """Return full quest data for all completed quests."""
    return [quest_data_dict[qid] for qid in character.get('completed_quests', []) if qid in quest_data_dict]


def get_available_quests(character, quest_data_dict):
    """Return quests that can currently be accepted."""
    available = []
    for qid, quest in quest_data_dict.items():
        # Only include quests that meet requirements
        if can_accept_quest(character, qid, quest_data_dict):
            available.append(quest)
    return available


# ============================================================================ 
# QUEST TRACKING
# ============================================================================

def is_quest_completed(character, quest_id):
    # Check if a quest is in the completed list
    return quest_id in character.get('completed_quests', [])


def is_quest_active(character, quest_id):
    # Check if a quest is in the active list
    return quest_id in character.get('active_quests', [])


def can_accept_quest(character, quest_id, quest_data_dict):
    """Check if quest requirements are met (returns boolean)."""

    # Quest must exist
    if quest_id not in quest_data_dict:
        return False

    quest = quest_data_dict[quest_id]

    # Must meet level requirement
    if character.get('level', 1) < quest.get('required_level', 1):
        return False

    # Must meet prerequisite quest requirement
    prereq = quest.get('prerequisite', 'NONE')
    if prereq != 'NONE' and prereq not in character.get('completed_quests', []):
        return False

    # Quest cannot already be completed
    if quest_id in character.get('completed_quests', []):
        return False

    # Quest cannot already be active
    if quest_id in character.get('active_quests', []):
        return False

    return True


def get_quest_prerequisite_chain(quest_id, quest_data_dict):
    """Return full prerequisite chain in order."""

    # Check if the quest exists
    if quest_id not in quest_data_dict:
        raise QuestNotFoundError(f"Quest {quest_id} not found")

    chain = []
    current = quest_id

    # Walk backwards through prerequisites
    while current != 'NONE':
        chain.insert(0, current)  # Insert at beginning to maintain order
        current = quest_data_dict.get(current, {}).get('prerequisite', 'NONE')
        if current != 'NONE' and current not in quest_data_dict:
            raise QuestNotFoundError(f"Prerequisite {current} does not exist")
    return chain


# ============================================================================ 
# QUEST STATISTICS
# ============================================================================

def get_quest_completion_percentage(character, quest_data_dict):
    """Calculate the percentage of quests completed."""
    total = len(quest_data_dict)
    if total == 0:
        return 0.0
    completed = len(character.get('completed_quests', []))
    return (completed / total) * 100.0


def get_total_quest_rewards_earned(character, quest_data_dict):
    """Calculate total XP and Gold earned from completed quests."""
    total_xp = 0
    total_gold = 0
    for qid in character.get('completed_quests', []):
        quest = quest_data_dict.get(qid, {})
        total_xp += quest.get('reward_xp', 0)
        total_gold += quest.get('reward_gold', 0)
    return {'total_xp': total_xp, 'total_gold': total_gold}


def get_quests_by_level(quest_data_dict, min_level, max_level):
    """Return quests within a certain level range."""
    return [q for q in quest_data_dict.values() if min_level <= q.get('required_level', 1) <= max_level]


# ============================================================================ 
# DISPLAY FUNCTIONS
# ============================================================================

def display_quest_info(quest_data):
    # Show quest details
    print(f"\n=== {quest_data.get('title', 'Unknown Quest')} ===")
    print(f"Description: {quest_data.get('description', '')}")
    print(f"Required Level: {quest_data.get('required_level', 1)}")
    print(f"Prerequisite: {quest_data.get('prerequisite', 'NONE')}")
    print(f"Rewards: XP={quest_data.get('reward_xp', 0)}, Gold={quest_data.get('reward_gold', 0)}\n")


def display_quest_list(quest_list):
    # Show a list of quests with basic info
    for quest in quest_list:
        print(f"{quest.get('title', 'Unknown')} - Level {quest.get('required_level', 1)}, "
              f"XP: {quest.get('reward_xp', 0)}, Gold: {quest.get('reward_gold', 0)}")


def display_character_quest_progress(character, quest_data_dict):
    # Show the character's quest progress
    active_count = len(character.get('active_quests', []))
    completed_count = len(character.get('completed_quests', []))
    percent = get_quest_completion_percentage(character, quest_data_dict)
    rewards = get_total_quest_rewards_earned(character, quest_data_dict)

    print(f"Active Quests: {active_count}")
    print(f"Completed Quests: {completed_count}")
    print(f"Completion: {percent:.2f}%")
    print(f"Total XP Earned: {rewards['total_xp']}")
    print(f"Total Gold Earned: {rewards['total_gold']}")


# ============================================================================ 
# VALIDATION
# ============================================================================

def validate_quest_prerequisites(quest_data_dict):
    """Check all prerequisites exist in quest data."""
    for qid, quest in quest_data_dict.items():
        prereq = quest.get('prerequisite', 'NONE')
        if prereq != 'NONE' and prereq not in quest_data_dict:
            raise QuestNotFoundError(f"Quest {qid} has invalid prerequisite {prereq}")
    return True



# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":
    print("=== QUEST HANDLER TEST ===")
    
    # Test data
    # test_char = {
    #     'level': 1,
    #     'active_quests': [],
    #     'completed_quests': [],
    #     'experience': 0,
    #     'gold': 100
    # }
    #
    # test_quests = {
    #     'first_quest': {
    #         'quest_id': 'first_quest',
    #         'title': 'First Steps',
    #         'description': 'Complete your first quest',
    #         'reward_xp': 50,
    #         'reward_gold': 25,
    #         'required_level': 1,
    #         'prerequisite': 'NONE'
    #     }
    # }
    #
    # try:
    #     accept_quest(test_char, 'first_quest', test_quests)
    #     print("Quest accepted!")
    # except QuestRequirementsNotMetError as e:
    #     print(f"Cannot accept: {e}")

