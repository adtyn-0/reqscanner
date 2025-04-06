
# reqscanner

**reqscanner** is a lightweight Python utility script that scans your project for imported modules and generates a `requirements.txt` file based on what's actually used and installed.

It’s similar in concept to tools like `pigar`, but more minimal and customizable for personal or small-scale projects.

---

## Features

- Detects all imported modules using AST
- Matches import aliases (e.g. `np` → `numpy`, `cv2` → `opencv-python`)
- Only includes third-party packages (excludes standard library)
- Skips virtual environments and cache folders
- Generates a clean `requirements.txt`
- Optional output file name and scan directory

---

## Usage

### 1. Basic scan in current directory:
```bash
python reqscanner.py
```

### 2. Scan a specific folder and set output file:
```bash
python reqscanner.py /path/to/project --output my-reqs.txt
```

---

## Example Output

```
numpy==1.24.3
pandas==1.5.2
scikit-learn==1.2.0
matplotlib==3.6.0
```

---

## Notes

- Only includes packages that are installed in your current Python environment.
- If a module is imported but not installed, it will be skipped with a warning.
- The alias map can be customized to support project-specific import styles.
``
