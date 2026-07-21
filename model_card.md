# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name

VibeFinder 1.0

---

## 2. Intended Use

VibeFinder generates a ranked top-5 song list based on a user's stated taste profile — favorite genre, favorite mood, and target energy/valence/danceability. It assumes the user can articulate their preferences as simple numeric/categorical values, and that a good recommendation is simply "a song similar to what you said you like." This is a classroom exploration of content-based filtering, not a system built for real users — it uses a tiny, hand-made catalog rather than real listening data.

---

## 3. How the Model Works

Each song has a genre, a mood, and three 0-1 scale attributes: energy, valence (positivity), and danceability. The user's profile states a favorite genre, favorite mood, and target values for those same three attributes. To score a song, the model gives +2.0 points if the genre matches, +1.0 point if the mood matches, and up to 2.0 more points spread across energy/valence/danceability based on how close the song's values are to what the user asked for — the closer the match, the more points. Every song in the catalog gets scored this way, then they're sorted from highest to lowest score, and the top 5 are shown along with the specific reasons behind each score. The starter logic was just a placeholder that returned the first k songs with no real scoring — I replaced it with this weighted formula and added human-readable explanations for each recommendation.

---

## 4. Data

The catalog has 18 songs across genres including pop, lofi, rock, ambient, jazz, synthwave, indie pop, electronic, rnb, folk, edm, and hiphop, with moods like happy, chill, intense, romantic, nostalgic, euphoric, melancholy, and confident. I expanded the original 10-song starter file with 8 additional songs to add more genre/mood diversity. What's missing: no lyrics, no artist popularity, no release era or cultural context, and no real listener behavior (plays, skips) — the dataset only captures surface-level audio attributes, which is a narrow slice of what actually makes up someone's musical taste.

---

## 5. Strengths

The system gives clearly reasonable results when a user's genre, mood, and numeric targets all point the same direction — for example, the default "pop/happy/energy=0.8" profile correctly ranked Sunrise City and Gym Hero at the top, which matched my own intuition. It also cleanly separates opposite-vibe profiles: Chill Lofi and High-Energy Pop produced completely different top-5 lists, showing the energy/valence/danceability scoring is doing real discriminating work, not just picking randomly. The explanations (e.g., "genre match (+2.0), energy closeness (+0.98)") make it easy to see exactly why a song ranked where it did, which is valuable for trust and debugging.

---

## 6. Limitations and Bias

This system over-prioritizes genre matches because they're worth +2.0, double a mood match — so a strong genre match can outrank a song that's actually a much better overall vibe fit. With only 18 songs and just 3-4 pop tracks, "pop" profiles keep recommending the same 2 songs (Gym Hero, Sunrise City) regardless of mood or valence targets, since the genre bonus alone puts them near the top. The adversarial test made this concrete: a user wanting "sad" music still got upbeat pop recommended, because the scoring function has no way to recognize that high energy + low valence + sad mood is an internally consistent request — it just sums independent closeness scores.

---

## 7. Evaluation

I tested 4 profiles: High-Energy Pop, Chill Lofi, Deep Intense Rock, and an adversarial Energetic-Sad profile.

- **High-Energy Pop vs Chill Lofi:** Pop profile surfaces upbeat, danceable tracks (Sunrise City, Gym Hero); lofi profile shifts entirely to low-energy, high-acousticness tracks (Rainy Window, Library Rain) — makes sense since target_energy is nearly opposite (0.9 vs 0.3).
- **Deep Intense Rock vs High-Energy Pop:** Both want high energy, but rock's low target_valence (0.4) correctly favors moodier/angrier tracks like Iron Horizon and Storm Runner instead of upbeat pop.
- **Adversarial - Energetic Sad:** This profile exposed a limitation — the system recommended high-energy pop songs that aren't actually "sad" in any real sense, because it scores energy and mood independently rather than checking if the combination makes musical sense. Asking for genre=pop, mood=sad, energy=0.9, valence=0.2 still returned Gym Hero and Sunrise City at the top — the same songs recommended for "High-Energy Pop" — because the genre match and high energy closeness dominated the score even though the mood didn't match at all.

### Raw output

=== High-Energy Pop ===
Profile: {'genre': 'pop', 'mood': 'happy', 'energy': 0.9, 'valence': 0.85, 'danceability': 0.85}
Sunrise City - Score: 4.88
Because: genre match (+2.0), mood match (+1.0), energy closeness (+0.92), valence closeness (+0.49), danceability closeness (+0.47)

