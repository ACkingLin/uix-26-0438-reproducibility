#!/usr/bin/env python3
"""Download the public UIX release and restore the exact original ZIP files.

Python 3.9+ standard library only. Interrupted downloads can be resumed by
rerunning the same command. Existing correct parts and archives are reused.
"""
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
import hashlib
import json
from pathlib import Path
import shutil
import time
import urllib.error
import urllib.request

BASE_URL = "https://github.com/ACkingLin/uix-26-0438-reproducibility/releases/download/v1.0.0"
ARCHIVES = {
    "Supplementary_Software_UIX.zip": (23569934, "f42d130fca704961ac5d75e1e8f7890b14fd4b995ecbe536f24658f259363556"),
    "Locked_Checkpoints_UIX.zip": (939111539, "27b2da89918185b1a1b760d75c6b7a7bf24fac7c8faef00d5b7fa024b6c5223b"),
}


def sha256(path):
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for block in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def matches(path, size, checksum):
    return path.is_file() and path.stat().st_size == size and sha256(path) == checksum


def fetch(url):
    request = urllib.request.Request(url, headers={"User-Agent": "UIX-public-reproducibility/1.0"})
    return urllib.request.urlopen(request, timeout=90)


def get_part(part, folder):
    name = part["name"]
    if Path(name).name != name or not name.startswith(tuple(n + ".part8-" for n in ARCHIVES)):
        raise ValueError("Unexpected release part name")
    target = folder / name
    if matches(target, part["bytes"], part["sha256"]):
        return name
    temporary = target.with_name(target.name + ".download")
    for attempt in range(3):
        try:
            with fetch(BASE_URL + "/" + name) as response, temporary.open("wb") as output:
                shutil.copyfileobj(response, output, length=1024 * 1024)
            if not matches(temporary, part["bytes"], part["sha256"]):
                raise ValueError("Downloaded part failed SHA-256 verification: " + name)
            temporary.replace(target)
            return name
        except (OSError, urllib.error.URLError, ValueError):
            if attempt == 2:
                raise
            time.sleep(attempt + 1)


def assemble(archive, part_folder, output_folder):
    target = output_folder / archive["name"]
    if matches(target, archive["bytes"], archive["sha256"]):
        return target
    if target.exists():
        raise FileExistsError("An existing archive has a different checksum: " + str(target))
    temporary = target.with_name(target.name + ".assembling")
    with temporary.open("wb") as output:
        for part in archive["parts"]:
            source = part_folder / part["name"]
            if not matches(source, part["bytes"], part["sha256"]):
                raise ValueError("Missing or corrupt part: " + str(source))
            with source.open("rb") as input_file:
                shutil.copyfileobj(input_file, output, length=1024 * 1024)
    if not matches(temporary, archive["bytes"], archive["sha256"]):
        raise ValueError("Reassembled archive failed SHA-256 verification")
    temporary.replace(target)
    return target


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, default=Path("uix_downloads"))
    parser.add_argument("--software-only", action="store_true", help="Download software/results only (about 24 MB)")
    parser.add_argument("--workers", type=int, default=4, choices=range(1, 9))
    parser.add_argument("--local-parts", type=Path, help="Verify and combine already downloaded parts without network access")
    parser.add_argument("--manifest", type=Path, help="Use a locally saved ARCHIVE_PARTS.json")
    args = parser.parse_args()
    if args.manifest:
        manifest = json.loads(args.manifest.read_text())
    else:
        with fetch(BASE_URL + "/ARCHIVE_PARTS.json") as response:
            manifest = json.load(response)
    if manifest["base_url"] != BASE_URL:
        raise ValueError("Unexpected release location")
    selected = [a for a in manifest["archives"] if not args.software_only or a["name"] == "Supplementary_Software_UIX.zip"]
    expected = {"Supplementary_Software_UIX.zip"} if args.software_only else set(ARCHIVES)
    if {a["name"] for a in selected} != expected or len(selected) != len(expected):
        raise ValueError("Unexpected archive list")
    for archive in selected:
        if (archive["bytes"], archive["sha256"]) != ARCHIVES[archive["name"]]:
            raise ValueError("Release archive identity differs from this downloader")
        for i, part in enumerate(archive["parts"]):
            if part["name"] != archive["name"] + f".part8-{i:04d}":
                raise ValueError("Unexpected part order")
        if sum(p["bytes"] for p in archive["parts"]) != archive["bytes"]:
            raise ValueError("Unexpected archive length")
    args.out.mkdir(parents=True, exist_ok=True)
    folder = args.local_parts or args.out / "parts"
    folder.mkdir(parents=True, exist_ok=True)
    parts = [p for a in selected if not matches(args.out / a["name"], a["bytes"], a["sha256"]) for p in a["parts"]]
    if not args.local_parts:
        print(f"Downloading {len(parts)} parts; rerun the same command to resume.", flush=True)
        with ThreadPoolExecutor(max_workers=args.workers) as pool:
            futures = [pool.submit(get_part, part, folder) for part in parts]
            for i, future in enumerate(as_completed(futures), 1):
                future.result()
                if i % 10 == 0 or i == len(parts):
                    print(f"Verified {i}/{len(parts)} parts", flush=True)
    for archive in selected:
        target = assemble(archive, folder, args.out)
        print("Verified archive:", target, archive["sha256"], flush=True)
    print("Extract the archives into the same parent directory; follow UIX_reproducibility/README.md.")


if __name__ == "__main__":
    main()
