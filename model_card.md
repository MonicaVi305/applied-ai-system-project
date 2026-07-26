# Model Card — VibeFinder 2.0

## Model Name
VibeFinder 2.0

## Goal / Task
Suggest the top 5 songs from a catalog that best match a user's
taste profile based on genre, mood, and energy level.

## Data Used
- 22 songs in CSV format
- Features: title, genre, mood, energy (0.0–1.0), tempo_bpm
- Limitation: small dataset may cause repetitive recommendations

## Algorithm Summary
1. Pre-filter songs that loosely match user profile (RAG retrieval)
2. Award points: genre match (+2.0), mood match (+1.0), energy similarity (0–2.0)
3. Calculate confidence score (raw score / 5.0)
4. Return top K songs sorted by score

## Observed Behavior / Biases
- Genre is weighted heaviest, so songs with matching genre rank higher
  even if mood does not match
- Pop songs appear frequently because the dataset has more pop entries
- Energy scoring always awards some points, so even poor matches
  receive non-zero scores — this can mislead low-confidence users

## Evaluation Process
Tested with 4 profiles: High-Energy Pop, Chill Lofi, Deep Intense Rock,
and Edge Case Empty Mood. Also ran 8 automated reliability tests covering
scoring logic, sorting, confidence ranges, and guardrail behavior.
All 8 tests passed.

## Intended Use
- Educational simulation of content-based filtering
- Portfolio demonstration of RAG and reliability testing concepts

## Non-Intended Use
- Not suitable for production music platforms
- Should not be used as a real recommendation engine without
  a much larger and more diverse dataset

## Ideas for Improvement
1. Add collaborative filtering using other users listening history
2. Expand dataset to 100+ songs across more genres
3. Add tempo_bpm matching as a fourth scoring dimension

## AI Collaboration Reflection

### How AI helped
AI generated the initial scaffolds for scoring logic and test structure,
saving significant time on boilerplate code.

### One helpful AI suggestion
The RAG pre-filtering step was suggested by AI and meaningfully improved
the system by reducing unnecessary scoring on irrelevant songs.

### One flawed AI suggestion
AI initially suggested returning an empty list for any profile with no
exact genre match — this was too strict and would have broken the edge
case profile. I revised the logic to use energy proximity as a fallback.

### Limitations
The system cannot learn from user feedback and will always return the
same results for the same profile, which is a fundamental limitation
of content-based filtering without user interaction data.