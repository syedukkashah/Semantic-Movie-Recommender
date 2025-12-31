"""
MOVIE DATA ENRICHMENT SCRIPT

Adds real movie titles, directors, and cast to the RDF knowledge base.
Uses local IMDb data or mock data for demonstration.
"""

import os
from rdflib import Graph, Namespace, Literal, URIRef

# Movie database - you can expand this with real IMDb data
MOVIE_DATABASE = {
    '0042674': {
        'title': 'Rope',
        'year': 1948,
        'director': 'Alfred Hitchcock',
        'cast': ['James Stewart', 'John Dall', 'Farley Granger'],
        'emotions': {'Joy': 0.8}
    },
    '0042819': {
        'title': 'Red River',
        'year': 1948,
        'director': 'Howard Hawks',
        'cast': ['John Wayne', 'Montgomery Clift', 'Joanne Dru'],
        'emotions': {'Joy': 0.75}
    },
    '0040497': {
        'title': 'Battleship Potemkin',
        'year': 1925,
        'director': 'Sergei Eisenstein',
        'cast': ['Alexander Antonov', 'Vladimir Barsky', 'Grigori Alexandrov'],
        'emotions': {'Joy': 1.0, 'Trust': 0.9}
    },
    '0041098': {
        'title': 'Ladri di biciclette',
        'year': 1948,
        'director': 'Vittorio De Sica',
        'cast': ['Lamberto Maggiorani', 'Enzo Staiola', 'Lianella Carell'],
        'emotions': {'Joy': 1.0, 'Sadness': 0.85}
    },
    '0043046': {
        'title': 'Singin\' in the Rain',
        'year': 1952,
        'director': 'Gene Kelly, Stanley Donen',
        'cast': ['Gene Kelly', 'Donald O\'Connor', 'Debbie Reynolds'],
        'emotions': {'Joy': 1.0}
    },
    '0043084': {
        'title': 'Vertigo',
        'year': 1958,
        'director': 'Alfred Hitchcock',
        'cast': ['James Stewart', 'Kim Novak', 'Barbara Bel Geddes'],
        'emotions': {'Fear': 0.95, 'Trust': 0.7}
    },
    '0041959': {
        'title': 'Sunset Boulevard',
        'year': 1950,
        'director': 'Billy Wilder',
        'cast': ['William Holden', 'Gloria Swanson', 'Erich von Stroheim'],
        'emotions': {'Sadness': 0.9, 'Disgust': 0.75}
    },
    '0043455': {
        'title': 'The Godfather',
        'year': 1972,
        'director': 'Francis Ford Coppola',
        'cast': ['Marlon Brando', 'Al Pacino', 'James Caan'],
        'emotions': {'Anger': 0.88, 'Trust': 0.92}
    },
    '0042179': {
        'title': 'The Third Man',
        'year': 1949,
        'director': 'Carol Reed',
        'cast': ['Orson Welles', 'Joseph Cotten', 'Alida Valli'],
        'emotions': {'Joy': 0.68, 'Surprise': 0.8}
    },
    '0042192': {
        'title': 'The Asphalt Jungle',
        'year': 1950,
        'director': 'John Huston',
        'cast': ['Sterling Hayden', 'Louis de Funès', 'Jean Hagen'],
        'emotions': {'Joy': 0.68, 'Anger': 0.7}
    },
}

def enrich_movie_data(ttl_path):
    """Add movie metadata to RDF graph."""
    
    # Load existing graph
    graph = Graph()
    graph.parse(ttl_path, format='turtle')
    
    # Define namespaces
    ONYX = Namespace('http://www.gsi.dit.upm.es/ontologies/onyx/ns#')
    MOVIE = Namespace('http://example.org/movie/')
    EMOTION = Namespace('http://example.org/emotion/')
    DBPEDIA = Namespace('http://dbpedia.org/ontology/')
    RDF = Namespace('http://www.w3.org/1999/02/22-rdf-syntax-ns#')
    
    # Add movie metadata
    movie_count = 0
    emotion_count = 0
    
    for movie_id, info in MOVIE_DATABASE.items():
        movie_uri = MOVIE[movie_id]
        
        # Ensure movie has the Movie type
        if (movie_uri, RDF.type, ONYX.Movie) not in graph:
            graph.add((movie_uri, RDF.type, ONYX.Movie))
        # Remove old label
        for o in graph.objects(movie_uri, URIRef('http://www.w3.org/2000/01/rdf-schema#label')):
            graph.remove((movie_uri, URIRef('http://www.w3.org/2000/01/rdf-schema#label'), o))
        
        # Add new title
        graph.add((movie_uri, URIRef('http://www.w3.org/2000/01/rdf-schema#label'), Literal(info['title'])))
        
        # Add director
        graph.add((movie_uri, DBPEDIA.director, Literal(info['director'])))
        
        # Add year
        graph.add((movie_uri, DBPEDIA.releaseDate, Literal(info['year'])))
        
        # Add cast members
        for i, actor in enumerate(info['cast'][:3]):
            graph.add((movie_uri, DBPEDIA[f'cast_member_{i}'], Literal(actor)))
        
        # Add emotions (if provided in the updated database)
        if 'emotions' in info:
            # Get or create the emotion set for this movie
            emotion_set_uri = EMOTION[f'set_{movie_id}']
            
            # Ensure movie links to emotion set
            if (movie_uri, ONYX.hasEmotionSet, emotion_set_uri) not in graph:
                graph.add((movie_uri, ONYX.hasEmotionSet, emotion_set_uri))
            
            for emotion_name, intensity in info['emotions'].items():
                # Create emotion entry
                emotion_uri = EMOTION[f'{movie_id}_{emotion_name.lower()}']
                
                # Make sure emotion set is of correct type
                graph.add((emotion_set_uri, RDF.type, ONYX.AggregatedEmotionSet))
                
                # Link emotion to set
                if (emotion_set_uri, ONYX.hasEmotion, emotion_uri) not in graph:
                    graph.add((emotion_set_uri, ONYX.hasEmotion, emotion_uri))
                
                # Link emotion to movie (direct link too, for querying)
                if (movie_uri, ONYX.hasEmotion, emotion_uri) not in graph:
                    graph.add((movie_uri, ONYX.hasEmotion, emotion_uri))
                
                # Set emotion properties
                graph.add((emotion_uri, RDF.type, ONYX.AggregatedEmotion))
                graph.add((emotion_uri, ONYX.hasEmotionCategory, ONYX[emotion_name]))
                graph.add((emotion_uri, ONYX.hasEmotionIntensity, Literal(intensity, datatype=URIRef('http://www.w3.org/2001/XMLSchema#float'))))
                graph.add((emotion_uri, ONYX.algorithmConfidence, Literal(0.85, datatype=URIRef('http://www.w3.org/2001/XMLSchema#float'))))
                
                emotion_count += 1
        
        movie_count += 1
    
    # Save enriched graph
    graph.serialize(ttl_path, format='turtle')
    print(f'[OK] Enriched {movie_count} movies with metadata')
    print(f'[OK] Added {emotion_count} emotion associations')
    print(f'[OK] Updated {ttl_path}')
    
    return graph

if __name__ == '__main__':
    ttl_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'movie-emotions.ttl')
    enrich_movie_data(ttl_path)