Gym Hero - Score: 3.92
Because: genre match (+2.0), energy closeness (+0.97), valence closeness (+0.46), danceability closeness (+0.48)

Rooftop Lights - Score: 2.83
Because: mood match (+1.0), energy closeness (+0.86), valence closeness (+0.48), danceability closeness (+0.48)

Neon Pulse - Score: 1.93
Because: energy closeness (+0.95), valence closeness (+0.5), danceability closeness (+0.47)

Solar Flare - Score: 1.90
Because: energy closeness (+1.0), valence closeness (+0.42), danceability closeness (+0.48)


=== Chill Lofi ===
Profile: {'genre': 'lofi', 'mood': 'chill', 'energy': 0.3, 'valence': 0.5, 'danceability': 0.5}
Library Rain - Score: 4.86
Because: genre match (+2.0), mood match (+1.0), energy closeness (+0.95), valence closeness (+0.45), danceability closeness (+0.46)

Rainy Window - Score: 4.83
Because: genre match (+2.0), mood match (+1.0), energy closeness (+0.9), valence closeness (+0.47), danceability closeness (+0.45)

Midnight Coding - Score: 4.79
Because: genre match (+2.0), mood match (+1.0), energy closeness (+0.88), valence closeness (+0.47), danceability closeness (+0.44)

Focus Flow - Score: 3.81
Because: genre match (+2.0), energy closeness (+0.9), valence closeness (+0.46), danceability closeness (+0.45)

Spacewalk Thoughts - Score: 2.86
Because: mood match (+1.0), energy closeness (+0.98), valence closeness (+0.42), danceability closeness (+0.45)


=== Deep Intense Rock ===
Profile: {'genre': 'rock', 'mood': 'intense', 'energy': 0.9, 'valence': 0.4, 'danceability': 0.5}
Iron Horizon - Score: 4.88
Because: genre match (+2.0), mood match (+1.0), energy closeness (+0.95), valence closeness (+0.47), danceability closeness (+0.45)

Storm Runner - Score: 4.87
Because: genre match (+2.0), mood match (+1.0), energy closeness (+0.99), valence closeness (+0.46), danceability closeness (+0.42)

Gym Hero - Score: 2.60
Because: mood match (+1.0), energy closeness (+0.97), valence closeness (+0.32), danceability closeness (+0.31)

Solar Flare - Score: 1.70
Because: energy closeness (+1.0), valence closeness (+0.35), danceability closeness (+0.35)

Night Drive Loop - Score: 1.69
Because: energy closeness (+0.85), valence closeness (+0.46), danceability closeness (+0.39)


=== Adversarial - Energetic Sad ===
Profile: {'genre': 'pop', 'mood': 'sad', 'energy': 0.9, 'valence': 0.2, 'danceability': 0.8}
Gym Hero - Score: 3.65
Because: genre match (+2.0), energy closeness (+0.97), valence closeness (+0.21), danceability closeness (+0.46)

Sunrise City - Score: 3.60
Because: genre match (+2.0), energy closeness (+0.92), valence closeness (+0.18), danceability closeness (+0.49)

Storm Runner - Score: 1.78
Because: energy closeness (+0.99), valence closeness (+0.36), danceability closeness (+0.43)

Solar Flare - Score: 1.75
Because: energy closeness (+1.0), valence closeness (+0.25), danceability closeness (+0.5)

Iron Horizon - Score: 1.73
Because: energy closeness (+0.95), valence closeness (+0.38), danceability closeness (+0.4)

---

## 8. Future Work

I'd add collaborative filtering (recommending based on what similar users liked) to reduce the filter-bubble effect of pure content-based matching. I'd also add a diversity bonus so the same 2-3 songs don't dominate every profile's top results, and I'd try detecting internally contradictory profiles (like "energetic + sad") so the system can either flag the conflict or weight mood more heavily instead of letting genre silently override it.

---

## 9. Personal Reflection

The biggest thing I learned is that a "recommendation" is really just arithmetic on whatever weights you hardcode — when I temporarily doubled the energy weight and halved the genre weight, the rankings shifted noticeably, which made it obvious the system isn't discovering some deeper truth about taste, it's just doing distance math. The most interesting discovery was the adversarial test: asking for "sad" music still returned upbeat pop songs, because the model treats energy, valence, and mood as independent numbers rather than understanding they should agree with each other. This changed how I think about real recommendation apps — even something that "feels" personalized can be a fairly shallow weighted sum underneath, and the weight choices themselves quietly encode whoever built the system's assumptions about what a good recommendation looks like.