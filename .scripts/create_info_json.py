#!/usr/bin/env python3
"""Generate the info.json / info.files.json manifests for the tile folders.

Root files and anything starting with "." are skipped. Every folder gets a hash
built from its children's hashes, so a hash change points straight at what moved.
"""
import argparse
import hashlib
import json
import os
from datetime import datetime, timezone

MANIFEST_VERSION = 1
CHUNK = 1 << 20


def file_node(path):
    h = hashlib.sha256()
    size = 0
    with open(path, "rb") as f:
        while chunk := f.read(CHUNK):
            h.update(chunk)
            size += len(chunk)
    return {"hash": h.hexdigest(), "size": size}


def folder_node(path, skip_files=False):
    """Walk one folder. Children are sorted by name so output is deterministic."""
    folders, files = {}, {}
    for entry in sorted(os.scandir(path), key=lambda e: e.name):
        if entry.name.startswith("."):
            continue
        if entry.is_dir():
            folders[entry.name] = folder_node(entry.path)
        elif entry.is_file() and not skip_files:
            files[entry.name] = file_node(entry.path)

    children = [("d", n, v) for n, v in folders.items()]
    children += [("f", n, v) for n, v in files.items()]
    h = hashlib.sha256()
    for kind, name, node in sorted(children, key=lambda c: c[1]):
        h.update(f"{kind} {node['hash']} {name}\n".encode("utf-8"))

    return {
        "hash": h.hexdigest(),
        "size": sum(n["size"] for n in (*folders.values(), *files.values())),
        "item_count": sum(n["item_count"] for n in folders.values()) + len(files),
        "folders": folders,
        "files": files,
    }


def without_files(folders):
    return {
        name: {
            "hash": n["hash"],
            "size": n["size"],
            "item_count": n["item_count"],
            "folders": without_files(n["folders"]),
        }
        for name, n in folders.items()
    }


def document(root, generated_at, detailed, detail_name):
    doc = {
        "manifest_version": MANIFEST_VERSION,
        "generated_at": generated_at,
        "hash_algorithm": "sha256",
        "detailed": detailed,
    }
    if not detailed:
        doc["detail_file"] = detail_name
    doc["hash"] = root["hash"]
    doc["size"] = root["size"]
    doc["item_count"] = root["item_count"]
    doc["folders"] = root["folders"] if detailed else without_files(root["folders"])
    return doc


def write_json(path, doc, indent):
    separators = (",", ": ") if indent else (",", ":")
    text = json.dumps(doc, indent=indent, separators=separators, ensure_ascii=False)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text + "\n")


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--root", default=".", help="repository root to scan")
    p.add_argument("--out-dir", default=".", help="where to write the manifests")
    p.add_argument("--info-name", default="info.json", help="folder-level manifest name")
    p.add_argument("--detail-name", default="info.files.json", help="per-file manifest name")
    args = p.parse_args()

    root = folder_node(args.root, skip_files=True)
    generated_at = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    os.makedirs(args.out_dir, exist_ok=True)

    write_json(
        os.path.join(args.out_dir, args.info_name),
        document(root, generated_at, False, args.detail_name),
        indent=2,
    )
    write_json(
        os.path.join(args.out_dir, args.detail_name),
        document(root, generated_at, True, args.detail_name),
        indent=None,
    )
    print(f"{root['item_count']} files, {root['size']} bytes, hash {root['hash']}")


if __name__ == "__main__":
    main()
