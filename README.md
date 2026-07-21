# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

Replace this paragraph with your own summary of what your version does.

---

## How The System Works

Real platforms like Spotify use collaborative filtering (recommending based on what similar users liked) and content-based filtering (recommending based on a song's own attributes). This project builds a simplified content-based recommender. Each Song will have: genre, mood, energy, tempo_bpm, valence, danceability, acousticness. The UserProfile will store a favorite_genre, favorite_mood, and target values for energy, valence, and danceability. The recommender will score every song by rewarding genre/mood matches and rewarding numeric features that are close to the user's target, then rank all songs by score to return the top results.

User Profile Critique: I asked my AI assistant whether this profile (favorite_genre=pop, favorite_mood=happy, target_energy=0.8, target_valence=0.8, target_danceability=0.8) could tell "intense rock" apart from "chill lofi." It can — energy alone separates them cleanly (rock ~0.91 vs lofi ~0.42 against a 0.8 target). But the critique surfaced a real weakness: because every numeric target is set high (0.8 across energy/valence/danceability), the profile can't tell "intense" apart from "happy" — a high-energy, low-valence song like angry rock scores almost as well as a genuinely happy pop song, because favorite_mood only helps when the song's mood string matches "happy" exactly, and both intense and chill songs fail that check equally. So the profile is fine at separating genres/moods far apart, but weak at distinguishing songs that are all high-energy but different in emotional tone. This is a good illustration of a filter bubble risk: without weighting valence more heavily, the system can conflate "energetic" with "positive."

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

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
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Sample Recommendation Output

Paste a sample of your recommender's output here as a text block so a reader can see what it produces:

```
# e.g.:
# User profile: genre=indie, mood=chill, energy=low
# Recommendations:
#   1. ...
#   2. ...
#   3. ...
```

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or demo video link here -->

---

## Experiments You Tried

Use this section to document the experiments you ran. For example:

- What happened when you changed the weight on genre from 2.0 to 0.5
- What happened when you added tempo or valence to the score
- How did your system behave for different types of users

---

## Limitations and Risks

Summarize some limitations of your recommender.

Examples:

- It only works on a tiny catalog
- It does not understand lyrics or language
- It might over favor one genre or mood

You will go deeper on this in your model card.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this



