from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
import csv


@dataclass
class Song:
    """Represents a song and its attributes. Required by tests/test_recommender.py"""
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
    """Represents a user's taste preferences. Required by tests/test_recommender.py"""
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    target_valence: float = 0.5
    target_danceability: float = 0.5
    likes_acoustic: bool = False


# ---- Shared scoring weights (the "Algorithm Recipe" from Phase 2) ----
GENRE_WEIGHT = 2.0
MOOD_WEIGHT = 1.0
ENERGY_WEIGHT = 1.0
VALENCE_WEIGHT = 0.5
DANCEABILITY_WEIGHT = 0.5


class Recommender:
    """OOP implementation of the recommendation logic. Required by tests/test_recommender.py"""

    def __init__(self, songs: List[Song]):
        self.songs = songs

    def _score(self, user: UserProfile, song: Song) -> Tuple[float, List[str]]:
        score = 0.0
        reasons = []

        if song.genre.lower() == user.favorite_genre.lower():
            score += GENRE_WEIGHT
            reasons.append(f"genre match (+{GENRE_WEIGHT})")

        if song.mood.lower() == user.favorite_mood.lower():
            score += MOOD_WEIGHT
            reasons.append(f"mood match (+{MOOD_WEIGHT})")

        energy_pts = ENERGY_WEIGHT * (1 - abs(song.energy - user.target_energy))
        score += energy_pts
        reasons.append(f"energy closeness (+{round(energy_pts, 2)})")

        valence_pts = VALENCE_WEIGHT * (1 - abs(song.valence - user.target_valence))
        score += valence_pts
        reasons.append(f"valence closeness (+{round(valence_pts, 2)})")

        dance_pts = DANCEABILITY_WEIGHT * (1 - abs(song.danceability - user.target_danceability))
        score += dance_pts
        reasons.append(f"danceability closeness (+{round(dance_pts, 2)})")

        return round(score, 3), reasons

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        scored = [(song, self._score(user, song)[0]) for song in self.songs]
        scored.sort(key=lambda pair: pair[1], reverse=True)
        return [song for song, _ in scored[:k]]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        score, reasons = self._score(user, song)
        return f"score={score} — " + ", ".join(reasons)


def load_songs(csv_path: str) -> List[Dict]:
    """Loads songs from a CSV file. Required by src/main.py"""
    print(f"Loading songs from {csv_path}...")
    songs = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            song = dict(row)
            song["id"] = int(row["id"])
            song["energy"] = float(row["energy"])
            song["tempo_bpm"] = float(row["tempo_bpm"])
            song["valence"] = float(row["valence"])
            song["danceability"] = float(row["danceability"])
            song["acousticness"] = float(row["acousticness"])
            songs.append(song)
    print(f"Loaded songs: {len(songs)}")
    return songs


def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """
    Scores a single song against user preferences.
    user_prefs keys expected: genre, mood, energy (valence/danceability optional).
    Returns (score, reasons).
    """
    score = 0.0
    reasons = []

    if "genre" in user_prefs and song["genre"].lower() == user_prefs["genre"].lower():
        score += GENRE_WEIGHT
        reasons.append(f"genre match (+{GENRE_WEIGHT})")

    if "mood" in user_prefs and song["mood"].lower() == user_prefs["mood"].lower():
        score += MOOD_WEIGHT
        reasons.append(f"mood match (+{MOOD_WEIGHT})")

    if "energy" in user_prefs:
        energy_pts = ENERGY_WEIGHT * (1 - abs(song["energy"] - user_prefs["energy"]))
        score += energy_pts
        reasons.append(f"energy closeness (+{round(energy_pts, 2)})")

    if "valence" in user_prefs:
        valence_pts = VALENCE_WEIGHT * (1 - abs(song["valence"] - user_prefs["valence"]))
        score += valence_pts
        reasons.append(f"valence closeness (+{round(valence_pts, 2)})")

    if "danceability" in user_prefs:
        dance_pts = DANCEABILITY_WEIGHT * (1 - abs(song["danceability"] - user_prefs["danceability"]))
        score += dance_pts
        reasons.append(f"danceability closeness (+{round(dance_pts, 2)})")

    return round(score, 3), reasons


def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """
    Functional implementation of the recommendation logic.
    Returns a list of (song_dict, score, explanation_string), sorted best first.
    """
    scored = []
    for song in songs:
        score, reasons = score_song(user_prefs, song)
        explanation = ", ".join(reasons)
        scored.append((song, score, explanation))

    scored.sort(key=lambda item: item[1], reverse=True)
    return scored[:k]