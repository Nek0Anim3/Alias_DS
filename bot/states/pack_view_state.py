from bot.views.packs_mypacks_menu import PacksListView

active_pack_views: dict[int, "PacksListView"] = {}

def register_pack_view(uid: int ,view: "PacksListView"):
    active_pack_views[uid] = view
    print("pack STATE: active_pack_views", active_pack_views)

def unregister_pack_view(uid: int):
    if uid in active_pack_views:
        active_pack_views.pop(uid)
        print("pack STATE: Poped active_pack ", active_pack_views)

def get_pack_view(uid: int):
    return active_pack_views.get(uid, {})