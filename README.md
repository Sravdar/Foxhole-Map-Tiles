# Foxhole-Map-Tiles
Map tiles for Foxhole interactive maps, version 1.51 from January 2023.

Link format: 
https://raw.githubusercontent.com/Kastow/Foxhole-Map-Tiles/master/Tiles/{z}/{z}_{x}_{y}.png

Demo: https://foxhole-tilemap-prototype.glitch.me/

Demo source: https://glitch.com/edit/#!/foxhole-tilemap-prototype

 - Map created by Clapfoot Inc. https://github.com/clapfoot/
 - Cut into hexes by Kastow
 - Cut into tiles by https://github.com/NoUDerp/ using https://github.com/NoUDerp/Tiler
 - Tiles created by Sentsu https://sentsu.itch.io/foxhole-better-map-mod

Now also contains icons that are used in Foxhole maps, created by Clapfoot Inc. and colored by https://github.com/BladeRikWr

Map and icon images are a property of Clapfoot Inc. and are used with their permission.

## Update manifest

The `with_json` branch carries generated manifests so apps can update only the tiles that
actually changed. They are regenerated automatically whenever `master` is updated.

 - `info.json` (~7 KB) — hash, size and file count per folder. Each top-level folder also
   names its `detail_file`.
 - One detail manifest per top-level folder (~600 KB each) — that folder's tree plus every
   individual file's hash and size:
   `info.tiles.json`, `info.sat.tiles.json`, `info.tree.tiles.json`,
   `info.fly.height.tiles.json`, `info.map.icons.json`.

```
https://raw.githubusercontent.com/Kastow/Foxhole-Map-Tiles/with_json/info.json
https://raw.githubusercontent.com/Kastow/Foxhole-Map-Tiles/with_json/info.sat.tiles.json
```

Suggested client flow: fetch `info.json`, compare the root `hash` with the stored one, and only
when it differs compare each top-level folder's `hash`. For every folder that changed, fetch its
`detail_file` and download the files whose hash changed. Subfolder hashes let you skip whole
zoom levels before looking at individual files.

For detailed information check [.scripts/create_info_json.py](.scripts/create_info_json.py).
