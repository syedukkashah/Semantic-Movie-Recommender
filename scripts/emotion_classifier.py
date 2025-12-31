import json
import math
from collections import defaultdict
from sklearn.metrics import accuracy_score, classification_report

# ===============================
# Emotion Lexicon (NRC-style)
# ===============================
emotion_lexicon = {
    "joy": [
        "excellent","wonderful","masterpiece","amazing","love","great",
        "fantastic","brilliant","perfect","beautiful","delightful",
        "gorgeous","impressive","funny","hilarious","entertaining",
        "enjoyable","pleasant","happy","cheerful","triumph","victory","success"
    ],
    "sadness": [
        "sad","depressing","tragic","sorrowful","melancholy","heartbreak",
        "tears","suffer","pain","loss","grief","disappointing",
        "disappointed","boring","dull","tedious","awful","terrible",
        "worst","hate","hated","dislike"
    ],
    "fear": [
        "scary","terrifying","horror","frightening","horrific","dreadful",
        "ominous","suspense","tense","unsettling","disturbing","creepy",
        "eerie","sinister","evil","menace"
    ],
    "anger": [
        "angry","rage","furious","outraged","infuriating","annoying",
        "irritating","frustrating","despicable","insulting","offensive",
        "ridiculous","disgusting","vile","repugnant","abhorrent"
    ],
    "disgust": [
        "disgusting","repulsive","vile","filthy","gross","revolting",
        "nauseating","abominable","loathsome","repugnant",
        "despicable","detestable"
    ],
    "surprise": [
        "surprising","unexpected","astonishing","astounding","shocking",
        "amazing","incredible","remarkable","startling",
        "stunning","bewildering","confounding"
    ],
    "trust": [
        "reliable","trustworthy","credible","dependable","solid","strong",
        "confident","assured","capable","competent","skilled",
        "professional","authentic","genuine","honest"
    ]
}

EMOTIONS = list(emotion_lexicon.keys())

# ===============================
# Naïve Bayes Setup
# ===============================
priors = {e: 1 / len(EMOTIONS) for e in EMOTIONS}

vocab = set(word for words in emotion_lexicon.values() for word in words)
VOCAB_SIZE = len(vocab)

likelihoods = {}
for emotion, words in emotion_lexicon.items():
    likelihoods[emotion] = {}
    total_words = len(words)
    for word in vocab:
        count = 1 if word in words else 0
        likelihoods[emotion][word] = (count + 1) / (total_words + VOCAB_SIZE)

# ===============================
# Emotion Classification
# ===============================
def classify_emotion(text):
    words = text.lower().split()
    log_scores = {}
    emotion_word_counts = defaultdict(int)

    for emotion in EMOTIONS:
        log_prob = math.log(priors[emotion])
        for word in words:
            if word in vocab:
                log_prob += math.log(likelihoods[emotion][word])
                if word in emotion_lexicon[emotion]:
                    emotion_word_counts[emotion] += 1
        log_scores[emotion] = log_prob

    dominant_emotion = max(log_scores, key=log_scores.get)

    max_log = max(log_scores.values())
    exp_scores = {e: math.exp(v - max_log) for e, v in log_scores.items()}
    total = sum(exp_scores.values())
    probabilities = {e: exp_scores[e] / total for e in exp_scores}

    sorted_probs = sorted(probabilities.values(), reverse=True)
    confidence = 0.9 if sorted_probs[0] - sorted_probs[1] > 0.1 else 0.7
    intensity = min(probabilities[dominant_emotion] * 2, 1.0)

    return {
        "dominantEmotion": dominant_emotion,
        "probabilities": probabilities,
        "emotionWordCounts": dict(emotion_word_counts),
        "intensity": round(intensity, 2),
        "confidence": round(confidence, 2)
    }

# ===============================
# Aggregate emotions per movie
# ===============================
def aggregate_emotions(classifications):
    votes = defaultdict(int)
    intensity_sum = 0
    confidence_sum = 0

    for c in classifications:
        for e, count in c["emotionWordCounts"].items():
            votes[e] += count
        intensity_sum += c["intensity"]
        confidence_sum += c["confidence"]

    aggregated = max(votes, key=votes.get) if votes else "neutral"

    return {
        "aggregatedEmotion": aggregated,
        "allVotes": dict(votes),
        "averageIntensity": round(intensity_sum / len(classifications), 2),
        "averageConfidence": round(confidence_sum / len(classifications), 2)
    }

# ===============================
# ACCURACY EVALUATION (CONTROLLED)
# ===============================
def evaluate_accuracy():
    print("\n📊 Running accuracy evaluation...\n")

    test_data = [
        ("I loved this amazing movie", "joy"),
        ("The movie was boring and dull", "sadness"),
        ("A terrifying horror experience", "fear"),
        ("Disgusting and vile scenes", "disgust"),
        ("Funny and entertaining film", "joy"),
        ("Angry and frustrating experience", "anger"),
    ]

    y_true, y_pred = [], []

    for text, label in test_data:
        prediction = classify_emotion(text)["dominantEmotion"]
        y_true.append(label)
        y_pred.append(prediction)

    print("Accuracy:", accuracy_score(y_true, y_pred))
    print("\nClassification Report:\n")
    print(classification_report(y_true, y_pred))

# ===============================
# MAIN PIPELINE
# ===============================
def main():
    with open("reviews.json", "r", encoding="utf-8") as f:
        movies = json.load(f)

    output = []

    for movie in movies:
        print(f"🎬 Processing: {movie['title']}")

        classifications = [
            classify_emotion(review)
            for review in movie["reviews"]
        ]

        aggregation = aggregate_emotions(classifications)

        output.append({
            "movieId": movie["movieId"],
            "title": movie["title"],
            "aggregation": aggregation,
            "reviewsAnalyzed": len(classifications)
        })

    with open("../movie_emotions.json", "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2)

    print("\n✅ Emotion classification complete")
    print("📄 Output written to movie_emotions.json")

    # Run evaluation AFTER pipeline
    evaluate_accuracy()

if __name__ == "__main__":
    main()
