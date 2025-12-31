# Frontend-Backend Integration Guide

## 🎬 Overview
This document explains how to run and use the integrated Movie Recommender system with the Lovable frontend and Python backend.

---

## 📁 Project Structure

```
Semantic-Movie-Recommender/
├── frontend/                    # React/TypeScript frontend (Vite + Lovable)
│   ├── src/
│   │   ├── App.tsx             # Main app with routing (already configured)
│   │   ├── pages/
│   │   │   ├── Index.tsx       # ✨ NEW - Main recommendation page
│   │   │   └── NotFound.tsx    # ✨ NEW - 404 page
│   │   ├── components/
│   │   │   ├── EmotionSelector.tsx      # Emotion selection buttons
│   │   │   ├── IntensitySlider.tsx      # Intensity control (0-100%)
│   │   │   └── MovieCard.tsx            # Individual movie display
│   │   ├── hooks/
│   │   │   └── useRecommendations.ts   # ✨ NEW - React Query hooks
│   │   └── ...
│   ├── package.json
│   └── vite.config.ts
│
├── scripts/                     # Python backend
│   ├── api_server.py           # ✨ NEW - Flask API server
│   ├── recommendation_engine.py # Core recommendation logic
│   ├── sparql_recommender.py   # SPARQL queries to RDF
│   ├── emotion_classifier.py   # Emotion detection
│   └── ...
│
├── movie-emotions.ttl          # RDF knowledge base
└── package.json
```

---

## 🚀 Getting Started

### Step 1: Install Dependencies

**Backend (Python):**
```bash
cd d:\Semantic-Movie-Recommender
pip install flask flask-cors
```
✓ Already done!

**Frontend (Node.js):**
```bash
cd d:\Semantic-Movie-Recommender\frontend
npm install
```

### Step 2: Start the Backend API Server

**From `scripts/` directory:**
```bash
cd d:\Semantic-Movie-Recommender\scripts
python api_server.py
```

Expected output:
```
============================================================
🎬 MOVIE RECOMMENDER API SERVER
============================================================
✓ Backend: d:\Semantic-Movie-Recommender\movie-emotions.ttl
✓ Emotions: joy, sadness, fear, anger, disgust, surprise, trust

📍 Starting server on http://localhost:5000

Available endpoints:
  GET  /api/health          - Health check
  GET  /api/emotions        - List supported emotions
  POST /api/recommend       - Get recommendations by emotion/intensity
  POST /api/journey         - Get emotion progression journey
  GET  /api/popular         - Get popular movies

Frontend: http://localhost:8080
============================================================
```

**Keep this terminal open!**

### Step 3: Start the Frontend Development Server

**In a new terminal, from `frontend/` directory:**
```bash
cd d:\Semantic-Movie-Recommender\frontend
npm run dev
```

Expected output:
```
VITE v5.x.x  ready in xxx ms

➜  Local:   http://localhost:5173/
➜  press h to show help
```

### Step 4: Open in Browser

Visit: **http://localhost:5173/**

---

## 💡 How It Works

### User Flow

```
1. User selects emotion (joy, sadness, etc.)
   ↓
2. User adjusts intensity slider (0-100%)
   ↓
3. Frontend sends POST request to http://localhost:5000/api/recommend
   {
     "emotion": "joy",
     "intensity": 0.8,
     "count": 10
   }
   ↓
4. Backend RecommendationEngine queries RDF graph
   - SPARQLRecommender.get_movies_by_emotion(emotion)
   - Scores movies by intensity match
   ↓
5. Backend returns JSON response
   {
     "success": true,
     "recommendations": [
       {
         "movie_id": "0040497",
         "title": "Battleship Potemkin",
         "director": "Sergei Eisenstein",
         "emotion": "joy",
         "intensity": 0.85,
         "confidence": 0.92,
         "score": 0.89
       },
       ...
     ]
   }
   ↓
6. Frontend displays MovieCard components with recommendations
```

---

## 🔌 API Endpoints

### 1. Health Check
```http
GET http://localhost:5000/api/health
```
Response: `{ "status": "ok", "message": "..." }`

### 2. Get Supported Emotions
```http
GET http://localhost:5000/api/emotions
```
Response:
```json
{
  "emotions": ["joy", "sadness", "fear", "anger", "disgust", "surprise", "trust"]
}
```

### 3. Get Recommendations (Main Endpoint)
```http
POST http://localhost:5000/api/recommend
Content-Type: application/json

{
  "emotion": "joy",
  "intensity": 0.8,
  "count": 10
}
```

**Response:**
```json
{
  "success": true,
  "emotion": "joy",
  "intensity": 0.8,
  "count": 10,
  "recommendations": [
    {
      "movie_id": "0040497",
      "title": "Battleship Potemkin",
      "director": "Sergei Eisenstein",
      "cast": ["Aleksandr Antonov", "Vladimir Barsky"],
      "emotion": "joy",
      "intensity": 0.85,
      "confidence": 0.92,
      "score": 0.89
    },
    ...
  ]
}
```

**Parameters:**
- `emotion` (required): One of `joy`, `sadness`, `fear`, `anger`, `disgust`, `surprise`, `trust`
- `intensity` (optional): 0.0-1.0, default 0.5
- `count` (optional): 1-50, default 10

---

