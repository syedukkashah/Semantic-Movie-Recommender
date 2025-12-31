"""
STEP 3: Knowledge Base (TTL) Generation

- Reads emotion_results.json
- Converts it into RDF triples
- Writes movie-emotions.ttl
"""

import json
import os
from rdflib import Graph, Namespace, RDF, RDFS, Literal, XSD


# ---------- PATHS ----------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_PATH = os.path.join(BASE_DIR, "..", "emotion_results.json")
OUTPUT_PATH = os.path.join(BASE_DIR, "..", "movie-emotions.ttl")


# ---------- NAMESPACES ----------
ONYX = Namespace("http://www.gsi.dit.upm.es/ontologies/onyx/ns#")
MOVIE = Namespace("http://example.org/movie/")
EMOTION = Namespace("http://example.org/emotion/")
EX = Namespace("http://example.org/")


def generate_kb():
    print("📥 Loading emotion_results.json...")

    with open(INPUT_PATH, "r", encoding="utf-8") as f:
        movies = json.load(f)

    g = Graph()

    # Bind prefixes (nice Turtle output)
    g.bind("onyx", ONYX)
    g.bind("movie", MOVIE)
    g.bind("emotion", EMOTION)
    g.bind("ex", EX)

    print(f"🧠 Creating knowledge graph for {len(movies)} movies...\n")

    for movie in movies:
        movie_uri = MOVIE[movie["movieId"]]
        agg = movie["aggregation"]

        # --- Movie entity ---
        g.add((movie_uri, RDF.type, ONYX.Movie))
        g.add((movie_uri, RDFS.label, Literal(movie["title"])))

        # --- Aggregated Emotion ---
        emotion_uri = EMOTION[f"agg_{movie['movieId']}"]
        emotion_category = ONYX[agg["aggregatedEmotion"].capitalize()]

        g.add((emotion_uri, RDF.type, ONYX.AggregatedEmotion))
        g.add((emotion_uri, ONYX.hasEmotionCategory, emotion_category))
        g.add((emotion_uri, ONYX.hasEmotionIntensity,
               Literal(agg["averageIntensity"], datatype=XSD.float)))
        g.add((emotion_uri, ONYX.algorithmConfidence,
               Literal(agg["averageConfidence"], datatype=XSD.float)))

        # Link movie → emotion
        g.add((movie_uri, ONYX.hasEmotion, emotion_uri))

        print(f"✅ Added KB entries for: {movie['title']}")

    # ---------- WRITE TTL ----------
    g.serialize(destination=OUTPUT_PATH, format="turtle")
    print(f"\n📄 Knowledge Base written to: {OUTPUT_PATH}")


if __name__ == "__main__":
    generate_kb()
