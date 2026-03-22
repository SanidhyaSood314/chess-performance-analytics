import requests
import time
from typing import List


BASE_URL = "https://api.chess.com/pub/player"

HEADERS = {
    "User-Agent": "ChessAnalyticsApp/1.0 (educational project)"
}


class ChessComAPIError(Exception):
    """Custom exception for Chess.com API errors."""
    pass


def fetch_archives(username: str) -> List[str]:
    """
    Fetch list of monthly archive URLs for a Chess.com user.
    """
    username = username.lower().strip()
    url = f"{BASE_URL}/{username}/games/archives"

    response = requests.get(url, headers=HEADERS)

    if response.status_code != 200:
        raise ChessComAPIError(
            f"Failed to fetch archives (status code: {response.status_code})"
        )

    data = response.json()
    return data.get("archives", [])


def fetch_monthly_pgn(archive_url: str) -> List[str]:
    """
    Fetch PGN strings from a single monthly archive.
    """
    response = requests.get(archive_url, headers=HEADERS)

    if response.status_code != 200:
        return []

    games = response.json().get("games", [])

    return [game["pgn"] for game in games if "pgn" in game]


def fetch_all_pgn(username: str, delay: float = 0.3) -> str:
    """
    Fetch all PGN games for a user and return
    one combined PGN string.
    """

    archives = fetch_archives(username)

    if not archives:
        return ""

    all_pgn_games = []

    for archive_url in archives:
        monthly_pgn = fetch_monthly_pgn(archive_url)
        all_pgn_games.extend(monthly_pgn)

        # Respect API rate limits
        time.sleep(delay)

    return "\n\n".join(all_pgn_games)