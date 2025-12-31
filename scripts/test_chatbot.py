#!/usr/bin/env python
"""Quick test of the recommendation engine"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from emotion_state_parser import parse_emotion, get_emotion_message
from recommendation_engine import RecommendationEngine

ttl_path = os.path.join(os.path.dirname(__file__), "..", "movie-emotions.ttl")

print("[OK] Testing Emotion-Based Movie Recommendation Chatbot\n")

# Test 1: Emotion parsing
print("=== TEST 1: Emotion Parsing ===")
test_input = "I feel sad and lonely right now"
emotion_state = parse_emotion(test_input)
print(f"Input: {test_input}")
print(f"Emotion: {emotion_state['emotion']}")
print(f"Intensity: {emotion_state['intensity']:.2f}")
print(f"Query Type: {emotion_state['query_type']}")
print(f"Message: {get_emotion_message(emotion_state)}\n")

# Test 2: Recommendation Engine
print("=== TEST 2: Recommendation Engine ===")
try:
    engine = RecommendationEngine(ttl_path)
    print("[OK] Engine initialized\n")
    
    # Get recommendations for joy
    print("Getting joy recommendations...")
    recommendations = engine.recommend_current_state("joy", num_results=3)
    
    if recommendations:
        print(f"Found {len(recommendations)} recommendations:")
        for i, r in enumerate(recommendations, 1):
            print(f"  {i}. {r['title']} (intensity: {r.get('intensity', 'N/A')})")
    else:
        print("No recommendations found")
        
except Exception as e:
    print(f"[ERROR] {e}")
    import traceback
    traceback.print_exc()

print("\n[OK] Tests completed")
