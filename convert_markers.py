#!/usr/bin/env python

"""
This script converts cubiomes csv exports to POI markers for structures in BlueMap

Author: Sebi

Usage:
1. export all (or any of the structures you want) using cubiomes-viewer, save as cubiomes-export.csv
2. execute convert_markers.py
3. copy the markers-*.json contents to each bluemap world config file
4. copy the icons from cubiomes-viewer/rc/icons/ to the BlueMap web/assets/ folder
5. re-render your maps
"""

import os, json

input_file = "cubiomes-export.csv"

# sets of markers to process for each world, including their image names (to be put into BlueMap's web/assets/ folder)
# the disabled ones were too many to be efficiently loaded in the webui on a 32kx32k map, they even made the browser lag heavily when not being actively displayed
WORLD_MARKERS = {
    "overworld": {
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
        # "ocean_ruin": "ruins.png",
        # "amethyst_geode": "geode.png",
        # "amethyst_geode": "geode.png",
    },
    "nether": {
        "ruined_portal_nether": "portal.png",
        "fortress": "fortress.png",
        "bastion_remnant": "bastion.png",
    },
    "end": {
        "end_city": "endcity.png",
        "end_gateway": "gateway.png",
    },
}

# the templates, copied from BlueMap docs
MARKER_SET_TEMPLATE = {
    "label": None,
    "toggleable": True,
    "default-hidden": True,
    "sorting": 0,
    "markers": None, # instanciate list on clone
}

MARKER_TEMPLATE = {
    "type": "poi",
    "position": None, # instanciate dict with {x, y, z} on clone
    "label": None, # the name in the webui
    "detail": None, # apparently supports html
    "icon": None, # path to the icon, BlueMap's "web" folder is the root. Not sure if other directories than assets/ are served properly
    "anchor": None, #
    "sorting": 0,
    "listed": True,
    "classes": [
        "my-custom-class",
    ],
    "min-distance": 10,
    "max-distance": 10000000,
}

def read_cubiomes_csv(input_file: str) -> dict:
    """Read a list of seed POIs from a CSV file exported from cubiomes-viewer."""
    seed_pois = {}
    with open(input_file, "r", encoding="utf-8") as f:
        lines = f.readlines()
        for l in lines[6:]:
            line_data = l.strip().split(";")[1:]

            structure_name = line_data[0]

            if structure_name not in seed_pois:
                seed_pois[structure_name] = []
            seed_pois[structure_name].append({"x": line_data[1], "y": line_data[2]})
    return seed_pois

def generate_markers(icons: dict, seed_pois: dict) -> dict:
    """Generate a set of markers for each structure type that has an icon assigned."""
    marker_sets = {}
    for j,structure_type in enumerate(seed_pois.keys()):
        type_name = structure_type.replace("_", " ").title()
        type_name_p = type_name + ("" if type_name.endswith("s") else "s")
        marker_set_name = structure_type + "_set"

        if structure_type not in icons:
            continue

        marker_sets[marker_set_name] = MARKER_SET_TEMPLATE.copy()
        current_marker_set = marker_sets[marker_set_name]
        current_marker_set["markers"] = {}
        current_marker_set["label"] = type_name_p
        current_marker_set["sorting"] = j

        if len(icons[structure_type]) == 0:
            current_icon = "assets/poi.svg"
            current_anchor = { "x": 25, "y": 45 }
        else:
            current_icon = f"assets/{icons[structure_type]}"
            current_anchor = { "x": 10, "y": 10 }

        # add a marker for each poi
        for i,pos in enumerate(seed_pois[structure_type], start=1):
            marker_name = f"{structure_type}_{i}"
            current_marker_set["markers"][marker_name] = MARKER_TEMPLATE.copy()
            current_marker = current_marker_set["markers"][marker_name]
            current_marker["position"] = {"x": pos["x"], "y": 64, "z": pos["y"]}
            current_marker["label"] = type_name + " No. " + str(i)
            current_marker["detail"] = "A " + type_name + "!"
            current_marker["sorting"] = i
            current_marker["icon"] = current_icon
            current_marker["anchor"] = current_anchor

def main() -> None:
    # check if input file exists
    if not os.path.isfile(input_file):
        print(f"Input file not found. Please export the list of structures from cubiomes-viewer and save the file as {input_file}")
        exit(1)

    # read the seed POIs from the input file
    seed_pois = read_cubiomes_csv(input_file)
    # the script currently expects there to be only one seed present in the whole csv file, but could easily be extended to process multiple seeds. I just don't see any reason why one would require this specifically.

    # generate markers for each world
    for current_world in WORLD_MARKERS.keys():
        print(f"generating {current_world} markers...")
        marker_sets = generate_markers(WORLD_MARKERS[current_world], seed_pois)

        # dump to file
        with open(f"markers-{current_world}.json", "w", encoding="utf-8") as f:
            json.dump(marker_sets, f)

if __name__ == "__main__":
    main()