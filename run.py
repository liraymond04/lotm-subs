#!/usr/bin/python3

import argparse
import subprocess
import json
import sys

URLS_FILE_PATH = "./urls.json"

log_tag = "[ocr]"


def log(msg: str):
    print(f"{log_tag} {msg}")


def run_script(script_name: str, arg: str = "") -> bool:
    command = ["python3", script_name]
    if arg:
        command.append(arg)

    try:
        result = subprocess.run(command, check=True)
        return result.returncode == 0
    except subprocess.CalledProcessError as e:
        log(f"Script {script_name} failed for {arg or 'batch'}: {e}")
        return False


def process_entry(i: str) -> bool:
    log(f"\n=== Processing {i} ===")

    scripts = [
        "download.py",
        "generate_timings.py",
        "ocr.py"
    ]

    for script in scripts:
        if not run_script(script, i):
            log(f"Run failed for {i}")
            return False

    log(f"Run finished for {i}")
    return True


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="run",
        description="Batch pipeline: download, generate timings, OCR subs.",
        formatter_class=argparse.MetavarTypeHelpFormatter
    )
    parser.add_argument(
        "input",
        type=str,
        help="Single entry key from urls.json",
        nargs="?"
    )

    args = parser.parse_args()

    failed = False

    if args.input:
        if not process_entry(args.input):
            failed = True
    else:
        try:
            with open(URLS_FILE_PATH, "r") as f:
                urls = json.load(f)
                for k in urls.keys():
                    if not process_entry(str(k)):
                        failed = True
        except FileNotFoundError:
            log(f"{URLS_FILE_PATH} not found.")
            sys.exit(1)

    sys.exit(1 if failed else 0)
