"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.
"""

from pathlib import Path
from typing import Any, Dict, List, Tuple

try:
    from .recommender import load_songs, recommend_songs
except ImportError:  # pragma: no cover - supports direct script execution
    from recommender import load_songs, recommend_songs


ROOT_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = ROOT_DIR / "data" / "songs.csv"


def print_recommendations(label: str, user_prefs: Dict[str, Any], songs: List[Dict[str, Any]], k: int = 5) -> None:
    print(f"\n=== {label} ===")
    print(
        "Profile: "
        f"genre={user_prefs.get('favorite_genre')}, "
        f"mood={user_prefs.get('favorite_mood')}, "
        f"energy={user_prefs.get('target_energy')}, "
        f"likes_acoustic={user_prefs.get('likes_acoustic')}"
    )

    recommendations = recommend_songs(user_prefs, songs, k=k)
    for index, rec in enumerate(recommendations, start=1):
        song, score, explanation = rec
        print(f"{index}. {song['title']}")
        print(f"   Score: {score:.2f}")
        print("   Reasons:")
        for reason in explanation.split(" | "):
            if reason:
                print(f"      - {reason}")
        print()


def main() -> None:  
    songs = load_songs(str(DATA_PATH))
    if not songs:
        raise ValueError(f"No songs were loaded from {DATA_PATH}")

    print(f"Loaded songs: {len(songs)}")

    profiles: List[Tuple[str, Dict[str, Any]]] = [
        (
            "High-Energy Pop",
            {
                "favorite_genre": "pop",
                "favorite_mood": "happy",
                "target_energy": 0.9,
                "likes_acoustic": False,
            },
        ),
        (
            "Chill Lofi",
            {
                "favorite_genre": "lofi",
                "favorite_mood": "chill",
                "target_energy": 0.3,
                "likes_acoustic": True,
            },
        ),
        (
            "Deep Intense Rock",
            {
                "favorite_genre": "rock",
                "favorite_mood": "intense",
                "target_energy": 0.95,
                "likes_acoustic": False,
            },
        ),
    ]

    for label, user_prefs in profiles:
        print_recommendations(label, user_prefs, songs, k=5)


if __name__ == "__main__":
    main()