### 4. Get Emotion Journey (Mood Progression)
```http
POST http://localhost:5000/api/journey
Content-Type: application/json

{
  "startEmotion": "sadness",
  "endEmotion": "joy",
  "count": 5
}
```
Returns a sequence of movies that progress from one emotion to another.

---

### 5. Get Popular Movies
```http
GET http://localhost:5000/api/popular?count=10
```
Returns top-rated movies without emotion filtering.

---

## 🎨 Frontend Components

### Index.tsx (New Main Page)
- **Purpose:** Main recommendation interface
- **Features:**
  - Emotion selector (6 buttons: joy, sadness, fear, anger, trust, surprise)
  - Intensity slider (0-100%)
  - Movie count selector (5, 10, 15, 20)
  - Recommendation grid with loading/error states
  - Toast notifications for feedback

### useRecommendations.ts (New Hook)
```typescript
// Get recommendations by emotion/intensity
const { data: movies, isLoading, error } = useRecommendations(
  emotion,      // "joy" | null
  intensity,    // 0-1
  count         // number
);

// Get emotion journey
const { data: journey } = useJourney(startEmotion, endEmotion);

// Get popular movies
const { data: popular } = usePopularMovies(10);
```

---

## 🔧 Troubleshooting

### Error: "Cannot connect to http://localhost:5000"
**Solution:** Make sure the Flask API server is running. Run:
```bash
cd d:\Semantic-Movie-Recommender\scripts
python api_server.py
```

### Error: "TTL file not found"
**Solution:** Ensure `movie-emotions.ttl` exists in the project root:
```bash
cd d:\Semantic-Movie-Recommender
ls movie-emotions.ttl
```

### Error: "ModuleNotFoundError: No module named 'sparql_recommender'"
**Solution:** Make sure you're running `api_server.py` from the `scripts/` directory:
```bash
cd d:\Semantic-Movie-Recommender\scripts
python api_server.py
```

### Frontend shows loading spinner forever
**Solution:** 
1. Check that API server is running and healthy:
   ```bash
   curl http://localhost:5000/api/health
   ```
2. Check browser console (F12) for network errors
3. Ensure CORS is enabled on the backend (it is by default)

---

## 📝 Integration Summary

| Component | Status | Details |
|-----------|--------|---------|
| Flask API Server | ✅ Created | [scripts/api_server.py](scripts/api_server.py) |
| React Query Hooks | ✅ Created | [frontend/src/hooks/useRecommendations.ts](frontend/src/hooks/useRecommendations.ts) |
| Index Page | ✅ Created | [frontend/src/pages/Index.tsx](frontend/src/pages/Index.tsx) |
| NotFound Page | ✅ Created | [frontend/src/pages/NotFound.tsx](frontend/src/pages/NotFound.tsx) |
| App.tsx Routing | ✅ Already Set | Uses Index & NotFound |
| EmotionSelector | ✅ Existing | 6 emotions (excludes disgust) |
| IntensitySlider | ✅ Existing | 0-100% control |
| MovieCard | ✅ Existing | Displays recommendations |
| Backend Dependencies | ✅ Installed | Flask, Flask-CORS |

---

## 🎯 Key Features Implemented

✅ **Emotion-Based Recommendations**
- User selects emotion → API returns matching movies

✅ **Intensity Matching**
- Slider controls preference for strong/subtle movies
- Backend scores by intensity similarity

✅ **Loading & Error States**
- Loading spinner while fetching
- Toast notifications for feedback
- Error alert with helpful message

✅ **Responsive UI**
- Mobile-friendly layout
- Animations and transitions
- Card-based movie display

✅ **Full CORS Integration**
- Frontend (port 8080) ↔ Backend (port 5000)
- No CORS errors

---

## 🚀 Next Steps (Optional Enhancements)

1. **Add Emotion Journey Feature**
   - "Lift my mood" button that transitions from one emotion to another
   - Uses `/api/journey` endpoint

2. **Reasoning Panel**
   - Show why each movie was recommended
   - Display confidence scores
   - Use `ReasoningPanel.tsx` component

3. **Add Disgust Emotion**
   - Frontend currently maps it to sadness
   - Add button and color styling for disgust

4. **Search & Filter**
   - Search by movie title
   - Filter by director, cast, year
   - Combine with emotion recommendations

5. **Favorites & History**
   - Save favorite recommendations
   - Show recommendation history
   - Use localStorage or backend database

6. **Deploy**
   - Build frontend: `npm run build`
   - Deploy to Vercel/Netlify
   - Deploy backend to Heroku/Railway

---

## 📚 File References

- **Backend entry point:** [scripts/api_server.py](scripts/api_server.py)
- **Recommendation logic:** [scripts/recommendation_engine.py](scripts/recommendation_engine.py)
- **SPARQL queries:** [scripts/sparql_recommender.py](scripts/sparql_recommender.py)
- **Frontend main page:** [frontend/src/pages/Index.tsx](frontend/src/pages/Index.tsx)
- **API hooks:** [frontend/src/hooks/useRecommendations.ts](frontend/src/hooks/useRecommendations.ts)
- **Knowledge base:** [movie-emotions.ttl](movie-emotions.ttl)

---

## ✨ Summary

Your Movie Recommender is now **fully integrated**! The frontend and backend communicate through a clean REST API. Users can:

1. Select an emotion
2. Adjust intensity
3. See personalized movie recommendations

All powered by your semantic knowledge graph and SPARQL engine!

Happy recommending! 🎬🍿
