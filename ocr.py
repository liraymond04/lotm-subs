#!/usr/bin/python3

import subprocess
import argparse
import json
import os
import sys

URLS_FILE_PATH = "./urls.json"

log_tag = "[ocr]"


def log(msg: str):
    print(f"{log_tag} {msg}")


def run_rapid_videocr(i: str) -> bool:
    input_path = f"{i}/RGBImages"
    output_dir = i
    output_file = i

    if not os.path.exists(input_path):
        log(f"Missing input directory: {input_path}, skipping.")
        return False

    command = [
        "rapid_videocr",
        "-i", input_path,
        "-o", "ass",
        "-s", output_dir,
        "-f", output_file
    ]

    try:
        subprocess.check_output(command, text=True)
        log(f"rapid_videocr completed for {i}")
        return True
    except subprocess.CalledProcessError as e:
        log(f"rapid_videocr failed for {i}: {e}")
        return False


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="rapid_videocr_runner",
        formatter_class=argparse.MetavarTypeHelpFormatter
    )
    parser.add_argument(
        "input",
        type=str,
        help="Folder name to process (e.g., '13')",
        nargs="?"
    )

    args = parser.parse_args()
    failed = False

    if args.input:
        if not run_rapid_videocr(args.input):
            failed = True
    else:
        try:
            with open(URLS_FILE_PATH, "r") as file:
                data = json.load(file)
                for key in data.keys():
                    if not run_rapid_videocr(str(key)):
                        failed = True
        except FileNotFoundError:
            log(f"{URLS_FILE_PATH} not found. Please provide a directory or create the file.")
            sys.exit(1)
        except json.JSONDecodeError as e:
            log(f"Invalid JSON in {URLS_FILE_PATH}: {e}")
            sys.exit(1)

    sys.exit(1 if failed else 0)
