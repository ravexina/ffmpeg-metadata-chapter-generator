import argparse


def process_line(line):
    time_str, chapter_name = line.strip().split("\t")
    hh, mm, ss = map(int, time_str.split(":"))
    line_ms = (hh * 3600 + mm * 60 + ss) * 1000
    return line_ms, chapter_name


def convert_chapters(input_file, output_file):
    with open(input_file, "r") as f:
        lines = f.readlines()

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

    with open(output_file, "w") as f:
        f.write("\n".join(output))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Convert chapters file to FFmpeg metadata format."
    )
    parser.add_argument("input_file", help="Path to the input chapters file.")
    parser.add_argument("output_file", help="Path to the output FFmpeg metadata file.")
    args = parser.parse_args()

    convert_chapters(args.input_file, args.output_file)
    print("Conversion complete.")
