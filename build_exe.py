#!/usr/bin/env python3
"""
Build script for creating a standalone Windows executable.

Usage:
    python build_exe.py
    # or with uv:
    uv run build_exe.py
"""
import subprocess
import sys
from pathlib import Path


def main():
    print('Building Windows executable with PyInstaller...')

    # PyInstaller command
    cmd = [
        'pyinstaller',
        '--onefile',
        '--name', 'optimise_tax',
        '--console',
        'optimise_tax.py',
    ]

    try:
        result = subprocess.run(cmd, check=True)
        print('\n✓ Build successful!')
        print(f'Executable location: {Path("dist/optimise_tax.exe").absolute()}')
        return 0
    except subprocess.CalledProcessError as e:
        print(f'\n✗ Build failed with error: {e}')
        return 1


if __name__ == '__main__':
    sys.exit(main())
