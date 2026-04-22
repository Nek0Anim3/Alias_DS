from discord import Interaction

from debug.DebugLogger import DebugLogger

active_interactions = {}

def save_interaction(uid: int, interaction: Interaction):
    active_interactions[uid] = interaction
    DebugLogger.Console("INTERACTIONS: Saved Interaction", interaction)

def get_interaction(uid: int):
    DebugLogger.Console("INTERACTIONS: Retrieved Interaction", active_interactions[uid])
    return active_interactions.get(uid)