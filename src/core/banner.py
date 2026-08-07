"""
HELIX Banner
"""

from .config import APP_NAME, VERSION


def show_banner():
    print("=" * 60)
    print(f"{APP_NAME:^60}")
    print(f"{'AI Desktop Assistant':^60}")
    print(f"{'Version ' + VERSION:^60}")
    print("=" * 60)
    print()