# BlueMap-World-POI-Markers

Simple python script to convert a cubiomes csv export to BlueMap markers to generate POIs for structures like strongholds, mansions, monuments, villages or pyramids.

## Usage

1. Use [cubiomes-viewer](https://github.com/Cubitect/cubiomes-viewer/releases) to find all structures for your world seed, for reference see the screenshot and instructions below.
2. Export all POIs as csv and save the file as "cubiomes-export.csv" in the directory you saved the script in
3. Run the script using any halfway modern python version `python3 convert_markers.py` or `python convert_markers.py` on Windows.
4. Open the generated `markers.json` with a text editor and copy all of its content
5. Open the `config/maps/overworld.conf` file and scroll to the bottom
6. Replace the empty brackets (`{}`) with the copied text
7. Run `java -jar BlueMap-<version>.jar -r` to update your map and add the markers
8. Download the cubiomes-viewer github repository and copy the pngs from `rc/icons/` to your BlueMap `web/assets/` folder.

By default, the script generates markers for the following structures:
- stronghold
- mansion
- swamp_hut
- monument
- ancient_city
- desert_well
- jungle_pyramid
- igloo
- pillager_outpost
- desert_pyramid
- village
- trail_ruins

Adding or removing certain structures is as easy as removing or adding lines to the top of the python script.
Be warned though, adding too many markers will significantly decrease the webui's user experience.

## Cubiomes CSV Export

1. Enter your world seed
2. Click the Structures tab
3. Define your map size to generate structures for, e.g. the region you pre-gen'd chunks for
4. Hit the analyze button (which is surprisingly quick)
5. Export... to the directory you put the script in and name it "cubiomes-export.csv"

<img width="803" alt="image" src="https://github.com/TheMcSebi/BlueMap-World-POI-Markers/assets/1323131/1651b2b1-3f31-467a-bf08-af1570b22e1a">

## BlueMap Screenshot

<img width="960" alt="image" src="https://github.com/TheMcSebi/BlueMap-World-POI-Markers/assets/1323131/82679d4a-2135-4c52-ae48-a48282e1133d">
