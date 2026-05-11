"""Forgeloop Configuration"""

import os
from dotenv import load_dotenv

load_dotenv()

def get_config():
    return {
        "E2B_API_KEY": os.getenv("E2B_API_KEY", ""),
        "E2B_PERSISTENT": os.getenv("E2B_PERSISTENT", "true").lower() == "true",
        "E2B_MEMORY_GB": int(os.getenv("E2B_MEMORY_GB", "8")),
        "MAX_FORGE_ITERATIONS": int(os.getenv("MAX_FORGE_ITERATIONS", "5")),
        "SELF_OPTIMIZE": os.getenv("SELF_OPTIMIZE", "true").lower() == "true",
        "PATTERN_MEMORY": os.getenv("PATTERN_MEMORY", "true").lower() == "true",
        "STREAM_THOUGHTS": os.getenv("STREAM_THOUGHTS", "true").lower() == "true"
    }
