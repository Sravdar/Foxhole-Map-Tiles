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

The `with-json` branch carries two generated manifests so apps can update only the tiles that actually changed. They are regenerated automatically whenever `master` is updated.

 - `info.json` (~7 KB) — hash, size and file count per folder.
 - `info.files.json` (~4.4 MB) — the same tree plus every individual file's hash and size.

```
https://raw.githubusercontent.com/Kastow/Foxhole-Map-Tiles/with-json/info.json
https://raw.githubusercontent.com/Kastow/Foxhole-Map-Tiles/with-json/info.files.json
```

Using these useful for apps that caches map tiles between sessions or downloads them for offline usage.

Suggested client flow: fetch `info.json`, compare the root `hash` with the stored one, and only when it differs fetch `info.files.json` and download the files whose hash changed. Folder hashes let you skip whole layers or zoom levels before looking at individual files.

For detailed information check the script itself and github action file. [.scripts/create_info_json.py](.scripts/create_info_json.py), [.github/workflows/info-json.yml](.github/workflows/info-json.yml).

