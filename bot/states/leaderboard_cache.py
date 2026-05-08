from debug.DebugLogger import DebugLogger

leaderboard_cache = []

def get_leaderboard_cache():
    global leaderboard_cache
    DebugLogger.Console(f"Fetched leaderboard cache")
    return leaderboard_cache

def update_leaderboard_cache(leaderboard_data):
    global leaderboard_cache
    leaderboard_cache[0] = leaderboard_data
    DebugLogger.Console(f"Updated leaderboard cache")
