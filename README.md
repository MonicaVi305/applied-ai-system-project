# VibeFinder 2.0 — Applied AI Music Recommender

## Base Project
This project extends the **Music Recommender Simulation** from Module 3.
The original system used a weighted scoring algorithm to match songs to user
taste profiles based on genre, mood, and energy. This version adds RAG-style
retrieval, confidence scoring, guardrails, logging, and automated reliability
testing.

## Title and Summary
VibeFinder 2.0 is a content-based music recommendation system that simulates
how platforms like Spotify suggest songs. Given a user taste profile, it
retrieves relevant candidates from a song catalog, scores each one using
weighted attributes, and returns ranked recommendations with confidence scores
and human-readable explanations.

## Architecture Overview
The system follows a retrieval-then-rank pipeline:

1. **RAG Retriever** — pre-filters songs by genre, mood, or energy proximity
2. **Scoring Engine** — awards points for genre match (+2.0), mood match (+1.0), and energy similarity (0–2.0)
3. **Confidence Calculator** — converts raw score to a 0.0–1.0 trust rating
4. **Guardrails** — validates user profiles and handles missing fields safely
5. **Logger** — records every run to `logs/recommender.log`

See `diagrams/architecture.mmd` for the full system diagram.

## Setup Instructions

1. Clone the repo:
   git clone https://github.com/MonicaVi305/applied-ai-system-project.git
   cd applied-ai-system-project

2. Install dependencies (none required — uses Python standard library only)

3. Run the recommender:
   python -m src.main

4. Run reliability tests:
   python tests/test_recommender.py

## Sample Recommendation Output

### High-Energy Pop Profile
### Chill Lofi Profile
### Edge Case — Empty Mood
## Design Decisions
- **Genre weighted at +2.0** because genre is the strongest signal of taste
- **RAG pre-filtering** reduces scoring overhead on large catalogs
- **Confidence score** gives users a trust signal beyond raw points
- **Guardrails** prevent crashes on malformed profiles
- **Standard library only** keeps setup simple with no dependencies

## Testing Summary

| Test | Description | Result |
|---|---|---|
| test_load_songs | CSV loads correctly | ✅ Pass |
| test_score_song_genre_and_mood_match | Full match scores above 3.0 | ✅ Pass |
| test_score_song_no_match | No match scores below 2.0 | ✅ Pass |
| test_order_total_is_zero_when_empty | Unknown profile gets low confidence | ✅ Pass |
| test_recommend_returns_correct_count | Returns correct k results | ✅ Pass |
| test_recommendations_sorted_by_score | Results sorted highest first | ✅ Pass |
| test_confidence_score_range | Confidence always 0.0–1.0 | ✅ Pass |
| test_invalid_user_prefs | Bad profile returns empty list | ✅ Pass |

**8/8 tests passed.**

## Reflection
See `model_card.md` for full responsible AI reflection.