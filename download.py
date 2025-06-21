#!/usr/bin/python3

import os
import subprocess
import argparse
import json
import sys

URLS_FILE_PATH = "./urls.json"

log_tag = "[download]"


def log(msg: str):
    print(f"{log_tag} {msg}")


def checkdir(dir: str) -> None:
    if not os.path.exists(dir):
        os.makedirs(dir)


def download_from_url(i: str, url: str) -> bool:
    try:
        checkdir(i)

        result = subprocess.check_output(
            f"yt-dlp --cookies-from-browser firefox {url} -o {i}/{i} -S res,ext:mp4:m4a --recode mp4",
            shell=True,
            text=True
        )

        result = result.strip().split("\n")[-2]

        if "Deleting original file" in result:
            log(f"{i}.mp4 has been downloaded")
        else:
            log(result)

        return True

    except subprocess.CalledProcessError as e:
        log(f"Download for file {i} from {url} failed: {e}")
        return False


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="download",
        formatter_class=argparse.MetavarTypeHelpFormatter
    )
    parser.add_argument(
        "input",
        type=str,
        help="File to download",
        nargs="?"
    )

    args = parser.parse_args()

    failed = False

    try:
        with open(URLS_FILE_PATH, "r") as file:
            data = json.load(file)

            if args.input:
                i = args.input
                log(f"Downloading file {i} from {data[i]}")
                if not download_from_url(i, data[i]):
                    failed = True
            else:
                for k, v in data.items():
                    log(f"Downloading file {k} from {v}")
                    if not download_from_url(k, v):
                        failed = True
    except FileNotFoundError:
        log(f"{URLS_FILE_PATH} not found.")
        sys.exit(1)
    except KeyError as e:
        log(f"Key {e} not found in {URLS_FILE_PATH}.")
        sys.exit(1)
    except json.JSONDecodeError as e:
        log(f"Invalid JSON in {URLS_FILE_PATH}: {e}")
        sys.exit(1)

    sys.exit(1 if failed else 0)
