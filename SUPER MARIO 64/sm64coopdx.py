#!/usr/bin/env python3
"""
sm64coopdx.py
Convert SM64-Reloaded textures into a sm64coopdx DynOS texture pack.

Pipeline
--------
1. SM64-Reloaded's sm64ex.sh builds a gfx/ folder from the source PNGs
   (run it manually first - see README below).
2. This script reads dynos_mgr_builtin_tex.cpp from the sm64coopdx source
   (fetched from GitHub automatically, or supplied locally) to learn which
   C variable name corresponds to each texture file path.
3. Each PNG is decoded to raw RGBA32, optionally resized, and written as a
   DynOS DATA_TYPE_TEXTURE_RAW (.tex) binary that sm64coopdx can load.

Usage
-----
  python3 sm64coopdx.py \\
      --gfx     "path/to/SM64-Reloaded/SUPER MARIO 64/_build/SM64 Reloaded (sm64ex)/gfx" \\
      --out     "path/to/sm64coopdx/dynos/packs/SM64 Reloaded" \\
      [--builtin path/to/sm64coopdx-src/data/dynos_mgr_builtin_tex.cpp] \\
      [--max-dim 256]

If --builtin is omitted the file is downloaded from the sm64coopdx GitHub repo.

Requirements
------------
  pip install Pillow requests   (requests only needed for auto-download)

How to prepare the source textures
-----------------------------------
  git clone https://github.com/GhostlyDark/SM64-Reloaded.git
  cd "SM64-Reloaded/SUPER MARIO 64"
  chmod +x sm64ex.sh
  echo "" | ./sm64ex.sh          # press enter to choose PNG format

That produces:
  _build/SM64 Reloaded (sm64ex)/gfx/   <-- use this as --gfx

DynOS .tex format (DATA_TYPE_TEXTURE_RAW = 21)
-----------------------------------------------
  u8   type        = 21
  u8   name_len
  char name[name_len]
  s32  rawFormat   = 0  (G_IM_FMT_RGBA)
  s32  rawSize     = 3  (G_IM_SIZ_32b)
  s32  rawWidth
  s32  rawHeight
  s32  rawDataLen  = rawWidth * rawHeight * 4
  u8   rawData[rawDataLen]   (RGBA32, row-major)

Why DATA_TYPE_TEXTURE_RAW and not DATA_TYPE_TEXTURE (PNG)?
  DynOS_Tex_LoadFromBinary reads DATA_TYPE_TEXTURE into mPngData only –
  it never calls stb_image to decode it into mRawData.  DynOS_Tex_Upload
  then uploads mRawData (empty) → black texture.  DATA_TYPE_TEXTURE_RAW
  stores the decoded pixels directly, so upload works first time.

Why use C variable names, not file paths?
  DynOS_Builtin_Tex_GetFromName() (dynos_mgr_builtin_tex.cpp) matches
  texture nodes by their C variable name (e.g. cave_09000000), not by the
  file path string.  The mapping is extracted from the macro table in that
  source file.
"""

import argparse
import os
import re
import struct
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# DynOS constants
# ---------------------------------------------------------------------------
DATA_TYPE_TEXTURE_RAW = 21
G_IM_FMT_RGBA         = 0
G_IM_SIZ_32b          = 3

BUILTIN_URL = (
    "https://raw.githubusercontent.com/coop-deluxe/sm64coopdx/"
    "main/data/dynos_mgr_builtin_tex.cpp"
)

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def fetch_builtin_source(url: str) -> str:
    try:
        import requests
    except ImportError:
        sys.exit(
            "ERROR: 'requests' not installed and --builtin not supplied.\n"
            "  pip install requests\n"
            "or pass --builtin path/to/dynos_mgr_builtin_tex.cpp"
        )
    print(f"Downloading builtin texture table from GitHub …")
    r = requests.get(url, timeout=30)
    r.raise_for_status()
    return r.text


def build_path_to_name(source: str) -> dict:
    """
    Parse dynos_mgr_builtin_tex.cpp and return {file_path: c_var_name}.

    Two macro forms exist:
      define_builtin_tex (var, "path", ...)  ->  name = var
      define_builtin_tex_(var, "path", ...)  ->  name = var + "_"
    """
    mapping = {}
    for var, path in re.findall(r'define_builtin_tex\((\w+),\s*"([^"]+)"', source):
        mapping[path] = var
    for var, path in re.findall(r'define_builtin_tex_\((\w+),\s*"([^"]+)"', source):
        mapping[path] = var + "_"
    return mapping


def make_tex_raw(name: str, img) -> bytes:
    """
    Encode one texture as DATA_TYPE_TEXTURE_RAW binary.
    img must be a Pillow Image (any mode; converted to RGBA internally).
    """
    name_enc = name.encode("ascii")
    if len(name_enc) > 255:
        raise ValueError(f"Texture name too long (>255 chars): {name!r}")
    rgba = img.convert("RGBA")
    raw  = rgba.tobytes()
    w, h = rgba.size
    return (
        struct.pack("B",  DATA_TYPE_TEXTURE_RAW) +
        struct.pack("B",  len(name_enc))          +
        name_enc                                   +
        struct.pack("<i", G_IM_FMT_RGBA)           +
        struct.pack("<i", G_IM_SIZ_32b)            +
        struct.pack("<i", w)                       +
        struct.pack("<i", h)                       +
        struct.pack("<i", len(raw))                +
        raw
    )


