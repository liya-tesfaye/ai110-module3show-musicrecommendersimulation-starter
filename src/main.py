"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from src.recommender import load_songs, recommend_songs


def main() -> None:
    songs = load_songs("data/songs.csv")

    profiles = {
        "High-Energy Pop": {"genre": "pop", "mood": "happy", "energy": 0.9, "valence": 0.85, "danceability": 0.85},
        "Chill Lofi": {"genre": "lofi", "mood": "chill", "energy": 0.3, "valence": 0.5, "danceability": 0.5},
        "Deep Intense Rock": {"genre": "rock", "mood": "intense", "energy": 0.9, "valence": 0.4, "danceability": 0.5},
        # Adversarial: conflicting signals (high energy + sad mood)
        "Adversarial - Energetic Sad": {"genre": "pop", "mood": "sad", "energy": 0.9, "valence": 0.2, "danceability": 0.8},
    }

    for label, user_prefs in profiles.items():
        print(f"\n=== {label} ===")
        print(f"Profile: {user_prefs}")
        recommendations = recommend_songs(user_prefs, songs, k=5)
        for song, score, explanation in recommendations:
            print(f"{song['title']} - Score: {score:.2f}")
            print(f"Because: {explanation}")
            print()


if __name__ == "__main__":
    main()


