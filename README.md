# 🎵 Music Recommender Simulation

## Project Summary

This project simulates a content-based music recommender. It takes a user's taste profile (favorite genre, favorite mood, and target energy/valence/danceability) and a catalog of 18 songs, scores every song using a weighted point system, and returns the top 5 matches with human-readable explanations for each score. It's built to show how a simple algorithm — not real listening data — can still produce results that feel personalized, and where that approach breaks down (like recommending upbeat songs to someone who explicitly wants "sad" music).

---

## How The System Works

Real platforms like Spotify use collaborative filtering (recommending based on what similar users liked) and content-based filtering (recommending based on a song's own attributes). This project builds a simplified content-based recommender. Each Song has: genre, mood, energy, tempo_bpm, valence, danceability, acousticness. The UserProfile stores a favorite_genre, favorite_mood, and target values for energy, valence, and danceability. The recommender scores every song by rewarding genre/mood matches and rewarding numeric features that are close to the user's target, then ranks all songs by score to return the top results.

**Algorithm Recipe:** Each song earns +2.0 points for a genre match, +1.0 for a mood match, up to +1.0 for energy closeness, up to +0.5 for valence closeness, and up to +0.5 for danceability closeness. Closeness is calculated as `1 - |song_value - target_value|`, so a song exactly matching the target earns full points and the score shrinks the further away it is. All songs are scored this way, then sorted highest-to-lowest, and the top 5 are returned as recommendations.

**User Profile Critique:** I asked my AI assistant whether this profile (favorite_genre=pop, favorite_mood=happy, target_energy=0.8, target_valence=0.8, target_danceability=0.8) could tell "intense rock" apart from "chill lofi." It can — energy alone separates them cleanly (rock ~0.91 vs lofi ~0.42 against a 0.8 target). But the critique surfaced a real weakness: because every numeric target is set high (0.8 across energy/valence/danceability), the profile can't tell "intense" apart from "happy" — a high-energy, low-valence song like angry rock scores almost as well as a genuinely happy pop song, because favorite_mood only helps when the song's mood string matches "happy" exactly, and both intense and chill songs fail that check equally. So the profile is fine at separating genres/moods far apart, but weak at distinguishing songs that are all high-energy but different in emotional tone. This is a good illustration of a filter bubble risk: without weighting valence more heavily, the system can conflate "energetic" with "positive."

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows
```

2. Install dependencies

```bash
   pip install -r requirements.txt
```

3. Run the app:

```bash
   python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
python -m pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Sample Recommendation Output

Profile: genre=pop, mood=happy, energy=0.8

Sunrise City - Score: 3.98
Because: genre match (+2.0), mood match (+1.0), energy closeness (+0.98)
Gym Hero - Score: 2.87
Because: genre match (+2.0), energy closeness (+0.87)
Rooftop Lights - Score: 1.96
Because: mood match (+1.0), energy closeness (+0.96)
Night Drive Loop - Score: 0.95
Because: energy closeness (+0.95)
Iron Horizon - Score: 0.95
Because: energy closeness (+0.95)

---

## Experiments You Tried

I ran a weight-shift experiment: temporarily changing GENRE_WEIGHT from 2.0 to 1.0 and ENERGY_WEIGHT from 1.0 to 2.0. This made energy-matching songs rank higher relative to genre matches — for example, low-energy lofi tracks started beating pop songs that only matched on genre, showing how sensitive the final ranking is to which weight is emphasized.

I also tested how the system behaves for very different user types by running 4 profiles side by side: High-Energy Pop, Chill Lofi, Deep Intense Rock, and an adversarial "Energetic Sad" profile. The first three behaved as expected — each profile's top results matched its intended vibe. The adversarial profile (pop, mood=sad, energy=0.9, valence=0.2) exposed a real weakness: it still recommended Gym Hero and Sunrise City, the same happy pop songs recommended for the High-Energy Pop profile, because genre match and energy closeness dominated the score even though "sad" didn't match at all. Full details are in `model_card.md`.

---

## Limitations and Risks

- It only works on a tiny catalog of 18 songs, so the same few tracks (especially pop songs) tend to dominate multiple different profiles.
- It does not understand lyrics, language, or cultural context — only numeric/categorical attributes like genre, mood, energy, valence, and danceability.
- It might over-favor genre, since a genre match (+2.0) is worth twice a mood match (+1.0), so a strong genre match can outrank a song that's actually a better overall vibe fit.
- It treats energy, valence, and mood as independent scores rather than understanding they should combine into a coherent "vibe," so it can recommend contradictory-feeling songs (e.g., energetic-and-happy songs to someone who wants energetic-and-sad).

You will go deeper on this in your model card.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Building this recommender taught me that a "recommendation" is really just arithmetic on whatever weights get hardcoded — when I doubled the energy weight and halved the genre weight, the rankings shifted noticeably, showing the system isn't discovering any deep truth about taste, it's doing distance math against a fixed formula. It also showed me where bias creeps into systems like this: because genre counts for more points than mood, and because the dataset skews toward a handful of pop songs, certain tracks get recommended across almost every profile regardless of fit. The adversarial test made this concrete — asking for "sad" music still returned upbeat pop songs, because the model has no way to recognize that high energy, low valence, and a "sad" mood should agree with each other rather than being scored as separate, unrelated dials.