"""
Add sprite_list to all Act 1 rooms.
Each sprite defines: id, name, states, trigger_puzzle, z_layer.
"""
import os, json

rooms_dir = "Output/OurRooms"

sprite_definitions = {
    1: [
        {"id": "chandelier", "name": {"en": "Crystal Chandelier", "zh": "水晶吊灯"},
         "states": ["idle", "swinging", "key_fallen"], "trigger_puzzle": "The Last Guest", "z_layer": 2},
        {"id": "guest_book", "name": {"en": "Guest Book", "zh": "宾客登记簿"},
         "states": ["closed", "open"], "trigger_puzzle": "The Last Guest", "z_layer": 3},
        {"id": "reception_safe", "name": {"en": "Reception Safe", "zh": "前台保险箱"},
         "states": ["locked", "open"], "trigger_puzzle": "Reception Desk Safe", "z_layer": 3},
        {"id": "bellhop_figurines", "name": {"en": "Bellhop Figurines", "zh": "门童小雕像"},
         "states": ["idle", "highlighted"], "trigger_puzzle": "Bellhop's Button Board", "z_layer": 3},
        {"id": "elevator_doors", "name": {"en": "Elevator Doors", "zh": "电梯门"},
         "states": ["locked", "token_inserted", "open"], "trigger_puzzle": "final_action", "z_layer": 1},
        {"id": "brass_key", "name": {"en": "Brass Key", "zh": "黄铜钥匙"},
         "states": ["hidden", "on_floor", "collected"], "trigger_puzzle": "The Last Guest", "z_layer": 4},
        {"id": "reception_note", "name": {"en": "Receptionist's Note", "zh": "前台便条"},
         "states": ["hidden", "visible", "collected"], "trigger_puzzle": "Reception Desk Safe", "z_layer": 4},
        {"id": "elevator_token", "name": {"en": "Elevator Token", "zh": "电梯代币"},
         "states": ["hidden", "revealed", "collected"], "trigger_puzzle": "Bellhop's Button Board", "z_layer": 4}
    ],
    2: [
        {"id": "table_napkins", "name": {"en": "Colored Napkins", "zh": "彩色餐巾"},
         "states": ["idle", "highlighted"], "trigger_puzzle": "Table Number Tally", "z_layer": 3},
        {"id": "chalkboard_menu", "name": {"en": "Chalkboard Menu", "zh": "黑板菜单"},
         "states": ["idle", "zoomed"], "trigger_puzzle": "The Chef's Secret Menu", "z_layer": 2},
        {"id": "kitchen_window", "name": {"en": "Kitchen Pass-Through", "zh": "厨房传菜窗"},
         "states": ["locked", "open"], "trigger_puzzle": "The Chef's Secret Menu", "z_layer": 2},
        {"id": "wine_bottle", "name": {"en": "Wine Bottle (3rd row, 5th)", "zh": "酒瓶（第3排第5瓶）"},
         "states": ["in_rack", "sliding_out", "compartment_open"], "trigger_puzzle": "The Wine Rack Code", "z_layer": 3},
        {"id": "wine_cork", "name": {"en": "Wine Cork", "zh": "酒瓶软木塞"},
         "states": ["hidden", "visible", "collected"], "trigger_puzzle": "The Chef's Secret Menu", "z_layer": 4},
        {"id": "dining_key", "name": {"en": "Dining Room Key", "zh": "餐厅钥匙"},
         "states": ["hidden", "revealed", "collected"], "trigger_puzzle": "The Wine Rack Code", "z_layer": 4}
    ],
    3: [
        {"id": "bar_mirror", "name": {"en": "Bar Mirror", "zh": "吧台镜子"},
         "states": ["idle", "zoomed_reflection"], "trigger_puzzle": "Mirror Writing", "z_layer": 1},
        {"id": "napkin_code", "name": {"en": "Napkin with Code", "zh": "写有密码的餐巾纸"},
         "states": ["hidden_behind_bottles", "reflected_in_mirror"], "trigger_puzzle": "Mirror Writing", "z_layer": 3},
        {"id": "cash_register", "name": {"en": "Cash Register", "zh": "收银机"},
         "states": ["locked", "drawer_open"], "trigger_puzzle": "Mirror Writing", "z_layer": 3},
        {"id": "colored_bottles", "name": {"en": "Cocktail Bottles (Blue/Red/Gold)", "zh": "鸡尾酒瓶（蓝/红/金）"},
         "states": ["on_shelf", "pouring"], "trigger_puzzle": "Cocktail Mixing", "z_layer": 3},
        {"id": "crystal_glass", "name": {"en": "Crystal Glass", "zh": "水晶杯"},
         "states": ["empty", "mixed", "placed_on_coaster"], "trigger_puzzle": "Cocktail Mixing", "z_layer": 4},
        {"id": "bar_hidden_panel", "name": {"en": "Hidden Panel", "zh": "隐藏面板"},
         "states": ["closed", "open"], "trigger_puzzle": "Cocktail Mixing", "z_layer": 3},
        {"id": "jukebox", "name": {"en": "Jukebox", "zh": "点唱机"},
         "states": ["off", "coin_inserted", "playing", "back_panel_open"], "trigger_puzzle": "Jukebox Serenade", "z_layer": 2}
    ],
    4: [
        {"id": "old_photograph", "name": {"en": "Framed Photograph", "zh": "框架照片"},
         "states": ["idle", "zoomed"], "trigger_puzzle": "Then and Now", "z_layer": 2},
        {"id": "magnifying_glass", "name": {"en": "Magnifying Glass", "zh": "放大镜"},
         "states": ["on_counter", "in_use", "collected"], "trigger_puzzle": "Then and Now", "z_layer": 4},
        {"id": "postcard_rack", "name": {"en": "Postcard Rack", "zh": "明信片架"},
         "states": ["idle", "zoomed"], "trigger_puzzle": "Postcard Sequence", "z_layer": 3},
        {"id": "vintage_register", "name": {"en": "Vintage Cash Register", "zh": "复古收银机"},
         "states": ["locked", "drawer_open"], "trigger_puzzle": "Postcard Sequence", "z_layer": 3},
        {"id": "glass_cabinet", "name": {"en": "Glass Display Cabinet", "zh": "玻璃展柜"},
         "states": ["locked", "unlocked_open"], "trigger_puzzle": "The Glass Cabinet", "z_layer": 2},
        {"id": "exit_door", "name": {"en": "Exit Door (missing handle)", "zh": "出口门（缺少把手）"},
         "states": ["handleless", "handle_attached", "open"], "trigger_puzzle": "final_action", "z_layer": 1}
    ],
    5: [
        {"id": "mail_cubbies", "name": {"en": "Mail Cubbies", "zh": "信件格子"},
         "states": ["empty", "letters_placed_correctly"], "trigger_puzzle": "Room Number Sort", "z_layer": 2},
        {"id": "sorting_table_drawer", "name": {"en": "Sorting Table Hidden Drawer", "zh": "分拣桌隐藏抽屉"},
         "states": ["closed", "open"], "trigger_puzzle": "Room Number Sort", "z_layer": 3},
        {"id": "pneumatic_tube", "name": {"en": "Pneumatic Tube Station", "zh": "气动管站"},
         "states": ["idle", "code_entered", "capsule_arriving"], "trigger_puzzle": "Package Weight Cipher", "z_layer": 2},
        {"id": "iron_door", "name": {"en": "Iron Exit Door", "zh": "铁门出口"},
         "states": ["locked", "dial_turning", "open"], "trigger_puzzle": "Iron Door Dial", "z_layer": 1},
        {"id": "sealed_envelope", "name": {"en": "DO NOT DELIVER Envelope", "zh": "请勿投递信封"},
         "states": ["hidden", "revealed", "opened", "collected"], "trigger_puzzle": "Room Number Sort", "z_layer": 4}
    ],
    6: [
        {"id": "cleaning_bottles", "name": {"en": "Cleaning Supply Bottles", "zh": "清洁用品瓶"},
         "states": ["on_shelves", "highlighted_by_color"], "trigger_puzzle": "Supply Shelf Count", "z_layer": 3},
        {"id": "supply_cabinet", "name": {"en": "Supply Cabinet", "zh": "清洁柜"},
         "states": ["padlocked", "open"], "trigger_puzzle": "Supply Shelf Count", "z_layer": 2},
        {"id": "fuse_box", "name": {"en": "Fuse Box", "zh": "保险丝盒"},
         "states": ["open_empty", "fuses_inserted", "circuits_active"], "trigger_puzzle": "Fuse Box Circuit", "z_layer": 2},
        {"id": "overhead_light", "name": {"en": "Overhead Light", "zh": "头顶灯"},
         "states": ["off", "on"], "trigger_puzzle": "Fuse Box Circuit", "z_layer": 1},
        {"id": "notice_board", "name": {"en": "Notice Board", "zh": "公告板"},
         "states": ["in_darkness", "illuminated"], "trigger_puzzle": "Fuse Box Circuit", "z_layer": 2},
        {"id": "key_ring", "name": {"en": "Key Ring on Hook", "zh": "挂钩上的钥匙环"},
         "states": ["hanging", "key_7_removed"], "trigger_puzzle": "Key Ring Match", "z_layer": 3}
    ],
    7: [
        {"id": "pool_lights", "name": {"en": "Underwater Pool Lights", "zh": "水下泳池灯"},
         "states": ["off", "red", "blue", "green"], "trigger_puzzle": "Chromatic Numbers", "z_layer": 1},
        {"id": "pool_floor_numbers", "name": {"en": "Pool Floor Numbers", "zh": "泳池地板数字"},
         "states": ["hidden", "red_visible", "blue_visible", "green_visible"], "trigger_puzzle": "Chromatic Numbers", "z_layer": 2},
        {"id": "locker_3", "name": {"en": "Locker #3", "zh": "3号储物柜"},
         "states": ["locked", "open"], "trigger_puzzle": "Chromatic Numbers", "z_layer": 2},
        {"id": "tile_panel", "name": {"en": "3x3 Tile Panel", "zh": "3x3瓷砖面板"},
         "states": ["all_white", "pattern_in_progress", "pattern_matched"], "trigger_puzzle": "Tile Mosaic Match", "z_layer": 3},
        {"id": "sauna_door", "name": {"en": "Sauna Glass Door", "zh": "桑拿房玻璃门"},
         "states": ["fogged_handleless", "handle_attached", "open"], "trigger_puzzle": "Sauna Exit", "z_layer": 1}
    ],
    8: [
        {"id": "weight_bench", "name": {"en": "Weight Bench with Plates", "zh": "带杠铃片的卧推凳"},
         "states": ["idle", "zoomed"], "trigger_puzzle": "Weight Plate Tally", "z_layer": 2},
        {"id": "fire_door_display", "name": {"en": "Fire Door Magnetic Lock", "zh": "防火门磁力锁"},
         "states": ["locked_step1", "step1_done", "fully_unlocked"], "trigger_puzzle": "Weight Plate Tally", "z_layer": 2},
        {"id": "jammed_locker", "name": {"en": "Jammed Locker", "zh": "卡住的储物柜"},
         "states": ["jammed", "magnet_retrieving", "items_removed"], "trigger_puzzle": "Locker Magnet Retrieval", "z_layer": 2},
        {"id": "wall_timer", "name": {"en": "Wall Timer", "zh": "墙上计时器"},
         "states": ["missing_knob", "knob_attached", "set_to_98"], "trigger_puzzle": "Timer Dial Set", "z_layer": 3},
        {"id": "magnetic_sign", "name": {"en": "Magnetic Wall Sign", "zh": "磁性墙标识"},
         "states": ["on_wall", "removed", "in_use"], "trigger_puzzle": "Locker Magnet Retrieval", "z_layer": 4}
    ],
    9: [
        {"id": "arcade_cabinets", "name": {"en": "5 Arcade Cabinets", "zh": "5台街机"},
         "states": ["attract_mode", "flashing_sequence", "playing", "game_over_digit"], "trigger_puzzle": "Cabinet Light Show", "z_layer": 2},
        {"id": "token_dispenser", "name": {"en": "Token Dispenser", "zh": "代币分发器"},
         "states": ["locked", "dispensing", "empty"], "trigger_puzzle": "Cabinet Light Show", "z_layer": 3},
        {"id": "prize_counter_keypad", "name": {"en": "Prize Counter Keypad", "zh": "奖品柜台键盘"},
         "states": ["idle", "code_entered"], "trigger_puzzle": "High Score Harvest", "z_layer": 3},
        {"id": "prize_cabinet", "name": {"en": "Prize Cabinet", "zh": "奖品柜"},
         "states": ["locked", "open_bear_visible"], "trigger_puzzle": "High Score Harvest", "z_layer": 2},
        {"id": "carpet_symbols", "name": {"en": "Carpet Symbols", "zh": "地毯符号"},
         "states": ["idle", "highlighted"], "trigger_puzzle": "Carpet Code Slots", "z_layer": 1},
        {"id": "token_slot_panel", "name": {"en": "Token Slot Panel", "zh": "代币投入面板"},
         "states": ["empty", "tokens_inserted", "key_dropped"], "trigger_puzzle": "Carpet Code Slots", "z_layer": 3}
    ],
    10: [
        {"id": "piano", "name": {"en": "Baby Grand Piano", "zh": "小三角钢琴"},
         "states": ["idle", "bench_open"], "trigger_puzzle": "Sheet Music Cipher", "z_layer": 2},
        {"id": "spotlight_panel", "name": {"en": "Spotlight Control Panel", "zh": "聚光灯控制面板"},
         "states": ["idle", "code_entered", "spotlights_active"], "trigger_puzzle": "Sheet Music Cipher", "z_layer": 3},
        {"id": "stage_spotlights", "name": {"en": "Stage Spotlights (Red + Blue)", "zh": "舞台聚光灯（红+蓝）"},
         "states": ["off", "red_on", "blue_on", "both_on_overlap_visible"], "trigger_puzzle": "Spotlight Reveal", "z_layer": 1},
        {"id": "stage_floor_numbers", "name": {"en": "Stage Floor Hidden Numbers", "zh": "舞台地板隐藏数字"},
         "states": ["hidden", "red_4_visible", "blue_9_visible", "purple_1_visible"], "trigger_puzzle": "Spotlight Reveal", "z_layer": 2},
        {"id": "portrait_frame", "name": {"en": "Edmund's Portrait", "zh": "埃德蒙肖像画"},
         "states": ["closed", "lock_open", "swung_open_niche_visible"], "trigger_puzzle": "Spotlight Reveal", "z_layer": 2},
        {"id": "stage_trapdoor", "name": {"en": "Stage Trapdoor", "zh": "舞台暗门"},
         "states": ["padlocked", "unlocked", "open"], "trigger_puzzle": "Stage Trapdoor", "z_layer": 1}
    ]
}

for room_dir in sorted(os.listdir(rooms_dir)):
    if not room_dir.startswith("Room_"):
        continue
    path = os.path.join(rooms_dir, room_dir, "design.json")
    with open(path, "r", encoding="utf-8") as f:
        room = json.load(f)

    rnum = room["room_number"]
    sprites = sprite_definitions.get(rnum, [])
    room["sprite_list"] = sprites

    with open(path, "w", encoding="utf-8") as f:
        json.dump(room, f, ensure_ascii=False, indent=2)

    total_states = sum(len(s["states"]) for s in sprites)
    print(f"Room {rnum:>2}: {len(sprites)} sprites, {total_states} total states")

print(f"\nDone! Total sprites: {sum(len(v) for v in sprite_definitions.values())}")
print(f"Total states: {sum(sum(len(s['states']) for s in v) for v in sprite_definitions.values())}")
