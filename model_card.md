# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

Give your model a short, descriptive name.  
Example: **VibeFinder 1.0**  

---

## 2. Intended Use  

Describe what your recommender is designed to do and who it is for. 

Prompts:  

- What kind of recommendations does it generate  
- What assumptions does it make about the user  
- Is this for real users or classroom exploration  

---

## 3. How the Model Works  

Explain your scoring approach in simple language.  

Prompts:  

- What features of each song are used (genre, energy, mood, etc.)  
- What user preferences are considered  
- How does the model turn those into a score  
- What changes did you make from the starter logic  

Avoid code here. Pretend you are explaining the idea to a friend who does not program.

---

## 4. Data  

Describe the dataset the model uses.  

Prompts:  

- How many songs are in the catalog  
- What genres or moods are represented  
- Did you add or remove data  
- Are there parts of musical taste missing in the dataset  

---

## 5. Strengths  

Where does your system seem to work well  

Prompts:  

- User types for which it gives reasonable results  
- Any patterns you think your scoring captures correctly  
- Cases where the recommendations matched your intuition  

---

## 6. Limitations and Bias 

## Limitations and Bias

This system over-prioritizes genre matches because they're worth +2.0, double a mood match — so a strong genre match can outrank a song that's actually a much better overall vibe fit. With only 18 songs and just 3-4 pop tracks, "pop" profiles keep recommending the same 2 songs (Gym Hero, Sunrise City) regardless of mood or valence targets, since the genre bonus alone puts them near the top. The adversarial test made this concrete: a user wanting "sad" music still got upbeat pop recommended, because the scoring function has no way to recognize that high energy + low valence + sad mood is an internally consistent request — it just sums independent closeness scores.
---

## 7. Evaluation  

## Evaluation

I tested 4 profiles: High-Energy Pop, Chill Lofi, Deep Intense Rock, and an adversarial Energetic-Sad profile.

- **High-Energy Pop vs Chill Lofi:** Pop profile surfaces upbeat, danceable tracks (Sunrise City, Gym Hero); lofi profile shifts entirely to low-energy, high-acousticness tracks (Rainy Window, Library Rain) — makes sense since target_energy is nearly opposite (0.9 vs 0.3).
- **Deep Intense Rock vs High-Energy Pop:** Both want high energy, but rock's low target_valence (0.4) correctly favors moodier/angrier tracks like Iron Horizon and Storm Runner instead of upbeat pop.
- **Adversarial - Energetic Sad:** This profile exposed a limitation — the system recommended high-energy pop songs that aren't actually "sad" in any real sense, because it scores energy and mood independently rather than checking if the combination makes musical sense.

ecause: energy closeness (+0.85), valence closeness (+0.46), danceability closeness (+0.39)
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

Ideas for how you would improve the model next.  

Prompts:  

- Additional features or preferences  
- Better ways to explain recommendations  
- Improving diversity among the top results  
- Handling more complex user tastes  

---

## 9. Personal Reflection  

A few sentences about your experience.  

Prompts:  

- What you learned about recommender systems  
- Something unexpected or interesting you discovered  
- How this changed the way you think about music recommendation apps  
