# File Scan Visualizer

Turn any file into a colored ASCII pixel map — readable bytes in yellow, noisy bytes in blue, and raw binary in white.

This program acts like an extened 'strings' type utility to aid finding interesting strings within binary files.

---

## 🔧 Features

- 🔍 Shows printable vs. non-printable characters
- 🌈 Colored output: Yellow (readable text), Blue (`*`), White (`.`)
- 🧠 Intelligent text detection: runs of 3+ readable chars shown as actual text
- 📄 Supports binary files and long input files
- 🛠️ Optional `--text-only` mode to extract just the readable strings

---

## 🚀 Usage

```bash
python3 main.py <filename> [--width WIDTH] [--text-only]
```

### Using uv

```bash
uv run main.py <filename> [--width WIDTH] [--text-only]
```
