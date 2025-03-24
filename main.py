import argparse
import string

# ANSI color codes
WHITE = '\033[97m'
BLUE = '\033[94m'
YELLOW = '\033[93m'
GREEN = '\033[92m'
CYAN = '\033[96m'
RESET = '\033[0m'

def print_banner():
    banner = r"""
   ___ _ _      __                      _ 
  / __(_) | ___/ _\ ___ __ _ _ __/\   /(_) _____      __
 / _\ | | |/ _ \ \ / __/ _` | '_ \ \ / / |/ _ \ \ /\ / /
/ /   | | |  __/\ \ (_| (_| | | | \ V /| |  __/\ V  V /
\/    |_|_|\___\__/\___\__,_|_| |_|\_/ |_|\___| \_/\_/
"""
    print(f"{CYAN}{banner}")
    print(f"{GREEN}Version 1.0.0 - TheGingerNinja 2025\n{RESET}")

def is_readable(char):
    return char in string.printable and char not in '\t\n\r\x0b\x0c'

def file_to_ascii_map(file_path, width=80, text_only=False):
    with open(file_path, 'rb') as f:
        data = f.read()

    lines = []
    i = 0
    while i < len(data):
        line = ''
        x = 0
        while x < width and i < len(data):
            char = chr(data[i])
            if is_readable(char):
                # Look ahead for a readable run
                run = [char]
                j = i + 1
                while j < len(data) and is_readable(chr(data[j])) and len(run) + x < width:
                    run.append(chr(data[j]))
                    j += 1

                if len(run) >= 3:
                    content = ''.join(run)
                    if text_only:
                        line += content
                    else:
                        line += f"{YELLOW}{content}{RESET}"
                    x += len(run)
                    i = j
                else:
                    if not text_only:
                        line += f"{BLUE}{'*' * len(run)}{RESET}"
                    x += len(run)
                    i += len(run)
            else:
                if not text_only:
                    line += f"{WHITE}.{RESET}"
                i += 1
                x += 1
        if line.strip():  # Avoid printing empty lines in text-only mode
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

