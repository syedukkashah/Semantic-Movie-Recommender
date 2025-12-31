"""
STEP 2: Emotion Classification (Python)

- Reads raw reviews from reviews.json
- Applies Naïve Bayes emotion classifier
- Aggregates emotions per movie
- Writes emotion_results.json

This script replaces emotion classification previously done in JavaScript.
"""

import json
import os
from emotion_classifier import classify_emotion, aggregate_emotions


# ---------- PATH SETUP ----------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_PATH = os.path.join(BASE_DIR, "..", "reviews.json")
OUTPUT_PATH = os.path.join(BASE_DIR, "..", "emotion_results.json")


# ---------- MAIN PROCESS ----------
def run_emotion_analysis():
    print("📥 Loading reviews.json...")

    if not os.path.exists(INPUT_PATH):
        raise FileNotFoundError("❌ reviews.json not found. Run pipeline.js first.")

    with open(INPUT_PATH, "r", encoding="utf-8") as f:
        movies = json.load(f)

    print(f"✅ Loaded {len(movies)} movies\n")

    final_results = []

    for movie in movies:
        movie_id = movie["movieId"]
        title = movie["title"]
        reviews = movie["reviews"]

        print(f"🎬 Processing: {title}")

        # ---- Classify each review ----
        classification_results = []
        for review in reviews:
            result = classify_emotion(review)
            classification_results.append(result)

        # ---- Aggregate emotions ----
        aggregation = aggregate_emotions(classification_results)

        print(f"   ➤ Dominant emotion: {aggregation['aggregatedEmotion'].upper()}")
        print(f"   ➤ Vote %: {aggregation['votePercentage']}%")
        print(f"   ➤ Avg intensity: {aggregation['averageIntensity']}")
        print(f"   ➤ Avg confidence: {aggregation['averageConfidence']}\n")

        final_results.append({
            "movieId": movie_id,
            "title": title,
            "aggregation": aggregation,
            "classifications": classification_results
        })

    # ---------- WRITE OUTPUT ----------
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(final_results, f, indent=2)

    print(f"✅ Emotion analysis complete!")
    print(f"📄 Results written to: {OUTPUT_PATH}")


# ---------- ENTRY POINT ----------
if __name__ == "__main__":
    run_emotion_analysis()
