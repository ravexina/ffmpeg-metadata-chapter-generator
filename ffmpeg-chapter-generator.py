#!/usr/bin/env python3

import re
import argparse
from pathlib import Path
from typing import Tuple


def process_line(line: str) -> Tuple[int, str]:
    # Search for HH:MM:SS/H:MM:SS or MM:SS/M:SS
    match = re.match(r"(\d{1,2}:\d{2}:\d{2})|(\d{1,2}:\d{2})", line.strip())
    if not match:
        raise ValueError(f"Invalid timestamp on line: {line}")

    time_str = match.group(1) or f"00:{match.group(2)}"
    chapter_name = line[match.end():].strip()

    hh, mm, ss = map(int, time_str.split(":"))
    line_ms = (hh * 3600 + mm * 60 + ss) * 1000
    return line_ms, chapter_name


def convert_chapters(input_file: Path, output_file: Path) -> None:
    lines = input_file.read_text().strip().splitlines(keepends=True)

    output = []
    output.append(";FFMETADATA1\n")
    timebase = 1000  # Timebase in milliseconds

    for index, line in enumerate(lines):
        start_ms, chapter_name = process_line(line)
        try:
            next_start_ms, _ = process_line(lines[index + 1])
        except IndexError:
            next_start_ms = ""

        print("START", start_ms)
        print("END", next_start_ms)
        print("--")

        chapter_info = (
            f"[CHAPTER]\n"
            f"TIMEBASE=1/{timebase}\n"
            f"START={start_ms}\n"
            f"END={next_start_ms}\n"
            f"title={chapter_name.strip()}\n"
        )
        output.append(chapter_info)

    output_file.write_text("\n".join(output))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Convert chapters file to FFmpeg metadata format."
    )
    parser.add_argument("input_file", help="Path to the input chapters file.")
    parser.add_argument("output_file", nargs="?", help="Path to the output FFmpeg metadata file (optional).")
    args = parser.parse_args()

    input_file = Path(args.input_file)
    output_file = Path(args.output_file) if args.output_file else Path(input_file).with_suffix(".ffmeta")

    convert_chapters(input_file, output_file)
    print(f"Conversion complete! Chapter file saved to: '{output_file}'")
