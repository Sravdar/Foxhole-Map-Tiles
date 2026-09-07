#!/usr/bin/env python3
"""Compare two manifests ignoring generated_at. Exit 0 if equal, 1 if different.

generated_at changes on every run, so a byte comparison would make the workflow
commit forever. A missing or unreadable OLD counts as different.
"""
import json
import sys


def load(path):
    try:
        with open(path, encoding="utf-8") as f:
            doc = json.load(f)
    except (OSError, ValueError):
        return None
    doc.pop("generated_at", None)
    return doc


def main():
    if len(sys.argv) != 3:
        sys.exit("usage: compare_info_json.py OLD NEW")
    old, new = load(sys.argv[1]), load(sys.argv[2])
    if new is None:
        sys.exit(f"cannot read {sys.argv[2]}")
    same = old == new
    print("same" if same else "different")
    sys.exit(0 if same else 1)


if __name__ == "__main__":
    main()
