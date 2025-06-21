#!/usr/bin/python3

import subprocess
import argparse
import json
import os
import sys

URLS_FILE_PATH = "./urls.json"
DIMENSIONS_FILE_PATH = "./dimensions.json"

log_tag = "[generate_timings]"


def log(msg: str):
    print(f"{log_tag} {msg}")


def run_videosubfinder(i: str, dims: dict) -> bool:
    mp4_path = f"{i}/{i}.mp4"
    output_dir = i
    rgb_dir = f"{i}/RGBImages"

    if not os.path.exists(mp4_path):
        log(f"MP4 not found for {i}, skipping.")
        return False

    command = [
        "videosubfinder",
        "-r",
        "-i", mp4_path,
        "-o", output_dir,
        "-te", str(dims.get("te", 0.20)),
        "-be", str(dims.get("be", 0.14)),
        "-le", str(dims.get("le", 0.25)),
        "-re", str(dims.get("re", 0.75))
    ]

    log(f"Running videosubfinder for {i}")
    try:
        subprocess.run(command, text=True, check=True)
    except:
        pass

    if os.path.exists(rgb_dir) and any(f.endswith(".jpeg") for f in os.listdir(rgb_dir)):
        log(f"RGBImages output generated for {i}")
        return True
    else:
        log(f"RGBImages output missing or empty for {i}")
        return False


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="generate_timings",
        formatter_class=argparse.MetavarTypeHelpFormatter
    )
    parser.add_argument(
        "input",
        type=str,
        help="Directory name containing mp4 file",
        nargs="?"
    )

    args = parser.parse_args()

    try:
        with open(DIMENSIONS_FILE_PATH, "r") as dim_file:
            dimensions = json.load(dim_file)
    except FileNotFoundError:
        log(f"{DIMENSIONS_FILE_PATH} not found. Using default dimensions.")
        dimensions = {}

    failed = False

    if args.input:
        if not run_videosubfinder(args.input, dimensions):
            failed = True
    else:
        try:
            with open(URLS_FILE_PATH, "r") as file:
                data = json.load(file)
                for key in data.keys():
                    if not run_videosubfinder(str(key), dimensions):
                        failed = True
        except FileNotFoundError:
            log(f"{URLS_FILE_PATH} not found.")
            sys.exit(1)
        except json.JSONDecodeError as e:
            log(f"Invalid JSON in {URLS_FILE_PATH}: {e}")
            sys.exit(1)

    sys.exit(1 if failed else 0)
