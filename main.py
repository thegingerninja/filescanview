import argparse
import string
import unittest

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
    """Check if a character is printable and not whitespace/control"""
    return char in string.printable and char not in '\t\n\r\x0b\x0c'

def format_run(run, text_only, min_run=3):
    """Format a run of readable characters."""
    content = ''.join(run)
    if len(run) >= min_run:
        return content if text_only else f"{ANSI['yellow']}{content}{ANSI['reset']}"
    else:
        return '' if text_only else f"{ANSI['blue']}{'*' * len(run)}{ANSI['reset']}"

def generate_line(data, start, width, text_only):
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

def read_file(file_path):
    """Read file contents as bytes."""
    with open(file_path, 'rb') as file:
        return file.read()

def generate_ascii_map(data, width=80, text_only=False):
    lines = []
    i = 0
    while i < len(data):
        line, i = generate_line(data, i, width, text_only)
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
    data = read_file(args.filename)
    ascii_map = generate_ascii_map(data, args.width, args.text_only)

    for line in ascii_map:
        print(line)


# -------- Unit Tests --------

class TestAsciiVisualizer(unittest.TestCase):
    def test_is_readable(self):
        self.assertTrue(is_readable('A'))
        self.assertTrue(is_readable(' '))
        self.assertFalse(is_readable('\n'))
        self.assertFalse(is_readable('\x00'))

    def test_format_run_text(self):
        run = list("Hello")
        output = format_run(run, text_only=True)
        self.assertEqual(output, "Hello")

    def test_format_run_ansi(self):
        run = list("Hi")
        output = format_run(run, text_only=False)
        expected = f"{ANSI['blue']}**{ANSI['reset']}"
        self.assertEqual(output, expected)

    def test_process_line(self):
        data = bytearray(b"AB!@#12345\x00\x01\x02XYZ")
        line, _ = generate_line(data, 0, 20, text_only=True)
        self.assertIn("12345", line)
        self.assertNotIn("\x00", line)


if __name__ == "__main__":
    main()
