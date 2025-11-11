#!/usr/bin/env python3
"""
Generate a repository manifest of JSON files with Git blob SHA-1 and sizes.

This produces a file with the following structure:
{
  "generated": "2025-11-11T...Z",
  "files": {
      "cards/foo.json": {"sha": "...", "size": 1234},
      ...
  }
}

Usage:
  python scripts/update_manifest.py --source cards --output cards_manifest.json

By default this includes only files with a .json extension. Paths in the
manifest are relative to the repo root and prefixed with the source root name
(e.g. "cards/..."). This matches the layout expected by the client's
`GitHubSync` implementation.
"""

import argparse
import hashlib
import json
import os
import sys
from datetime import datetime, timezone


def git_blob_sha1(data: bytes) -> str:
    # Git blob hash: sha1("blob <len>\0" + data)
    header = b"blob " + str(len(data)).encode("ascii") + b"\0"
    h = hashlib.sha1()
    h.update(header)
    h.update(data)
    return h.hexdigest()


def gather_files(source_dir: str, include_exts=None):
    if include_exts is None:
        include_exts = {'.json'}
    files = []
    for root, dirs, filenames in os.walk(source_dir):
        # sort for deterministic output
        dirs.sort()
        filenames.sort()
        for fn in filenames:
            if include_exts and not any(fn.lower().endswith(e) for e in include_exts):
                continue
            full = os.path.join(root, fn)
            rel = os.path.relpath(full, source_dir)
            files.append((full, rel.replace('\\', '/')))
    return files


def build_manifest(source_dir: str, source_key: str):
    manifest_files = {}
    files = gather_files(source_dir)
    for full, rel in files:
        try:
            with open(full, 'rb') as f:
                data = f.read()
        except Exception as e:
            print(f"Warning: failed to read {full}: {e}", file=sys.stderr)
            continue
        sha = git_blob_sha1(data)
        size = len(data)
        # manifest keys should be relative to repo root, typically like 'cards/<rel>'
        key = f"{source_key}/{rel}" if source_key else rel
        manifest_files[key] = { 'sha': sha, 'size': size }
    return manifest_files


def write_output(out_path: str, files_map: dict):
    obj = {
        'generated': datetime.now(timezone.utc).isoformat(),
        'files': {}
    }
    # sort keys for stable output
    for k in sorted(files_map.keys()):
        obj['files'][k] = { 'sha': files_map[k]['sha'], 'size': files_map[k]['size'] }
    os.makedirs(os.path.dirname(out_path) or '.', exist_ok=True)
    tmp = out_path + '.tmp'
    with open(tmp, 'w', encoding='utf-8') as f:
        json.dump(obj, f, indent=2, ensure_ascii=False)
        f.write('\n')
    os.replace(tmp, out_path)
    print(f"Wrote manifest to {out_path} ({len(files_map)} files)")


def main(argv=None):
    p = argparse.ArgumentParser(description='Generate cards_manifest.json for GitHubSync')
    p.add_argument('--source', '-s', action='append', default=[], help='Source directories. Can be specified multiple times. Each value may be "key=path" or just "path". (e.g. -s cards=run/kdm_db/cards)')
    p.add_argument('--output', '-o', default='kdm_manifest.json', help='Output manifest path (default: kdm_manifest.json)')
    p.add_argument('--include-ext', '-e', action='append', default=['.json'], help='File extensions to include (can be repeated). Default: .json')
    args = p.parse_args(argv)

    if not args.source:
        print("Error: at least one --source (-s) is required", file=sys.stderr)
        return 2

    exts = set(e if e.startswith('.') else ('.' + e) for e in args.include_ext)

    combined = {}
    # Each source entry can be "key=path" or just "path" (key defaults to basename)
    for s in args.source:
        if '=' in s:
            key, path = s.split('=', 1)
            key = key.strip()
            path = path.strip()
        else:
            path = s
            key = os.path.basename(os.path.normpath(path))

        if not os.path.isdir(path):
            print(f"Warning: source directory does not exist, skipping: {path}", file=sys.stderr)
            continue

        files_map = build_manifest(path, key)
        # merge
        for k, v in files_map.items():
            if k in combined:
                print(f"Warning: duplicate key in manifest for {k}, overwriting with latest source", file=sys.stderr)
            combined[k] = v

    if not combined:
        print("Error: no files found in any sources", file=sys.stderr)
        return 2

    write_output(args.output, combined)
    return 0


if __name__ == '__main__':
    sys.exit(main())
