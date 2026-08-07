"""
HELIX Logger
"""

from datetime import datetime


def log(message: str):
    """Print a timestamped log message."""
    current_time = datetime.now().strftime("%H:%M:%S")
    print(f"[{current_time}] {message}")