"""
FLASK API SERVER

REST API wrapper for the RecommendationEngine.
Connects the frontend to the movie recommendation backend.
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from recommendation_engine import RecommendationEngine
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for frontend on localhost:8080

# Initialize recommendation engine with TTL knowledge base
script_dir = os.path.dirname(__file__)
ttl_path = os.path.join(script_dir, "..", "movie-emotions.ttl")

try:
    engine = RecommendationEngine(ttl_path)
    logger.info(f"✓ RecommendationEngine initialized with {ttl_path}")
except Exception as e:
    logger.error(f"✗ Failed to initialize RecommendationEngine: {e}")
    engine = None


# ===== HEALTH CHECK =====
@app.route("/api/health", methods=["GET"])
def health():
    """Health check endpoint."""
    return jsonify({
        "status": "ok",
        "message": "Movie Recommender API is running"
    }), 200


# ===== EMOTIONS LIST =====
@app.route("/api/emotions", methods=["GET"])
def get_emotions():
    """Return list of supported emotions."""
    if not engine:
        return jsonify({"error": "Engine not initialized"}), 500
    
    return jsonify({
        "emotions": engine.emotion_list
    }), 200


# ===== MAIN RECOMMENDATION ENDPOINT =====
@app.route("/api/recommend", methods=["POST"])
def get_recommendations():
    """
    Get movie recommendations based on user emotion and intensity.
    
    Request body:
    {
        "emotion": "joy",
        "intensity": 0.8,
        "count": 10 (optional, default 10)
    }
    
    Response:
    {
        "success": true,
        "recommendations": [
            {
                "movie_id": "0040497",
                "title": "Battleship Potemkin",
                "director": "Sergei Eisenstein",
                "cast": ["Actor1", "Actor2"],
                "emotion": "joy",
                "intensity": 0.85,
                "confidence": 0.92,
                "score": 0.89
            },
            ...
        ]
    }
    """
    try:
        data = request.get_json()
        
        # Validate input
        if not data:
            return jsonify({"error": "Request body required"}), 400
        
        emotion = data.get("emotion", "").lower()
        intensity = data.get("intensity", 0.5)
        count = data.get("count", 10)
        
        # Validate emotion
        if not emotion or emotion not in engine.emotion_list:
            return jsonify({
                "error": f"Invalid emotion. Supported emotions: {', '.join(engine.emotion_list)}"
            }), 400
        
        # Validate intensity
        try:
            intensity = float(intensity)
            if not (0.0 <= intensity <= 1.0):
                return jsonify({"error": "Intensity must be between 0.0 and 1.0"}), 400
        except (ValueError, TypeError):
            return jsonify({"error": "Intensity must be a number"}), 400
        
        # Validate count
        try:
            count = int(count)
            if count < 1 or count > 50:
                count = 10
        except (ValueError, TypeError):
            count = 10
        
        # Get recommendations
        recommendations = engine.recommend_current_state(
            user_emotion=emotion,
            user_intensity=intensity,
            num_results=count
        )
        
        # Format response
        response = {
            "success": True,
            "emotion": emotion,
            "intensity": intensity,
            "count": len(recommendations),
            "recommendations": recommendations
        }
        
        return jsonify(response), 200
        
    except Exception as e:
        logger.error(f"Error in /api/recommend: {e}")
        return jsonify({"error": str(e)}), 500


# ===== EMOTION JOURNEY ENDPOINT =====
@app.route("/api/journey", methods=["POST"])
def get_emotion_journey():
    """
    Get a sequence of movies for mood progression.
    
    Request body:
    {
        "startEmotion": "sadness",
        "endEmotion": "joy",
        "count": 5 (optional)
    }
    
    Response:
    {
        "success": true,
        "journey": [movie1, movie2, ...]
    }
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "Request body required"}), 400
        
        start_emotion = data.get("startEmotion", "").lower()
        end_emotion = data.get("endEmotion", "").lower()
        count = data.get("count", 5)
        
        # Validate emotions
        if start_emotion not in engine.emotion_list or end_emotion not in engine.emotion_list:
            return jsonify({
                "error": f"Invalid emotion. Supported: {', '.join(engine.emotion_list)}"
            }), 400
        
        # Get journey
        journey = engine.recommend_emotion_journey(
            start_emotion=start_emotion,
            end_emotion=end_emotion,
            num_results=count
        )
        
        response = {
            "success": True,
            "startEmotion": start_emotion,
            "endEmotion": end_emotion,
            "count": len(journey),
            "journey": journey
        }
        
        return jsonify(response), 200
        
    except Exception as e:
        logger.error(f"Error in /api/journey: {e}")
        return jsonify({"error": str(e)}), 500


# ===== NEUTRAL/POPULAR MOVIES ENDPOINT =====
@app.route("/api/popular", methods=["GET"])
def get_popular_movies():
    """
    Get top-rated/popular movies (no emotion filter).
    
    Query params:
    - count: number of movies (default 10, max 50)
    
    Response:
    {
        "success": true,
        "recommendations": [movie1, movie2, ...]
    }
    """
    try:
        count = request.args.get("count", 10, type=int)
        
        if count < 1 or count > 50:
            count = 10
        
        recommendations = engine.recommend_neutral(num_results=count)
        
        response = {
            "success": True,
            "count": len(recommendations),
            "recommendations": recommendations
        }
        
        return jsonify(response), 200
        
    except Exception as e:
        logger.error(f"Error in /api/popular: {e}")
        return jsonify({"error": str(e)}), 500


# ===== ERROR HANDLERS =====
@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return jsonify({"error": "Endpoint not found"}), 404


@app.errorhandler(500)
def server_error(error):
    """Handle 500 errors."""
    return jsonify({"error": "Internal server error"}), 500


# ===== MAIN =====
if __name__ == "__main__":
    if not engine:
        print("❌ Cannot start server: RecommendationEngine failed to initialize")
        exit(1)
    
    print("\n" + "="*60)
    print("🎬 MOVIE RECOMMENDER API SERVER")
    print("="*60)
    print(f"✓ Backend: {ttl_path}")
    print(f"✓ Emotions: {', '.join(engine.emotion_list)}")
    print("\n📍 Starting server on http://localhost:5000")
    print("\nAvailable endpoints:")
    print("  GET  /api/health          - Health check")
    print("  GET  /api/emotions        - List supported emotions")
    print("  POST /api/recommend       - Get recommendations by emotion/intensity")
    print("  POST /api/journey         - Get emotion progression journey")
    print("  GET  /api/popular         - Get popular movies")
    print("\nFrontend: http://localhost:8080")
    print("="*60 + "\n")
    
    app.run(debug=True, host="0.0.0.0", port=5000)
