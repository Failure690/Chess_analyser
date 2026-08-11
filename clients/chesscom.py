"""
Chess.com API client.
Docs: https://www.chess.com/news/view/published-data-api
No authentication required.
"""

import re
import requests

BASE_URL = "https://api.chess.com/pub"


def get_archives(username: str) -> list[str]:
    """
    Return a list of archive URLs (one per month) for a given player.
    """
    url = f"{BASE_URL}/player/{username}/games/archives"
    response = requests.get(url, headers={"User-Agent": "chess-analyser-app"})
    response.raise_for_status()
    data = response.json()
    return data["archives"]


def get_games_for_month(archive_url: str) -> list[dict]:
    """
    Given one archive URL, return the list of games played that month.
    """
    response = requests.get(archive_url, headers={"User-Agent": "chess-analyser-app"})
    response.raise_for_status()
    data = response.json()
    return data["games"]


def get_all_games(username: str) -> list[dict]:
    """
    Fetch every game a player has ever played, across all months.
    """
    all_games = []
    archives = get_archives(username)
    for archive_url in archives:
        games = get_games_for_month(archive_url)
        all_games.extend(games)
    return all_games


def extract_opening_name(eco_url: str) -> str:
    """
    Turn a Chess.com ECO URL into a readable opening name.
    """
    if not eco_url:
        return "Unknown"
    name_part = eco_url.split("/openings/")[-1]
    name_part = name_part.split("...")[0]
    name_part = name_part.replace("-", " ")
    return name_part.strip()


def normalize_game(raw_game: dict) -> dict:
    """
    Take a raw game dict from the Chess.com API and return a clean,
    flat dict with just the fields we care about.
    """
    return {
        "source": "chesscom",
        "url": raw_game.get("url"),
        "pgn": raw_game.get("pgn"),
        "time_class": raw_game.get("time_class"),
        "time_control": raw_game.get("time_control"),
        "rated": raw_game.get("rated"),
        "end_time": raw_game.get("end_time"),
        "white_username": raw_game.get("white", {}).get("username"),
        "white_rating": raw_game.get("white", {}).get("rating"),
        "white_result": raw_game.get("white", {}).get("result"),
        "black_username": raw_game.get("black", {}).get("username"),
        "black_rating": raw_game.get("black", {}).get("rating"),
        "black_result": raw_game.get("black", {}).get("result"),
        "opening_name": extract_opening_name(raw_game.get("eco", "")),
        "uuid": raw_game.get("uuid"),
    }


if __name__ == "__main__":
    username = input("Please input your Chess.com Username: ")
    current_username = username.strip().lower()

    while True:
        archives = get_archives(current_username)
        print(f"\n{current_username} has {len(archives)} months of games available.")

        latest_month_games = get_games_for_month(archives[-1])
        print(f"Most recent month has {len(latest_month_games)} games.")

        # Build a list of opponents from the most recent month of games

        opponents = []
        for game in latest_month_games:
            clean_game = normalize_game(game)
            if clean_game["white_username"].lower() == current_username:
                opponent = clean_game["black_username"]
            else:
                opponent = clean_game["white_username"]
            opponents.append(opponent)

        # Print a numbered list of opponents for the user to choose from

        for i, opponent in enumerate(opponents, start=1):
            print(f"{i}. {opponent}")

        choice = input("\nEnter the number of the opponent you want to analyze (or 'q' to quit): ")

        if choice.lower() == "q":
            break
        
        try:
            index = int(choice) -1
            current_username = opponents[index].strip().lower()
        except (ValueError, IndexError):
            print("Invalid choice. Please try again.")
