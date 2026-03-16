from bot.views.join_menu import JoinMenuView

active_joins: dict[int, "JoinMenuView"] = {}

def register_join_view(uid: int ,view: "JoinMenuView"):
    active_joins[uid] = view
    print("JOIN STATE: active_joins", active_joins)

def unregister_join_view(uid: int):
    if uid in active_joins:
        active_joins.pop(uid)
        print("JOIN STATE: Poped active_join ", active_joins)

def get_join_view(uid: int):
    return active_joins.get(uid, {})