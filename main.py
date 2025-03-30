import argparse
import string

# ANSI color codes
ANSI = {
    'white': '\033[97m',
    'blue': '\033[94m',
    'yellow': '\033[93m',
    'green': '\033[92m',
    'cyan': '\033[96m',
    'reset': '\033[0m',
}

def print_banner():
    banner = r"""
   ___ _ _      __                      _ 
  / __(_) | ___/ _\ ___ __ _ _ __/\   /(_) _____      __
 / _\ | | |/ _ \ \ / __/ _` | '_ \ \ / / |/ _ \ \ /\ / /
/ /   | | |  __/\ \ (_| (_| | | | \ V /| |  __/\ V  V /
\/    |_|_|\___\__/\___\__,_|_| |_|\_/ |_|\___| \_/\_/
"""
    print(f"{ANSI['cyan']}{banner}")
    print(f"{ANSI['green']}Version 1.0.0 - TheGingerNinja 2025\n{ANSI['reset']}")

def is_readable(char):
    return char in string.printable and char not in '\t\n\r\x0b\x0c'

def format_run(run, text_only):
    if len(run) >= 3:
        content = ''.join(run)
        return content if text_only else f"{ANSI['yellow']}{content}{ANSI['reset']}"
    else:
        return '' if text_only else f"{ANSI['blue']}{'*' * len(run)}{ANSI['reset']}"

def process_line(data, start, width, text_only):
    line = ''
    i = start
    line_len = 0

    while i < len(data) and line_len < width:
        char = chr(data[i])
        if is_readable(char):
            run = [char]
            j = i + 1
            while j < len(data) and is_readable(chr(data[j])) and len(run) + line_len < width:
                run.append(chr(data[j]))
                j += 1
            line += format_run(run, text_only)
            line_len += len(run)
            i = j
        else:
            if not text_only:
                line += f"{ANSI['white']}.{ANSI['reset']}"
            line_len += 1
            i += 1

    return line, i

def file_to_ascii_map(file_path, width=80, text_only=False):
    with open(file_path, 'rb') as f:
        data = f.read()

    lines = []
    i = 0
    while i < len(data):
        line, i = process_line(data, i, width, text_only)
        if line.strip():
            lines.append(line)
    return lines

def main():
    parser = argparse.ArgumentParser(description="Visualize a file as a colored ASCII pixel map.")
    parser.add_argument("filename", help="Path to the input file")
    parser.add_argument("--width", type=int, default=80, help="Width of the output (default: 80)")
    parser.add_argument("--text-only", action="store_true", help="Only display yellow text (3+ readable chars)")
    args = parser.parse_args()

    print_banner()

    ascii_map = file_to_ascii_map(args.filename, args.width, args.text_only)

    for line in ascii_map:
        print(line)

if __name__ == "__main__":
    main()
