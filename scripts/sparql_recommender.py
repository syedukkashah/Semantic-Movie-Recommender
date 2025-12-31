"""
SPARQL RECOMMENDER

Builds and executes SPARQL queries against the RDF knowledge base.
Queries movies by emotion categories with configurable filters.
"""

from rdflib import Graph, Namespace, URIRef
from typing import List, Dict, Optional


# ===== NAMESPACES =====
ONYX = Namespace("http://www.gsi.dit.upm.es/ontologies/onyx/ns#")
MOVIE = Namespace("http://example.org/movie/")
EMOTION = Namespace("http://example.org/emotion/")
RDF = Namespace("http://www.w3.org/1999/02/22-rdf-syntax-ns#")
RDFS = Namespace("http://www.w3.org/2000/01/rdf-schema#")
XSD = Namespace("http://www.w3.org/2001/XMLSchema#")


class SPARQLRecommender:
    """Query movie-emotions.ttl using SPARQL."""
    
    def __init__(self, ttl_path: str):
        """Load RDF graph from TTL file."""
        self.graph = Graph()
        self.graph.parse(ttl_path, format="turtle")
        print(f"[OK] Loaded {len(self.graph)} RDF triples from {ttl_path}")
    
    def get_movies_by_emotion(
        self, 
        emotion: str, 
        intensity_threshold: float = 0.0,
        limit: int = 10
    ) -> List[Dict]:
        """
        Find movies with specific emotion category.
        Returns ONLY the primary emotion for each movie (no duplicates).
        
        Args:
            emotion: Emotion category (joy, sadness, fear, anger, disgust, surprise, trust)
            intensity_threshold: Minimum intensity (0.0-1.0)
            limit: Max results
        
        Returns:
            List of movie dicts with {movie_id, title, director, cast, emotion, intensity, confidence, description}
        """
        
        emotion_uri = ONYX[emotion.capitalize()]
        
        query = f"""
        PREFIX onyx: <http://www.gsi.dit.upm.es/ontologies/onyx/ns#>
        PREFIX movie: <http://example.org/movie/>
        PREFIX emotion: <http://example.org/emotion/>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX dbpedia: <http://dbpedia.org/ontology/>
        PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
        
        SELECT ?movieId ?title ?director 
               ?cast0 ?cast1 ?cast2
               ?intensity ?confidence ?description
        WHERE {{
            ?movie a onyx:Movie ;
                rdfs:label ?title ;
                onyx:hasEmotionSet ?emotionSet .
            
            ?emotionSet onyx:hasEmotion ?emotion .
            ?emotion onyx:hasEmotionCategory onyx:{emotion.capitalize()} ;
                     onyx:hasEmotionIntensity ?intensity ;
                     onyx:algorithmConfidence ?confidence .
            
            OPTIONAL {{ ?movie dbpedia:director ?director }}
            OPTIONAL {{ ?movie dbpedia:cast_member_0 ?cast0 }}
            OPTIONAL {{ ?movie dbpedia:cast_member_1 ?cast1 }}
            OPTIONAL {{ ?movie dbpedia:cast_member_2 ?cast2 }}
            OPTIONAL {{ ?movie rdfs:comment ?description }}
            OPTIONAL {{ ?movie dbpedia:abstract ?description }}
            
            BIND(STRAFTER(STR(?movie), "movie/") AS ?movieId)
            
            FILTER (?intensity >= {intensity_threshold})
            FILTER (?title != "User reviews" && ?title != "movie reviews")
        }}
        ORDER BY DESC(?intensity) DESC(?confidence)
        LIMIT {limit}
        """
        
        results = []
        seen_movies = set()
        
        for row in self.graph.query(query):
            movie_id = str(row.movieId)
            
            # Skip if we've already seen this movie (ensures no duplicates)
            if movie_id in seen_movies:
                continue
            
            seen_movies.add(movie_id)
            
            cast = []
            if row.cast0:
                cast.append(str(row.cast0))
            if row.cast1:
                cast.append(str(row.cast1))
            if row.cast2:
                cast.append(str(row.cast2))
            
            description = ""
            if row.description:
                desc_str = str(row.description)
                # Limit description to 150 characters
                description = desc_str[:150] + "..." if len(desc_str) > 150 else desc_str
            
            results.append({
                'movie_id': movie_id,
                'title': str(row.title),
                'director': str(row.director) if row.director else 'Unknown',
                'cast': cast,
                'emotion': emotion,
                'intensity': float(row.intensity),
                'confidence': float(row.confidence),
                'description': description
            })
        
        return results
    
    def get_all_emotions_for_movie(self, movie_id: str) -> Dict:
        """Get all emotions associated with a specific movie."""
        
        query = f"""
        PREFIX onyx: <{str(ONYX)}>
        PREFIX movie: <{str(MOVIE)}>
        PREFIX emotion: <{str(EMOTION)}>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        
        SELECT ?title ?emotionCategory ?intensity ?confidence
        WHERE {{
            movie:{movie_id} a onyx:Movie ;
                rdfs:label ?title ;
                onyx:hasEmotionSet ?emotionSet .
            
            ?emotionSet onyx:hasEmotion ?emotion .
            ?emotion onyx:hasEmotionCategory ?emotionCategory ;
                     onyx:hasEmotionIntensity ?intensity ;
                     onyx:algorithmConfidence ?confidence .
        }}
        """
        
        emotions = []
        title = None
        for row in self.graph.query(query):
            title = str(row.title)
            emotion_name = str(row.emotionCategory).split('#')[-1].lower()
            emotions.append({
                'emotion': emotion_name,
                'intensity': float(row.intensity),
                'confidence': float(row.confidence)
            })
        
        return {
            'movie_id': movie_id,
            'title': title,
            'emotions': emotions
        }
    
    def get_top_movies_overall(self, limit: int = 10) -> List[Dict]:
        """Get highest confidence movies regardless of emotion."""
        
        query = f"""
        PREFIX onyx: <{str(ONYX)}>
        PREFIX movie: <{str(MOVIE)}>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        
        SELECT DISTINCT ?movieId ?title ?confidence
        WHERE {{
            ?movie a onyx:Movie ;
                rdfs:label ?title ;
                onyx:hasEmotionSet ?emotionSet .
            
            ?emotionSet onyx:hasEmotion ?emotion .
            ?emotion onyx:algorithmConfidence ?confidence .
            
            BIND(STRAFTER(STR(?movie), "movie/") AS ?movieId)
        }}
        ORDER BY DESC(?confidence)
        LIMIT {limit}
        """
        
        results = []
        seen = set()
        for row in self.graph.query(query):
            movie_id = str(row.movieId)
            if movie_id not in seen:
                results.append({
                    'movie_id': movie_id,
                    'title': str(row.title),
                    'confidence': float(row.confidence)
                })
                seen.add(movie_id)
        
        return results
    
    def get_all_movies(self) -> List[Dict]:
        """Get all movies in knowledge base."""
        
        query = f"""
        PREFIX onyx: <{str(ONYX)}>
        PREFIX movie: <{str(MOVIE)}>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        
        SELECT DISTINCT ?movieId ?title
        WHERE {{
            ?movie a onyx:Movie ;
                rdfs:label ?title .
            
            BIND(STRAFTER(STR(?movie), "movie/") AS ?movieId)
        }}
        ORDER BY ?movieId
        """
        
        results = []
        for row in self.graph.query(query):
            results.append({
                'movie_id': str(row.movieId),
                'title': str(row.title)
            })
        
        return results


