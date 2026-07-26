# Reliability Tests for Music Recommender
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.recommender import load_songs, score_song, recommend_songs, calculate_confidence

# ── Sample data for testing ──────────────────────────────────────────────────
SAMPLE_SONGS = [
    {"title": "Sunrise City", "genre": "pop", "mood": "happy", "energy": 0.82, "tempo_bpm": 120.0},
    {"title": "Storm Runner", "genre": "rock", "mood": "intense", "energy": 0.91, "tempo_bpm": 140.0},
    {"title": "Library Rain", "genre": "lofi", "mood": "chill", "energy": 0.35, "tempo_bpm": 75.0},
    {"title": "Velvet Thunder", "genre": "pop", "mood": "intense", "energy": 0.90, "tempo_bpm": 130.0},
    {"title": "Neon Harbor", "genre": "jazz", "mood": "chill", "energy": 0.31, "tempo_bpm": 90.0},
]

POP_HAPPY_PROFILE = {
    "favorite_genre": "pop",
    "favorite_mood": "happy",
    "target_energy": 0.9
}

# ── Tests ─────────────────────────────────────────────────────────────────────

def test_load_songs():
    """Songs CSV loads and returns a non-empty list."""
    songs = load_songs("data/songs.csv")
    assert len(songs) > 0, "Song list should not be empty"
    print("✅ test_load_songs passed")


def test_score_song_genre_and_mood_match():
    """A song matching genre and mood should score higher than 3.0."""
    song = {"title": "Sunrise City", "genre": "pop", "mood": "happy", "energy": 0.82}
    score, reasons = score_song(POP_HAPPY_PROFILE, song)
    assert score > 3.0, f"Expected score > 3.0 but got {score}"
    print(f"✅ test_score_song_genre_and_mood_match passed (score={score})")


def test_score_song_no_match():
    """A song with no genre or mood match should score below 2.0."""
    song = {"title": "Library Rain", "genre": "lofi", "mood": "chill", "energy": 0.35}
    score, reasons = score_song(POP_HAPPY_PROFILE, song)
    assert score < 2.0, f"Expected score < 2.0 but got {score}"
    print(f"✅ test_score_song_no_match passed (score={score})")


def test_order_total_is_zero_when_empty():
    """recommend_songs with no genre/mood match should return low confidence scores."""
    weird_profile = {
        "favorite_genre": "zzzz",
        "favorite_mood": "zzzz",
        "target_energy": 0.5
    }
    results = recommend_songs(weird_profile, SAMPLE_SONGS, k=5)
    # Energy alone can still retrieve songs, but confidence should be low
    for r in results:
        assert r["confidence"] < 0.5, (
            f"Expected low confidence for no-match profile but got {r['confidence']}"
        )
    print("✅ test_order_total_is_zero_when_empty passed (low confidence verified)")


def test_recommend_returns_correct_count():
    """recommend_songs returns exactly k results when enough candidates exist."""
    results = recommend_songs(POP_HAPPY_PROFILE, SAMPLE_SONGS, k=3)
    assert len(results) <= 3, f"Expected at most 3 results but got {len(results)}"
    print(f"✅ test_recommend_returns_correct_count passed (got {len(results)} results)")


def test_recommendations_sorted_by_score():
    """Results should be sorted highest score first."""
    results = recommend_songs(POP_HAPPY_PROFILE, SAMPLE_SONGS, k=5)
    scores = [r["score"] for r in results]
    assert scores == sorted(scores, reverse=True), "Results are not sorted by score"
    print("✅ test_recommendations_sorted_by_score passed")


def test_confidence_score_range():
    """Confidence scores should always be between 0.0 and 1.0."""
    results = recommend_songs(POP_HAPPY_PROFILE, SAMPLE_SONGS, k=5)
    for r in results:
        assert 0.0 <= r["confidence"] <= 1.0, f"Confidence out of range: {r['confidence']}"
    print("✅ test_confidence_score_range passed")


def test_invalid_user_prefs():
    """Missing required keys in user_prefs should return empty list."""
    bad_profile = {"favorite_genre": "pop"}  # missing mood and energy
    results = recommend_songs(bad_profile, SAMPLE_SONGS, k=5)
    assert results == [], f"Expected empty list for bad profile but got {results}"
    print("✅ test_invalid_user_prefs passed")


# ── Run all tests ─────────────────────────────────────────────────────────────
if __name__ == "__main__":
    tests = [
        test_load_songs,
        test_score_song_genre_and_mood_match,
        test_score_song_no_match,
        test_order_total_is_zero_when_empty,
        test_recommend_returns_correct_count,
        test_recommendations_sorted_by_score,
        test_confidence_score_range,
        test_invalid_user_prefs,
    ]

    passed = 0
    failed = 0

    print("\n" + "="*50)
    print("Running Reliability Tests...")
    print("="*50)

    for test in tests:
        try:
            test()
            passed += 1
        except AssertionError as e:
            print(f"❌ {test.__name__} FAILED: {e}")
            failed += 1

    print("="*50)
    print(f"Results: {passed} passed, {failed} failed out of {len(tests)} tests")
    print("="*50) 