"""
RECOMMENDATION ENGINE

Core logic that orchestrates emotion parsing, SPARQL queries, and movie ranking.
Provides recommendations based on user emotional state.
"""

from sparql_recommender import SPARQLRecommender
from typing import List, Dict, Optional
import os


class RecommendationEngine:
    """Orchestrate movie recommendations based on user emotions."""
    
    def __init__(self, ttl_path: str):
        """Initialize with TTL knowledge base path."""
        self.recommender = SPARQLRecommender(ttl_path)
        self.emotion_list = ["joy", "sadness", "fear", "anger", "disgust", "surprise", "trust"]
    
    def recommend_current_state(
        self,
        user_emotion: str,
        user_intensity: float = 0.5,
        num_results: int = 10
    ) -> List[Dict]:
        """
        User feels X emotion → recommend movies that evoke the same emotion.
        
        Best for: "I feel sad" → find sad movies
        """
        if user_emotion.lower() not in self.emotion_list:
            return []
        
        movies = self.recommender.get_movies_by_emotion(
            emotion=user_emotion.lower(),
            intensity_threshold=0.0,
            limit=num_results * 3  # Get extra to rank and deduplicate
        )
        
        # Filter out "movie reviews" and invalid titles
        filtered_movies = [
            m for m in movies 
            if m['title'] and 'movie reviews' not in m['title'].lower()
        ]
        
        # Deduplicate by movie_id while preserving order
        seen = set()
        unique_movies = []
        for movie in filtered_movies:
            if movie['movie_id'] not in seen:
                unique_movies.append(movie)
                seen.add(movie['movie_id'])
        
        # Score by similarity to user intensity
        scored_movies = self._score_by_intensity_match(unique_movies, user_intensity)
        
        return scored_movies[:num_results]
    
    def recommend_desired_state(
        self,
        desired_emotion: str,
        current_emotion: Optional[str] = None,
        num_results: int = 10
    ) -> List[Dict]:
        """
        User wants to feel Y emotion → recommend movies that evoke it.
        
        Best for: "I want to feel happy" → find uplifting movies
        """
        if desired_emotion.lower() not in self.emotion_list:
            return []
        
        movies = self.recommender.get_movies_by_emotion(
            emotion=desired_emotion.lower(),
            intensity_threshold=0.0,
            limit=num_results * 3
        )
        
        # Filter out "movie reviews" and invalid titles
        filtered_movies = [
            m for m in movies 
            if m['title'] and 'movie reviews' not in m['title'].lower()
        ]
        
        # Deduplicate by movie_id
        seen = set()
        unique_movies = []
        for movie in filtered_movies:
            if movie['movie_id'] not in seen:
                unique_movies.append(movie)
                seen.add(movie['movie_id'])
        
        # Prefer high intensity if going for emotional boost
        scored_movies = self._score_by_intensity_match(unique_movies, intensity=0.8)
        
        return scored_movies[:num_results]
    
    def recommend_neutral(self, num_results: int = 10) -> List[Dict]:
        """
        Random recommendation → suggest popular movies.
        
        Best for: "Surprise me" → get top-rated movies
        """
        movies = self.recommender.get_top_movies_overall(limit=num_results)
        return movies
    
    def recommend_emotion_journey(
        self,
        start_emotion: str,
        end_emotion: str,
        num_results: int = 5
    ) -> List[Dict]:
        """
        Recommend movies that transition mood from start to end emotion.
        
        Example: sad → happy (comfort movies that lift mood)
        Returns a sequence of movies for mood progression.
        """
        if start_emotion.lower() not in self.emotion_list or end_emotion.lower() not in self.emotion_list:
            return []
        
        # Get movies for both emotions
        start_movies = self.recommender.get_movies_by_emotion(start_emotion.lower(), limit=num_results * 2)
        end_movies = self.recommender.get_movies_by_emotion(end_emotion.lower(), limit=num_results * 2)
        
        # Filter and deduplicate
        all_movies = start_movies + end_movies
        filtered_movies = [
            m for m in all_movies 
            if m['title'] and 'movie reviews' not in m['title'].lower()
        ]
        
        seen = set()
        unique_movies = []
        for movie in filtered_movies:
            if movie['movie_id'] not in seen:
                unique_movies.append(movie)
                seen.add(movie['movie_id'])
        
        # Combine and score by transition potential
        journey = []
        
        # Start with a few validating (same emotion as current state)
        for movie in unique_movies:
            if movie['emotion'] == start_emotion.lower() and len(journey) < 2:
                journey.append(movie)
        
        # Add transition movies (high confidence from both)
        for movie in unique_movies:
            if movie['emotion'] == end_emotion.lower() and len(journey) < num_results:
                journey.append(movie)
        
        return journey[:num_results]
    
    def _score_by_intensity_match(
        self,
        movies: List[Dict],
        intensity: float
    ) -> List[Dict]:
        """
        Score movies by how well they match the desired intensity.
        High intensity → prefer intense movies
        Low intensity → prefer subtle movies
        """
        for movie in movies:
            movie_intensity = movie['intensity']
            
            # Distance from target intensity (0 = perfect match)
            distance = abs(movie_intensity - intensity)
            
            # Score: closer to intensity = higher score
            intensity_score = 1.0 - distance
            
            # Combine with confidence
            movie['score'] = (intensity_score * 0.6) + (movie['confidence'] * 0.4)
        
        # Sort by score
        movies.sort(key=lambda m: m['score'], reverse=True)
        
        return movies
    
    def get_recommendation_reasoning(self, movie: Dict, reason: str) -> str:
        """Generate human-readable explanation for recommendation."""
        
        return f"**{movie['title']}** - {reason}"
    
    def format_recommendations(
        self,
        movies: List[Dict],
        reasoning: List[str] = None
    ) -> str:
        """
        Format movie recommendations as readable output.
        """
        if not movies:
            return "Sorry, I couldn't find any movies matching that emotion."
        
        output = []
        for i, movie in enumerate(movies, 1):
            reason = reasoning[i-1] if reasoning and i-1 < len(reasoning) else ""
            
            title = movie['title']
            
            # Add emotion info if available
            extra_info = ""
            if 'emotion' in movie:
                extra_info += f" ({movie['emotion']})"
            if 'intensity' in movie:
                intensity = movie['intensity']
                intensity_label = "strong" if intensity > 0.7 else "moderate" if intensity > 0.4 else "subtle"
                extra_info += f" - {intensity_label} intensity"
            
            line = f"{i}. {title}{extra_info}"
            if reason:
                line += f" - {reason}"
            
            output.append(line)
        
        return "\n".join(output)


# ===== TEST =====
if __name__ == "__main__":
    # Find TTL file
    ttl_path = os.path.join(os.path.dirname(__file__), "..", "movie-emotions.ttl")
    
    if os.path.exists(ttl_path):
        engine = RecommendationEngine(ttl_path)
        
        print("\n=== TEST 1: Current Emotional State (Joy) ===")
        recommendations = engine.recommend_current_state("joy", user_intensity=0.8, num_results=5)
        print(engine.format_recommendations(recommendations))
        
        print("\n=== TEST 2: Desired Emotional State (Happy) ===")
        recommendations = engine.recommend_desired_state("joy", num_results=5)
        print(engine.format_recommendations(recommendations))
        
        print("\n=== TEST 3: Neutral / Random Recommendation ===")
        recommendations = engine.recommend_neutral(num_results=5)
        print(engine.format_recommendations(recommendations))
        
        print("\n=== TEST 4: Emotion Journey (Sad → Happy) ===")
        recommendations = engine.recommend_emotion_journey("sadness", "joy", num_results=5)
        print(engine.format_recommendations(recommendations))
    else:
        print(f"❌ TTL file not found at {ttl_path}")
