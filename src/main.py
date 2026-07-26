# main.py - CLI entry point for Music Recommender
from src.recommender import load_songs, recommend_songs

def print_recommendations(profile_name, user_prefs, songs, k=5):
    """Print formatted recommendations for a user profile."""
    print(f"\n{'='*50}")
    print(f"=== {profile_name} ===")
    print(f"Profile: {user_prefs}")
    print(f"{'='*50}")

    results = recommend_songs(user_prefs, songs, k)

    if not results:
        print("No recommendations found. Check your profile settings.")
        return

    for i, result in enumerate(results, 1):
        song = result["song"]
        print(f"\n{i}. {song['title']}")
        print(f"   Score: {result['score']} | Confidence: {result['confidence']}")
        print(f"   Reasons:")
        for reason in result["reasons"]:
            print(f"      - {reason}")


def main():
    songs = load_songs("data/songs.csv")
    print(f"Loaded songs: {len(songs)}")

    profiles = [
        ("High-Energy Pop", {
            "favorite_genre": "pop",
            "favorite_mood": "happy",
            "target_energy": 0.9
        }),
        ("Chill Lofi", {
            "favorite_genre": "lofi",
            "favorite_mood": "chill",
            "target_energy": 0.3
        }),
        ("Deep Intense Rock", {
            "favorite_genre": "rock",
            "favorite_mood": "intense",
            "target_energy": 0.95
        }),
        ("Edge Case - Empty Mood", {
            "favorite_genre": "pop",
            "favorite_mood": "",
            "target_energy": 0.5
        }),
    ]

    for profile_name, user_prefs in profiles:
        print_recommendations(profile_name, user_prefs, songs)


if __name__ == "__main__":
    main()