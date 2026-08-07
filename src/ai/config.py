"""
HELIX AI Configuration
"""

import os

AI_PROVIDER = "groq"

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

MODEL_NAME = "llama-3.3-70b-versatile"