# ---------------------------------------------------------------------------
# Main conversion
# ---------------------------------------------------------------------------

def convert(gfx_dir: str, out_dir: str, mapping: dict, max_dim: int | None):
    try:
        from PIL import Image
    except ImportError:
        sys.exit("ERROR: Pillow not installed.  pip install Pillow")

    os.makedirs(out_dir, exist_ok=True)

    # Remove stale .tex files from a previous run
    removed = sum(
        1 for f in os.listdir(out_dir)
        if f.endswith(".tex") and os.remove(os.path.join(out_dir, f)) is None
    )
    if removed:
        print(f"Removed {removed} stale .tex files from previous run.")

    created = skipped = errors = 0

    for root, _, files in os.walk(gfx_dir):
        for fname in files:
            if not fname.lower().endswith(".png"):
                continue

            abs_path = os.path.join(root, fname)
            rel      = os.path.relpath(abs_path, gfx_dir).replace(os.sep, "/")

            c_name = mapping.get(rel)
            if not c_name:
                skipped += 1
                continue

            try:
                img = Image.open(abs_path)
                if max_dim and (img.width > max_dim or img.height > max_dim):
                    img.thumbnail((max_dim, max_dim), Image.LANCZOS)

                tex_data = make_tex_raw(c_name, img)
            except Exception as e:
                print(f"  WARNING: skipping {rel}: {e}", file=sys.stderr)
                errors += 1
                continue

            # Filename on disk can be anything (the C name lives inside the binary)
            safe_name = rel.replace("/", "__") + ".tex"
            with open(os.path.join(out_dir, safe_name), "wb") as f:
                f.write(tex_data)
            created += 1

    return created, skipped, errors


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Convert SM64-Reloaded sm64ex textures → sm64coopdx DynOS pack",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__.split("Usage")[0],
    )
    parser.add_argument(
        "--gfx", required=True,
        help='Path to the gfx/ folder built by sm64ex.sh, e.g. '
             '"SM64-Reloaded/SUPER MARIO 64/_build/SM64 Reloaded (sm64ex)/gfx"',
    )
    parser.add_argument(
        "--out", required=True,
        help='Output directory for the DynOS pack, e.g. '
             '"sm64coopdx/dynos/packs/SM64 Reloaded"',
    )
    parser.add_argument(
        "--builtin", default=None,
        help="Path to dynos_mgr_builtin_tex.cpp from the sm64coopdx source tree. "
             "If omitted, the file is fetched automatically from GitHub.",
    )
    parser.add_argument(
        "--max-dim", type=int, default=256,
        help="Rescale any texture whose longest side exceeds this value "
             "(default: 256). Use 0 to disable rescaling (full 4K — needs ~3.5 GB RAM).",
    )

    args = parser.parse_args()

    max_dim = args.max_dim if args.max_dim > 0 else None

    # 1. Load builtin texture table
    if args.builtin:
        print(f"Reading builtin texture table from {args.builtin} …")
        with open(args.builtin, encoding="utf-8") as f:
            source = f.read()
    else:
        source = fetch_builtin_source(BUILTIN_URL)

    mapping = build_path_to_name(source)
    print(f"  {len(mapping)} builtin texture entries loaded.")

    # 2. Validate input directory
    gfx_dir = args.gfx
    if not os.path.isdir(gfx_dir):
        sys.exit(
            f"ERROR: gfx directory not found: {gfx_dir!r}\n"
            "Run sm64ex.sh inside 'SUPER MARIO 64/' first."
        )

    # 3. Convert
    size_label = f"≤{max_dim}px" if max_dim else "full resolution"
    print(f"Converting textures ({size_label}) …")
    created, skipped, errors = convert(gfx_dir, args.out, mapping, max_dim)

    # 4. Summary
    pack_mb = sum(
        os.path.getsize(os.path.join(args.out, f))
        for f in os.listdir(args.out) if f.endswith(".tex")
    ) / 1024 / 1024

    print()
    print(f"Done.")
    print(f"  Created : {created} .tex files")
    print(f"  Skipped : {skipped} (no matching builtin — expected for font/special textures)")
    print(f"  Errors  : {errors}")
    print(f"  Pack size on disk: {pack_mb:.0f} MB")
    print()
    print(f"Pack written to: {args.out}")
    print()
    print("Next steps:")
    print("  1. Launch sm64coopdx")
    print('  2. Open the DynOS menu → Packs → enable "SM64 Reloaded"')
    print("  3. Enter / reload a level to see the textures")


if __name__ == "__main__":
    main()
