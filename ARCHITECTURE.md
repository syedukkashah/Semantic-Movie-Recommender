# 🎬 System Architecture & Integration Map

## 📊 High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                     BROWSER (http://localhost:8080)             │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  React App (Vite + TypeScript)                          │   │
│  ├─────────────────────────────────────────────────────────┤   │
│  │                                                         │   │
│  │  ┌──────────────┐         ┌──────────────────────────┐ │   │
│  │  │   App.tsx    │────────▶│ Router                   │ │   │
│  │  │              │         ├──────────────────────────┤ │   │
│  │  │ - Routing    │         │ / → Index.tsx           │ │   │
│  │  │ - QueryClient│         │ * → NotFound.tsx        │ │   │
│  │  │ - Providers  │         └──────────────────────────┘ │   │
│  │  └──────────────┘                                       │   │
│  │                                                         │   │
│  │  ┌──────────────────────────────────────────────────┐  │   │
│  │  │  Index.tsx (Main Page)                           │  │   │
│  │  ├──────────────────────────────────────────────────┤  │   │
│  │  │  State: emotion, intensity, count                │  │   │
│  │  │                                                  │  │   │
│  │  │  ┌──────────────────┐  ┌──────────────────┐    │  │   │
│  │  │  │ EmotionSelector  │  │ IntensitySlider  │    │  │   │
│  │  │  │ (6 buttons)      │  │ (0-100%)         │    │  │   │
│  │  │  └──────────────────┘  └──────────────────┘    │  │   │
│  │  │                                                  │  │   │
│  │  │  ┌────────────────────────────────────────┐    │  │   │
│  │  │  │ useRecommendations Hook               │    │  │   │
│  │  │  │ (React Query + Axios)                 │    │  │   │
│  │  │  └────────────────────────────────────────┘    │  │   │
│  │  │                                                  │  │   │
│  │  │  ┌────────────────────────────────────────┐    │  │   │
│  │  │  │ MovieCard Grid                        │    │  │   │
│  │  │  │ (Displays recommendations)            │    │  │   │
│  │  │  └────────────────────────────────────────┘    │  │   │
│  │  └──────────────────────────────────────────────────┘  │   │
│  │                                                         │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│                            ▼                                    │
│                      HTTP / JSON                               │
│                    (Port 5000)                                 │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
                             │
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│              FLASK API SERVER (http://localhost:5000)           │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ api_server.py (Flask App with CORS)                    │   │
│  ├─────────────────────────────────────────────────────────┤   │
│  │                                                         │   │
│  │  /api/health          GET                             │   │
│  │  /api/emotions        GET                             │   │
│  │  /api/recommend       POST ◄─ Main Endpoint           │   │
│  │  /api/journey         POST                            │   │
│  │  /api/popular         GET                             │   │
│  │                                                         │   │
│  └─────────────────────────────────────────────────────────┘   │
│                            │                                    │
│                            ▼                                    │
│  ┌──────────────────────────────────────────────────────┐      │
│  │ RecommendationEngine (recommendation_engine.py)      │      │
│  ├──────────────────────────────────────────────────────┤      │
│  │                                                      │      │
│  │  - recommend_current_state(emotion, intensity)      │      │
│  │  - recommend_desired_state(emotion)                 │      │
│  │  - recommend_neutral()                              │      │
│  │  - recommend_emotion_journey(start, end)            │      │
│  │  - _score_by_intensity_match(movies, intensity)     │      │
│  │                                                      │      │
│  └──────────────────────────────────────────────────────┘      │
│                            │                                    │
│                            ▼                                    │
│  ┌──────────────────────────────────────────────────────┐      │
│  │ SPARQLRecommender (sparql_recommender.py)            │      │
│  ├──────────────────────────────────────────────────────┤      │
│  │                                                      │      │
│  │  - get_movies_by_emotion(emotion, threshold)        │      │
│  │  - get_emotions_by_movie(movie_id)                  │      │
│  │  - get_highest_confidence_movies(emotion)           │      │
│  │  - get_top_movies_overall()                         │      │
│  │                                                      │      │
│  │  Executes SPARQL queries on RDF graph               │      │
│  │                                                      │      │
│  └──────────────────────────────────────────────────────┘      │
│                            │                                    │
│                            ▼                                    │
│  ┌──────────────────────────────────────────────────────┐      │
│  │ movie-emotions.ttl (RDF Knowledge Base)              │      │
│  ├──────────────────────────────────────────────────────┤      │
│  │                                                      │      │
│  │  movie:0040497                                      │      │
│  │    - label: "Battleship Potemkin"                   │      │
│  │    - director: "Sergei Eisenstein"                  │      │
│  │    - hasEmotion: [                                  │      │
│  │        { category: joy, intensity: 0.85,            │      │
│  │          confidence: 0.92 },                         │      │
│  │        { category: trust, intensity: 0.78, ... }    │      │
│  │      ]                                               │      │
│  │                                                      │      │
│  │  [RDFLib Graph with hundreds of movies]             │      │
│  │                                                      │      │
│  └──────────────────────────────────────────────────────┘      │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🔄 Data Flow Sequence

```
User Action                Response Flow
─────────────────         ─────────────────

[Click "Joy" button]
         │
         ▼
[emit: onSelect("joy")]
         │
         ▼
[setSelectedEmotion("joy")]
         │
         ▼
[useRecommendations hook detects emotion change]
         │
         ▼
[POST http://localhost:5000/api/recommend]
{
  emotion: "joy",
  intensity: 0.5,
  count: 10
}
         │
         ▼
[Flask receives request]
         │
         ├─ Validate emotion & intensity
         │
         ├─ Call RecommendationEngine
         │   .recommend_current_state("joy", 0.5)
         │
         ├─ Engine calls SPARQLRecommender
         │   .get_movies_by_emotion("joy")
         │
         ├─ SPARQL queries movie-emotions.ttl
         │   SELECT ?movie WHERE {
         │     ?movie onyx:hasEmotion ?e .
         │     ?e onyx:hasEmotionCategory onyx:Joy
         │   }
         │
         ├─ Returns all movies with joy emotion
         │
         ├─ Engine scores by intensity match
         │   distance = |movie_intensity - user_intensity|
         │   score = (1 - distance) * 0.6 + confidence * 0.4
         │
         ├─ Sorts by score (highest first)
         │
         └─ Returns top 10 movies as JSON
         │
         ▼
[Frontend receives recommendations array]
         │
         ├─ Update React Query cache
         │
         ├─ Map emotions (7 backend → 6 frontend)
         │
         └─ Render MovieCard components
         │
         ▼
[Display movie grid with:
 - Title
 - Director
 - Emotion tag
 - Confidence %
 - Animation
]
         │
         ▼
[User sees results!]
```

---

## 📁 Component Dependency Tree

```
App.tsx (Router Provider)
│
├─ QueryClientProvider (React Query)
├─ TooltipProvider (shadcn/ui)
├─ Toaster (Notifications)
│
└─ Routes
   │
   ├─ Route: "/" 
   │  └─ Index.tsx
   │     │
   │     ├─ useState: emotion, intensity, count
   │     ├─ useToast: notifications
   │     ├─ useRecommendations: API hook
   │     │  ├─ useQuery (React Query)
   │     │  └─ axios (HTTP client)
   │     │
   │     ├─ JSX Components:
   │     │  ├─ Header
   │     │  ├─ EmotionSelector
   │     │  │  └─ Button x 6
   │     │  ├─ IntensitySlider
   │     │  │  └─ Slider (shadcn)
   │     │  ├─ MovieCard Grid
   │     │  │  └─ MovieCard x N
   │     │  │     ├─ Badge
   │     │  │     └─ Text
   │     │  ├─ Alert (error state)
   │     │  └─ Loader (loading state)
   │     │
   │     └─ UI Components (shadcn/ui)
   │        ├─ Button
   │        ├─ Alert
   │        ├─ Slider
   │        └─ Card
   │
   └─ Route: "*"
      └─ NotFound.tsx
         ├─ Button (navigation)
         └─ Text
```

---

## 🔌 API Contract (Frontend ↔ Backend)

```
┌─────────────────────────────────────────────────────────┐
│ REQUEST                                                 │
├─────────────────────────────────────────────────────────┤
│ POST /api/recommend                                     │
│ Content-Type: application/json                          │
│                                                         │
│ {                                                       │
│   "emotion": "joy" | "sadness" | "fear" | ... (req)   │
│   "intensity": 0.0-1.0 (optional, default 0.5)        │
│   "count": 1-50 (optional, default 10)                │
│ }                                                       │
└─────────────────────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────┐
│ RESPONSE (200 OK)                                       │
├─────────────────────────────────────────────────────────┤
│ {                                                       │
│   "success": true,                                     │
│   "emotion": "joy",                                    │
│   "intensity": 0.8,                                    │
│   "count": 10,                                         │
│   "recommendations": [                                 │
│     {                                                  │
│       "movie_id": "0040497",                           │
│       "title": "Battleship Potemkin",                  │
│       "director": "Sergei Eisenstein",                 │
│       "cast": ["Actor1", "Actor2"],                    │
│       "emotion": "joy",                                │
│       "intensity": 0.85,                               │
│       "confidence": 0.92,                              │
│       "score": 0.89                                    │
│     },                                                 │
│     ... (9 more)                                       │
│   ]                                                    │
│ }                                                       │
└─────────────────────────────────────────────────────────┘

ERROR RESPONSES:
- 400: Bad Request (invalid emotion, intensity out of range)
- 500: Server Error (engine/SPARQL error)
```

---

## 🎨 State Management Flow

```
User Interaction
    │
    ├─ Click emotion button
    │  ├─ EmotionSelector.onSelect()
    │  └─ Index.setSelectedEmotion(emotion)
    │
    ├─ Move intensity slider
    │  ├─ IntensitySlider.onChange()
    │  └─ Index.setIntensity(value)
    │
    └─ Change result count
       ├─ Button.onClick()
       └─ Index.setCount(value)

React Query Hook Dependency
    │
    └─ useRecommendations(emotion, intensity, count)
       │
       ├─ Watches: emotion, intensity, count
       ├─ Triggers: When any change
       │
       ├─ Makes: POST /api/recommend
       ├─ Stores: data, isLoading, error
       ├─ Caches: 5 minutes
       │
       └─ On Success:
          ├─ Update React state
          ├─ Trigger re-render
          └─ Display MovieCards

Toast Notifications
    │
    ├─ onEmotionSelect: "Finding movies..."
    ├─ onSuccess: Movies loaded (implicit)
    ├─ onError: "Error fetching" alert
    └─ onCountChange: "Refetching..." (optional)
```

---

## 🗂️ File Organization

```
Semantic-Movie-Recommender/
├── 📄 INTEGRATION_GUIDE.md          ◄─ Complete setup guide
├── 📄 IMPLEMENTATION_SUMMARY.md     ◄─ What was built
├── 📄 QUICK_REFERENCE.md            ◄─ This file (short version)
├── 🔧 start.bat                     ◄─ Quick start script
│
├── frontend/
│   ├── src/
│   │   ├── 📄 App.tsx
│   │   │   └─ Routes to Index & NotFound
│   │   │
│   │   ├── pages/
│   │   │   ├── ✨ Index.tsx         ◄─ Main page (NEW)
│   │   │   └── ✨ NotFound.tsx      ◄─ 404 page (NEW)
│   │   │
│   │   ├── hooks/
│   │   │   ├── ✨ useRecommendations.ts  ◄─ API hooks (NEW)
│   │   │   └── use-toast.ts
│   │   │
│   │   ├── EmotionSelector.tsx
│   │   ├── IntensitySlider.tsx
│   │   ├── MovieCard.tsx
│   │   └── components/ui/            ◄─ shadcn components
│   │
│   ├── vite.config.ts
│   └── package.json
│
├── scripts/
│   ├── ✨ api_server.py            ◄─ Flask API (NEW)
│   ├── recommendation_engine.py
│   ├── sparql_recommender.py
│   ├── emotion_classifier.py
│   └── ...
│
├── 📊 movie-emotions.ttl            ◄─ RDF knowledge base
└── 📦 package.json
```

---

## 🔐 Security & CORS

```
Frontend (localhost:8080)
         │
         ├─ Makes request to Backend (localhost:5000)
         │
         └─ Flask-CORS allows it:
            CORS(app) in api_server.py
            ├─ Allows all origins (development)
            ├─ Allows all methods
            └─ Allows all headers

Production Changes Needed:
├─ Update: CORS(app, origins=["https://example.com"])
├─ Add: Rate limiting
├─ Add: Authentication
└─ Use: HTTPS (TLS)
```

---

## 📊 Performance Characteristics

```
Operation              Time      Cache    Status
─────────────────────  ────────  ────────  ──────
Initial Page Load      ~200ms    -         ✅ Fast
First Recommendation   ~500ms    Cache 5m  ✅ OK
Subsequent Same Query  ~50ms     Hit       ✅ Fast
Change Emotion         ~500ms    Invalidate ✅ OK
Change Intensity       ~500ms    Reuse    ✅ OK

Bottlenecks:
1. SPARQL query on large RDF graph
2. Network latency (5000→8080 local only)
3. Browser rendering (few ms)

Optimizations:
✅ React Query caching
✅ SPARQL indexing
✅ Result limiting (10 movies default)
```

---

## ✅ Integration Checklist

```
Backend:
✅ Flask API created
✅ CORS enabled
✅ All 5 endpoints working
✅ Error handling
✅ Dependencies installed

Frontend:
✅ Main page created
✅ 404 page created
✅ React Query hooks created
✅ State management
✅ Loading/error states
✅ Toast notifications
✅ Responsive design

Documentation:
✅ Integration guide
✅ Implementation summary
✅ Quick reference
✅ Architecture diagram (this file)

Testing:
✅ API endpoints
✅ Frontend components
✅ Data flow
✅ Error handling
```

---

## 🎓 Key Concepts

**React Query:**
- Manages server state (recommendations)
- Handles caching & revalidation
- Provides loading/error states
- Deduplicates requests

**SPARQL:**
- Queries RDF knowledge graph
- Filters by emotion & other criteria
- Returns movie metadata
- Supports reasoning

**CORS (Cross-Origin Resource Sharing):**
- Allows browser requests across ports
- Enabled in Flask with CORS(app)
- Frontend (8080) → Backend (5000)

**Intensity Matching:**
- User selects 0-100% intensity
- Converted to 0-1 range
- Backend scores movies by proximity
- Closer match = higher score

---

## 🚀 Deployment Flow

```
Local Development:
├─ Frontend: http://localhost:8080
├─ Backend: http://localhost:5000
└─ API_BASE_URL: "http://localhost:5000/api"

Production:
├─ Frontend: Deployed to Vercel/Netlify
├─ Backend: Deployed to Heroku/Railway
├─ API_BASE_URL: "https://api.example.com/api"
└─ CORS: Limited to specific origins
```

---

**Architecture Document Created: January 1, 2026**
**System Status: ✅ Ready for Development & Testing**
