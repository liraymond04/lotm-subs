#!/usr/bin/python3

import os
import json
import argparse
import sys
import shutil

URLS_FILE_PATH = "./urls.json"
STYLE_FILE_PATH = "./style.ass"

log_tag = "[apply_style]"


def log(msg: str):
    print(f"{log_tag} {msg}")


def load_style() -> tuple[str, str]:
    if not os.path.isfile(STYLE_FILE_PATH):
        log(f"{STYLE_FILE_PATH} not found.")
        sys.exit(1)

    with open(STYLE_FILE_PATH, "r", encoding="utf-8") as f:
        style_line = f.readline().strip()

    if not style_line.startswith("Style:"):
        log("Style file must start with 'Style:' line.")
        sys.exit(1)

    try:
        style_fields = style_line.split(":", 1)[1].split(",")
        style_name = style_fields[0].strip()
    except Exception as e:
        log(f"Failed to parse style name: {e}")
        sys.exit(1)

    return style_line, style_name


def apply_style_to_file(filepath: str, style_line: str, style_name: str) -> bool:
    try:
        # Backup original file
        backup_path = filepath + ".bak"
        shutil.copy(filepath, backup_path)
        log(f"Backed up original file to {backup_path}")

        with open(filepath, "r", encoding="utf-8") as f:
            lines = f.readlines()

        new_lines = []
        in_styles = False
        style_present = False
        last_style_idx = None

        for idx, line in enumerate(lines):
            stripped = line.strip()

            new_lines.append(line)

            if stripped.startswith("[V4+ Styles]"):
                in_styles = True
                continue

            if in_styles:
                if stripped.startswith("Style:"):
                    if style_name in stripped:
                        style_present = True
                    last_style_idx = idx
                elif stripped.startswith("["):
                    in_styles = False

        # Insert the new style line if not present
        if not style_present:
            insert_idx = (last_style_idx + 1) if last_style_idx is not None else len(new_lines)
            new_lines.insert(insert_idx, style_line + "\n")
            if insert_idx + 1 < len(new_lines) and not new_lines[insert_idx + 1].strip():
                pass  # already has blank line
            elif insert_idx + 1 < len(new_lines) and new_lines[insert_idx + 1].strip().startswith("["):
                new_lines.insert(insert_idx + 1, "\n")  # insert blank line before [Events]
            log(f"Inserted custom style '{style_name}'")

        # Replace all Dialogue style names
        for i in range(len(new_lines)):
            if new_lines[i].strip().startswith("Dialogue:"):
                parts = new_lines[i].split(",", 9)
                if len(parts) >= 10:
                    parts[3] = style_name
                    new_lines[i] = ",".join(parts)

        with open(filepath, "w", encoding="utf-8") as f:
            f.writelines(new_lines)

        log(f"Updated style in {filepath}")
        return True

    except Exception as e:
        log(f"Failed to process {filepath}: {e}")
        return False


def process_entry(entry: str, style_line: str, style_name: str) -> bool:
    ass_file = os.path.join(entry, f"{entry}.ass")
    if not os.path.isfile(ass_file):
        log(f"{ass_file} not found.")
        return False

    return apply_style_to_file(ass_file, style_line, style_name)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="apply_style",
        formatter_class=argparse.MetavarTypeHelpFormatter
    )
    parser.add_argument(
        "input",
        type=str,
        help="Entry name to process",
        nargs="?"
    )

    args = parser.parse_args()
    style_line, style_name = load_style()

    failed = False

    try:
        with open(URLS_FILE_PATH, "r") as file:
            data = json.load(file)

            if args.input:
                if not process_entry(args.input, style_line, style_name):
                    failed = True
            else:
                for key in data.keys():
                    if not process_entry(key, style_line, style_name):
                        failed = True

    except FileNotFoundError:
        log(f"{URLS_FILE_PATH} not found.")
        sys.exit(1)
    except json.JSONDecodeError as e:
        log(f"Invalid JSON in {URLS_FILE_PATH}: {e}")
        sys.exit(1)

    sys.exit(1 if failed else 0)
