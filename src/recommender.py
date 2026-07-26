# Music Recommender - Extended with RAG, Logging, and Guardrails
import csv
import logging
import os
from datetime import datetime

# Set up logging
os.makedirs("logs", exist_ok=True)
logging.basicConfig(
    filename="logs/recommender.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def load_songs(filepath="data/songs.csv"):
    """Load songs from CSV and convert numerical values to floats."""
    songs = []
    try:
        with open(filepath, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    row["energy"] = float(row["energy"])
                    row["tempo_bpm"] = float(row["tempo_bpm"])
                    if "popularity_rating" in row:
                        row["popularity_rating"] = float(row["popularity_rating"])
                    songs.append(row)
                except ValueError as e:
                    logging.warning(f"Skipping malformed row: {row} — {e}")
        logging.info(f"Loaded {len(songs)} songs from {filepath}")
    except FileNotFoundError:
        logging.error(f"File not found: {filepath}")
        print(f"ERROR: Could not find {filepath}")
    return songs


def retrieve_relevant_songs(user_prefs, songs, top_n=15):
    """
    RAG-style retrieval: pre-filter songs that are loosely relevant
    to the user profile before scoring. This narrows the candidate pool.
    """
    # Guardrail: validate user_prefs
    if not isinstance(user_prefs, dict):
        logging.error("Invalid user_prefs: must be a dictionary")
        return []

    required_keys = ["favorite_genre", "favorite_mood", "target_energy"]
    for key in required_keys:
        if key not in user_prefs:
            logging.warning(f"Missing key in user_prefs: {key}")
            print(f"WARNING: user profile is missing '{key}'")
            return []

    candidates = []
    for song in songs:
        genre_match = song.get("genre", "").lower() == user_prefs["favorite_genre"].lower()
        mood_match = song.get("mood", "").lower() == user_prefs["favorite_mood"].lower()
        energy_close = abs(song["energy"] - user_prefs["target_energy"]) <= 0.5

        if genre_match or mood_match or energy_close:
            candidates.append(song)

    logging.info(f"RAG retrieval: {len(candidates)} candidates from {len(songs)} songs")
    return candidates[:top_n]


def score_song(user_prefs, song):
    """Score a single song against user preferences and return score + reasons."""
    score = 0.0
    reasons = []

    # Guardrail: skip songs missing required fields
    required = ["genre", "mood", "energy"]
    for field in required:
        if field not in song:
            logging.warning(f"Song missing field '{field}': {song}")
            return 0.0, [f"Song data incomplete — missing {field}"]

    # Genre match
    if song["genre"].lower() == user_prefs.get("favorite_genre", "").lower():
        score += 2.0
        reasons.append(f"Genre matched your favorite genre '{user_prefs['favorite_genre']}' (+2.0).")
    else:
        reasons.append(f"Genre did not match '{user_prefs.get('favorite_genre')}'.")

    # Mood match
    if song["mood"].lower() == user_prefs.get("favorite_mood", "").lower():
        score += 1.0
        reasons.append(f"Mood matched your favorite mood '{user_prefs['favorite_mood']}' (+1.0).")
    else:
        reasons.append(f"Mood did not match '{user_prefs.get('favorite_mood')}'.")

    # Energy similarity
    energy_gap = abs(song["energy"] - user_prefs.get("target_energy", 0.5))
    energy_score = round(max(0.0, 1.0 - energy_gap) * 2, 2)
    score += energy_score
    reasons.append(
        f"Energy similarity score: {energy_score:.2f} "
        f"(song={song['energy']:.2f} vs target={user_prefs.get('target_energy', 0.5):.2f})."
    )

    return round(score, 2), reasons


def calculate_confidence(score, max_score=5.0):
    """Calculate a confidence score between 0.0 and 1.0."""
    return round(min(score / max_score, 1.0), 2)


def recommend_songs(user_prefs, songs, k=5):
    """
    Full pipeline: retrieve relevant songs (RAG),
    score each one, and return top K with confidence scores.
    """
    # Guardrail: check k is valid
    if not isinstance(k, int) or k <= 0:
        logging.warning(f"Invalid k value: {k}, defaulting to 5")
        k = 5

    # RAG retrieval step
    candidates = retrieve_relevant_songs(user_prefs, songs)

    if not candidates:
        logging.warning("No candidates retrieved — returning empty list")
        return []

    scored = []
    for song in candidates:
        score, reasons = score_song(user_prefs, song)
        confidence = calculate_confidence(score)
        scored.append({
            "song": song,
            "score": score,
            "confidence": confidence,
            "reasons": reasons
        })

    # Sort by score descending
    scored.sort(key=lambda x: x["score"], reverse=True)

    logging.info(f"Returning top {k} recommendations for profile: {user_prefs}")
    return scored[:k] 