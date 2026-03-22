# config/settings.py

import os


# -------------------------------------------------
# Chess.com Username
# -------------------------------------------------

USERNAME = "Sanu314"


# -------------------------------------------------
# App UI Configuration
# -------------------------------------------------

APP_TITLE = "♟️ Chess Performance Analytics"
APP_DESCRIPTION = "Upload your PGN file to begin analysis."

PAGE_CONFIG = {
    "page_title": "Chess Performance Analytics",
    "layout": "wide"
}


# -------------------------------------------------
# Engine Configuration
# -------------------------------------------------

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

ENGINE_PATH = os.path.join(BASE_DIR, "engines", "stockfish.exe")