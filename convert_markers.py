import os, json

input_file = "cubiomes-export.csv"

marker_icons = {
    "stronghold": "stronghold.png",
    "mansion": "mansion.png",
    "swamp_hut": "hut.png",
    "monument": "monument.png",
    "ancient_city": "ancient_city.png",
    "desert_well": "well.png",
    "jungle_pyramid": "jungle.png",
    "igloo": "igloo.png",
    "pillager_outpost": "outpost.png",
    "desert_pyramid": "desert.png",
    "village": "village.png",
    "trail_ruins": "trails.png",
    # "ruined_portal": "portal_lit.png",
    # "buried_treasure": "treasure.png",
    # "shipwreck": "shipwreck.png",
}

# the disabled ones are too many to be efficiently loaded in the webui, they even make it lag when they're not being actively displayed

data = []
if not os.path.isfile(input_file):
    print(f"Input file not found. Please export the list of structures from cubiomes-viewer and save the file as {input_file}")
    exit(1)

with open(input_file, "r", encoding="utf-8") as f:
    lines = f.readlines()
    for l in lines[6:]:
        line = l.strip().split(";")[1:]
        data.append(line)

types = {}
for d in data:
    if d[0] not in types:
        types[d[0]] = []
    types[d[0]].append({"x": d[1], "y": d[2]})

# the templates, copied from BlueMap docs
marker_set_template = {
    "label": "Example Marker Set",
    "toggleable": True,
    "default-hidden": True,
    "sorting": 0,
    "markers": None,
}

marker_template = {
    "type": "poi",
    "position": None,
    "label": None, # the name
    "detail": None, # apparently supports html
    "icon": None,
    "anchor": None,
    "sorting": 0,
    "listed": True,
    "classes": [
        "my-custom-class",
    ],
    "min-distance": 10,
    "max-distance": 10000000,
}

# generate markers dict from templates
marker_sets = {}
for j,t in enumerate(types.keys()):
    type_name = t.replace("_", " ").title()
    type_name_p = type_name + ("" if type_name.endswith("s") else "s")

    print(f"{t}: {len(types[t])}", end="")
    if t not in marker_icons:
        print("")
        continue

    marker_sets[t + "_set"] = marker_set_template.copy()
    current_marker_set = marker_sets[t + "_set"]

    current_marker_set["markers"] = {}
    current_marker_set["label"] = type_name_p
    current_marker_set["sorting"] = j

    if len(marker_icons[t]) == 0:
        print(f" !!unassigned icon for type {t}!!", end="")
        current_icon = "assets/poi.svg"
        current_anchor = { "x": 25, "y": 45 }
    else:
        current_icon = f"assets/{marker_icons[t]}"
        current_anchor = { "x": 10, "y": 10 }

    for i,pos in enumerate(types[t], start=1):
        marker_name = f"{t}_{i}"
        current_marker_set["markers"][marker_name] = marker_template.copy()
        current_marker = current_marker_set["markers"][marker_name]
        current_marker["position"] = {"x": pos["x"], "y": 64, "z": pos["y"]}
        current_marker["label"] = type_name + " No. " + str(i)
        current_marker["detail"] = "A " + type_name + "!"
        current_marker["sorting"] = i
        current_marker["icon"] = current_icon
        current_marker["anchor"] = current_anchor

    print(" (added markers)")

# dump to file
with open("markers.json", "w", encoding="utf-8") as f:
    json.dump(marker_sets, f)