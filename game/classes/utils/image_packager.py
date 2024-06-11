"""
image_packager.py

Author: Liam Nixon
Last modified: 13/05/2024

Packages images for export to PyInstaller
"""

import os
import sys


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)