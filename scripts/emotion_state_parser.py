"""
EMOTION STATE PARSER

Converts user natural language input into structured emotion states.
Maps user emotions to NRC emotion categories (joy, sadness, fear, anger, disgust, surprise, trust).
"""

import re
from typing import Dict, List, Optional, Tuple


# ===== EMOTION LEXICON =====
EMOTION_KEYWORDS = {
    "joy": [
        "happy", "joy", "joyful", "cheerful", "glad", "delighted", "pleased",
        "excited", "thrilled", "wonderful", "amazing", "awesome", "fantastic",
        "great", "uplifted", "grateful", "content", "satisfied", "fun"
    ],
    "sadness": [
        "sad", "sadness", "depressed", "depression", "miserable", "unhappy",
        "lonely", "alone", "gloomy", "melancholy", "down", "blue", "grief",
        "heartbreak", "disappointed", "upset", "crying", "tears", "tragic"
    ],
    "fear": [
        "scared", "fear", "afraid", "frightened", "terrified", "anxious",
        "nervous", "worried", "panic", "dread", "horror", "creepy", "eerie",
        "tension", "suspense", "scary", "dangerous", "threat"
    ],
    "anger": [
        "angry", "anger", "furious", "mad", "rage", "hostile", "irritated",
        "annoyed", "aggravated", "outraged", "violent", "intense", "heated",
        "conflict", "aggressive", "bitter", "resentful"
    ],
    "disgust": [
        "disgusted", "disgust", "gross", "revolting", "repulsive", "vile",
        "nasty", "yucky", "sick", "nausea", "repugnant", "abhorrent", "filthy"
    ],
    "surprise": [
        "surprised", "surprise", "shocked", "astonished", "amazed", "stunned",
        "unexpected", "twist", "revelation", "shocking", "jaw-dropping",
        "unpredictable", "plot twist", "incredible"
    ],
    "trust": [
        "trust", "faith", "confident", "assured", "reliable", "faithful",
        "loyal", "inspire", "positive", "hopeful", "belief", "strength",
        "courage", "determined", "brave", "confident"
    ]
}

# Inverse mapping for quick lookup
EMOTION_MAP = {}
for emotion, keywords in EMOTION_KEYWORDS.items():
    for keyword in keywords:
        EMOTION_MAP[keyword.lower()] = emotion


# ===== QUERY TYPE DETECTION =====
CURRENT_STATE_MARKERS = [
    "i feel", "i'm feeling", "i am feeling", "feeling", "i'm", "i am",
    "currently", "right now", "at the moment", "how i feel"
]

DESIRED_STATE_MARKERS = [
    "i want to feel", "want to feel", "like to feel", "make me feel",
    "should feel", "want", "like", "need", "looking for",
    "in the mood for", "want something", "recommend"
]

NEUTRAL_MARKERS = [
    "surprise me", "random", "surprise", "anything", "doesn't matter",
    "i don't care", "whatever", "pick", "choose", "suggest"
]


def parse_emotion(text: str) -> Dict:
    """
    Parse user input and extract emotion information.
    
    Returns:
    {
        'emotion': str (emotion name or None),
        'intensity': float (0.0-1.0),
        'query_type': str ('current_state', 'desired_state', 'neutral'),
        'secondary_emotions': List[str],
        'confidence': float (0.0-1.0),
        'raw_text': str
    }
    """
    text_lower = text.lower().strip()
    
    # Detect query type
    query_type = detect_query_type(text_lower)
    
    # Extract emotions
    emotions_found = extract_emotions(text_lower)
    
    if not emotions_found:
        return {
            'emotion': None,
            'intensity': 0.0,
            'query_type': query_type,
            'secondary_emotions': [],
            'confidence': 0.0,
            'raw_text': text
        }
    
    # Sort by frequency (primary emotion = most frequent)
    primary_emotion = emotions_found[0][0]
    primary_count = emotions_found[0][1]
    secondary_emotions = [e[0] for e in emotions_found[1:]]
    
    # Calculate intensity based on word count and repetition
    intensity = min(1.0, primary_count / 3.0)  # Max at 3+ occurrences
    
    # Calculate confidence
    confidence = min(1.0, primary_count / 2.0)  # Higher if emotion mentioned multiple times
    confidence = min(1.0, confidence + 0.5)  # Base confidence of 0.5
    
    return {
        'emotion': primary_emotion,
        'intensity': intensity,
        'query_type': query_type,
        'secondary_emotions': secondary_emotions,
        'confidence': confidence,
        'raw_text': text
    }


def detect_query_type(text: str) -> str:
    """
    Detect whether user is asking about current state, desired state, or neutral recommendation.
    """
    # Check for neutral/random first
    for marker in NEUTRAL_MARKERS:
        if marker in text:
            return 'neutral'
    
    # Check for desired state
    for marker in DESIRED_STATE_MARKERS:
        if marker in text:
            return 'desired_state'
    
    # Check for current state
    for marker in CURRENT_STATE_MARKERS:
        if marker in text:
            return 'current_state'
    
    # Default to current state if contains emotion keywords
    if any(emotion_word in text for emotion_word in EMOTION_MAP.keys()):
        return 'current_state'
    
    # Otherwise neutral
    return 'neutral'


def extract_emotions(text: str) -> List[Tuple[str, int]]:
    """
    Extract emotion keywords from text and return sorted by frequency.
    
    Returns: List of (emotion_name, count) tuples sorted by count descending
    """
    emotion_counts = {}
    
    # Find all emotion keywords
    words = re.findall(r'\b\w+\b', text)
    for word in words:
        word_lower = word.lower()
        if word_lower in EMOTION_MAP:
            emotion = EMOTION_MAP[word_lower]
            emotion_counts[emotion] = emotion_counts.get(emotion, 0) + 1
    
    # Sort by count descending
    sorted_emotions = sorted(emotion_counts.items(), key=lambda x: x[1], reverse=True)
    return sorted_emotions


def get_emotion_message(state: Dict) -> str:
    """
    Generate a conversational message based on parsed emotion state.
    """
    if state['query_type'] == 'neutral':
        return "I'll recommend some highly-rated movies for you!"
    
    emotion = state['emotion']
    if not emotion:
        return "I didn't catch an emotion. Tell me how you're feeling or what you'd like to watch."
    
    intensity = state['intensity']
    intensity_word = "strongly" if intensity > 0.7 else "somewhat" if intensity > 0.4 else "slightly"
    
    if state['query_type'] == 'current_state':
        return f"I understand you're {intensity_word} feeling {emotion}. Let me find movies that match that emotion..."
    else:  # desired_state
        return f"You want to feel {emotion}! Let me find movies that evoke that..."


# ===== TEST =====
if __name__ == "__main__":
    test_inputs = [
        "I feel sad and lonely",
        "I want to feel happy and excited",
        "Surprise me with something interesting",
        "I'm scared right now",
        "Make me laugh, I want joy"
    ]
    
    for text in test_inputs:
        result = parse_emotion(text)
        message = get_emotion_message(result)
        print(f"\nInput: {text}")
        print(f"Parsed: {result}")
        print(f"Message: {message}")