# ===== TEST =====
if __name__ == "__main__":
    import os
    
    # Find TTL file
    ttl_path = os.path.join(os.path.dirname(__file__), "..", "movie-emotions.ttl")
    
    if os.path.exists(ttl_path):
        recommender = SPARQLRecommender(ttl_path)
        
        print("\n🎬 Movies with JOY emotion:")
        joy_movies = recommender.get_movies_by_emotion("joy", limit=5)
        for movie in joy_movies:
            print(f"  {movie['title']} (ID: {movie['movie_id']}) - Intensity: {movie['intensity']:.2f}")
        
        print("\n🎬 All emotions for first movie:")
        if joy_movies:
            movie_id = joy_movies[0]['movie_id']
            all_emotions = recommender.get_all_emotions_for_movie(movie_id)
            print(f"  Movie: {all_emotions['title']}")
            for emotion in all_emotions['emotions']:
                print(f"    - {emotion['emotion']}: {emotion['intensity']:.2f}")
        
        print("\n🎬 Top movies overall:")
        top_movies = recommender.get_top_movies_overall(limit=5)
        for movie in top_movies:
            print(f"  {movie['title']} (Confidence: {movie['confidence']:.2f})")
    else:
        print(f"[ERROR] TTL file not found at {ttl_path}")
