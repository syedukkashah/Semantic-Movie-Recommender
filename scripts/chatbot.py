"""
EMOTION-BASED CHATBOT

Main chatbot class that orchestrates the entire recommendation pipeline.
Handles conversation flow and user interactions.
"""

from emotion_state_parser import parse_emotion, get_emotion_message
from recommendation_engine import RecommendationEngine
from typing import Dict, Optional
import os


class EmotionChatbot:
    """Interactive chatbot for emotion-based movie recommendations."""
    
    def __init__(self, ttl_path: str):
        """Initialize chatbot with knowledge base."""
        self.engine = RecommendationEngine(ttl_path)
        self.conversation_history = []
        self.user_context = {
            'last_emotion': None,
            'watched_movies': set(),
            'preferences': {}
        }
    
    def handle_user_input(self, user_message: str) -> Dict:
        """
        Process user input and generate recommendations.
        
        Returns:
        {
            'response': str (conversational response),
            'recommendations': List[Dict] (movie recommendations),
            'reasoning': str (explanation),
            'emotion_state': Dict (parsed emotion)
        }
        """
        
        # Parse emotion from input
        emotion_state = parse_emotion(user_message)
        
        # Store in history
        self.conversation_history.append({
            'message': user_message,
            'emotion_state': emotion_state
        })
        
        # Acknowledge user's emotion
        acknowledgment = get_emotion_message(emotion_state)
        
        # Generate recommendations based on query type
        recommendations = self._get_recommendations(emotion_state)
        
        # Format response
        response = self._format_response(acknowledgment, recommendations, emotion_state)
        
        return {
            'response': response,
            'recommendations': recommendations,
            'emotion_state': emotion_state,
            'acknowledgment': acknowledgment
        }
    
    def _get_recommendations(self, emotion_state: Dict) -> list:
        """Get movie recommendations based on parsed emotion state."""
        
        query_type = emotion_state['query_type']
        emotion = emotion_state['emotion']
        intensity = emotion_state['intensity']
        
        if query_type == 'neutral':
            # Random recommendation
            recommendations = self.engine.recommend_neutral(num_results=10)
            reasoning = "These are highly-rated movies you might enjoy."
        
        elif query_type == 'current_state':
            # Match current emotion
            if emotion:
                recommendations = self.engine.recommend_current_state(
                    emotion, 
                    user_intensity=intensity,
                    num_results=10
                )
                reasoning = f"These movies capture {emotion} like you're feeling."
            else:
                recommendations = self.engine.recommend_neutral(num_results=10)
                reasoning = "Here are some recommended movies for you."
        
        elif query_type == 'desired_state':
            # Match desired emotion
            if emotion:
                recommendations = self.engine.recommend_desired_state(
                    emotion,
                    num_results=10
                )
                reasoning = f"These movies should make you feel {emotion}."
            else:
                recommendations = self.engine.recommend_neutral(num_results=10)
                reasoning = "Here are some uplifting movies."
        
        else:
            # Fallback
            recommendations = self.engine.recommend_neutral(num_results=10)
            reasoning = "Here are some movies I think you'd enjoy."
        
        return recommendations
    
    def _format_response(
        self, 
        acknowledgment: str, 
        recommendations: list,
        emotion_state: Dict
    ) -> str:
        """Format chatbot response with recommendations."""
        
        if not recommendations:
            return acknowledgment + " Sorry, I couldn't find any matching movies."
        
        response = acknowledgment + "\n\n"
        response += "Here are my recommendations:\n\n"
        
        for i, movie in enumerate(recommendations[:5], 1):  # Show top 5
            title = movie['title']
            movie_id = movie.get('movie_id', '?')
            director = movie.get('director', 'Unknown')
            cast = movie.get('cast', [])
            
            # Add emotion info
            details = []
            if 'emotion' in movie:
                details.append(f"emotion: {movie['emotion'].upper()}")
            if 'intensity' in movie:
                intensity = movie['intensity']
                intensity_label = "strong" if intensity > 0.7 else "moderate" if intensity > 0.4 else "subtle"
                details.append(f"intensity: {intensity_label} ({intensity:.2f})")
            if 'confidence' in movie:
                details.append(f"confidence: {movie['confidence']:.2%}")
            
            detail_str = f" [{', '.join(details)}]" if details else ""
            imdb_link = f"(IMDb: tt{movie_id})"
            
            # Format cast list
            cast_str = ", ".join(cast) if cast else "N/A"
            
            response += f"{i}. **{title}** {imdb_link}\n"
            response += f"   Director: {director}\n"
            response += f"   Cast: {cast_str}\n"
            response += f"   {detail_str}\n\n"
        
        if len(recommendations) > 5:
            response += f"... and {len(recommendations) - 5} more recommendations available\n\n"
        
        response += "💡 Tip: You can search for these movies using the IMDb IDs (e.g., search 'tt0042674' on IMDb)\n\n"
        response += "Would you like more details or different recommendations?"
        
        return response
    
    def ask_follow_up(self) -> str:
        """Generate a follow-up question to continue conversation."""
        
        last_emotion = self.conversation_history[-1]['emotion_state']['emotion'] if self.conversation_history else None
        
        if last_emotion == 'sadness':
            return "Would you like something to cheer you up, or do you want more movies like this?"
        elif last_emotion == 'fear':
            return "Want more suspenseful movies, or would you like something to calm down?"
        elif last_emotion == 'anger':
            return "Looking for more intense movies, or something to cool off?"
        else:
            return "Want more recommendations, or would you like to explore a different mood?"
    
    def ask_clarification(self) -> str:
        """Ask user to clarify their emotional state."""
        
        return (
            "I'm not sure what emotion you're describing. "
            "Could you tell me:\n"
            "- How you're feeling right now?\n"
            "- What mood you want to be in?\n"
            "- Or I can just surprise you with a random recommendation!"
        )
    
    def reset_conversation(self):
        """Reset conversation history."""
        self.conversation_history = []
        self.user_context = {
            'last_emotion': None,
            'watched_movies': set(),
            'preferences': {}
        }


# ===== INTERACTIVE CHAT LOOP =====
def run_chatbot_interactive(ttl_path: str):
    """Run interactive chatbot session."""
    
    chatbot = EmotionChatbot(ttl_path)
    
    print("=" * 60)
    print("🎬 EMOTION-BASED MOVIE RECOMMENDATION CHATBOT 🎬")
    print("=" * 60)
    print("\nHi! I'm here to recommend movies based on your emotions.")
    print("Tell me how you're feeling or what mood you want to be in!")
    print("(Type 'quit' to exit, 'reset' to start over)\n")
    
    while True:
        user_input = input("You: ").strip()
        
        if not user_input:
            continue
        
        if user_input.lower() == 'quit':
            print("\nThanks for chatting! Enjoy your movie! 🍿")
            break
        
        if user_input.lower() == 'reset':
            chatbot.reset_conversation()
            print("\nConversation reset. Start fresh!\n")
            continue
        
        # Get recommendation
        result = chatbot.handle_user_input(user_input)
        
        # Display response
        print(f"\nChatbot: {result['response']}\n")


# ===== TEST =====
if __name__ == "__main__":
    ttl_path = os.path.join(os.path.dirname(__file__), "..", "movie-emotions.ttl")
    
    if os.path.exists(ttl_path):
        # Run interactive session
        run_chatbot_interactive(ttl_path)
    else:
        print(f"❌ TTL file not found at {ttl_path}")
        print(f"Expected: {ttl_path}")
