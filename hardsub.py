#!/usr/bin/python3

import subprocess
import argparse
import json
import os
import sys

URLS_FILE_PATH = "./urls.json"

log_tag = "[hardsub]"


def log(msg: str):
    print(f"{log_tag} {msg}")


def hardsub(i: str) -> bool:
    mp4_path = f"{i}/{i}.mp4"
    ass_path = f"{i}/{i}.ass"
    output_path = f"{i}/{i}_subbed.mp4"

    if not (os.path.exists(mp4_path) and os.path.exists(ass_path)):
        log(f"Missing .mp4 or .ass file for {i}, skipping.")
        return False

    command = f"ffmpeg -i '{mp4_path}' -vf 'ass={ass_path}' '{output_path}' -y"

    try:
        subprocess.check_output(command, shell=True, text=True)
        log(f"Hardsubbing for file {i} completed")
        return True
    except subprocess.CalledProcessError as e:
        log(f"Hardsubbing for file {i} failed: {e}")
        return False


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="hardsub",
        formatter_class=argparse.MetavarTypeHelpFormatter
    )
    parser.add_argument(
        "input",
        type=str,
        help="File to hardsub",
        nargs="?"
    )

    args = parser.parse_args()
    failed = False

    if args.input:
        if not hardsub(args.input):
            failed = True
    else:
        try:
            with open(URLS_FILE_PATH, "r") as file:
                data = json.load(file)
                for item in data:
                    if not hardsub(item):
                        failed = True
        except FileNotFoundError:
            log(f"{URLS_FILE_PATH} not found.")
            sys.exit(1)
        except json.JSONDecodeError as e:
            log(f"Invalid JSON in {URLS_FILE_PATH}: {e}")
            sys.exit(1)

    sys.exit(1 if failed else 0)
