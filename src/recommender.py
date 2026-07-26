import csv
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Tuple


@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """

    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float


@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """

    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool


class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """

    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        scored_songs = []
        for index, song in enumerate(self.songs):
            score, _ = score_song(self._user_to_prefs(user), self._song_to_dict(song))
            scored_songs.append((score, index, song))

        scored_songs.sort(key=lambda item: (-item[0], item[1]))
        return [song for _, _, song in scored_songs[:k]]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        _, reasons = score_song(self._user_to_prefs(user), self._song_to_dict(song))
        return _format_explanation(reasons)

    @staticmethod
    def _user_to_prefs(user: UserProfile) -> Dict[str, object]:
        return {
            "favorite_genre": user.favorite_genre,
            "favorite_mood": user.favorite_mood,
            "target_energy": user.target_energy,
            "likes_acoustic": user.likes_acoustic,
        }

    @staticmethod
    def _song_to_dict(song: Song) -> Dict[str, object]:
        return {
            "id": song.id,
            "title": song.title,
            "artist": song.artist,
            "genre": song.genre,
            "mood": song.mood,
            "energy": song.energy,
            "tempo_bpm": song.tempo_bpm,
            "valence": song.valence,
            "danceability": song.danceability,
            "acousticness": song.acousticness,
        }


def load_songs(csv_path: str) -> List[Dict]:
    """Load songs from a CSV file into a list of dictionaries."""
    songs_path = Path(csv_path)
    print(f"Loading songs from {songs_path}...")

    with songs_path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        songs = []
        for row in reader:
            songs.append(
                {
                    "id": int(row["id"]),
                    "title": row["title"],
                    "artist": row["artist"],
                    "genre": row["genre"],
                    "mood": row["mood"],
                    "energy": float(row["energy"]),
                    "tempo_bpm": float(row["tempo_bpm"]),
                    "valence": float(row["valence"]),
                    "danceability": float(row["danceability"]),
                    "acousticness": float(row["acousticness"]),
                }
            )

    return songs


def _format_explanation(reasons: List[str]) -> str:
    """Convert a list of scoring reasons into a readable explanation string."""
    if not reasons:
        return "This song did not match your profile closely."
    return " | ".join(reasons)


def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Score one song against a user's preference profile and explain the result."""
    score = 0.0
    reasons: List[str] = []

    genre_weight = 1.0
    mood_weight = 1.0
    energy_weight = 2.0 

    favorite_genre = user_prefs.get("favorite_genre")
    if favorite_genre and song.get("genre") == favorite_genre:
        score += genre_weight
        reasons.append(f"Genre matched your favorite genre '{favorite_genre}' (+{genre_weight:.1f}).")
    else: 
        
        reasons.append(f"Genre did not match '{favorite_genre}'.")

    favorite_mood = user_prefs.get("favorite_mood")
    if favorite_mood and song.get("mood") == favorite_mood:
        score += mood_weight
        reasons.append(f"Mood matched your favorite mood '{favorite_mood}' (+{mood_weight:.1f}).")
    else:
        reasons.append(f"Mood did not match '{favorite_mood}'.")

    target_energy = user_prefs.get("target_energy")
    if target_energy is not None:
        target_energy_value = float(target_energy)
        current_energy = float(song.get("energy", 0.0))
        energy_gap = abs(current_energy - target_energy_value)
        energy_similarity = max(0.0, 1.0 - energy_gap)
        energy_bonus = energy_similarity * energy_weight
        score += energy_bonus
        reasons.append(
            f"Energy was {energy_similarity:.2f} similar to your target ({current_energy:.2f} vs {target_energy_value:.2f}), adding {energy_bonus:.2f}."
        )

    return score, reasons


def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """Rank songs by score and return the top-k recommendations with explanations."""
    scored_songs = []
    for index, song in enumerate(songs):
        score, reasons = score_song(user_prefs, song)
        explanation = _format_explanation(reasons)
        scored_songs.append((song, score, explanation, index))

    scored_songs.sort(key=lambda item: (-item[1], item[3]))
    return [(song, score, explanation) for song, score, explanation, _ in scored_songs[:k]]
