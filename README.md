# 🎬 Semantic Movie Recommender

An emotion-based movie recommendation system using semantic web technologies, RDF knowledge graphs, and SPARQL queries.

**Features:**
- 🎭 7 emotion categories (joy, sadness, fear, anger, disgust, surprise, trust)
- 🎚️ Intensity slider to customize recommendations
- 🎥 Smart recommendations from an RDF knowledge base
- 💾 SPARQL queries for precise movie matching
- 🎨 Beautiful React frontend with Tailwind CSS

---

## 🚀 Quick Start

### Prerequisites
- **Python 3.x** - https://www.python.org/
- **Node.js 16+** - https://nodejs.org/

### 1️⃣ Clone & Setup

```bash
# Clone the repository
git clone <repo-url>
cd Semantic-Movie-Recommender

# Install Python dependencies
pip install -r requirements.txt

# Install frontend dependencies
cd frontend
npm install
cd ..
```

### 2️⃣ Start the Servers

**Option A: Run Both Servers (Easiest)**

You can use the convenience scripts:

**On Windows:**
```bash
start_all.bat
```

**On Mac/Linux:**
```bash
bash start_all.sh
```

**Option B: Run Manually in Separate Terminals**

**Terminal 1 - Backend API Server:**
```bash
cd scripts
python api_server.py
```
Backend runs on: http://localhost:5000

**Terminal 2 - Frontend Development Server:**
```bash
cd frontend
npm run dev
```
Frontend runs on: http://localhost:5173

### 3️⃣ Open in Browser

Visit: **http://localhost:5173**

1. Select an emotion (joy, sadness, fear, anger, disgust, surprise, or trust)
2. Adjust the intensity slider (0-100%)
3. See personalized movie recommendations!

---

## 📋 Project Structure

```
Semantic-Movie-Recommender/
├── scripts/
│   ├── api_server.py              # Flask REST API server
│   ├── recommendation_engine.py   # Core recommendation logic
│   ├── sparql_recommender.py      # SPARQL/RDF queries
│   └── emotion_classifier.py      # Emotion detection
│
├── frontend/
│   ├── src/
│   │   ├── pages/Index.tsx        # Main recommendation page
│   │   ├── EmotionSelector.tsx    # Emotion buttons
│   │   ├── IntensitySlider.tsx    # Intensity control
│   │   ├── MovieCard.tsx          # Movie display
│   │   └── ...
│   └── package.json
│
├── movie-emotions.ttl              # RDF knowledge base
├── requirements.txt                # Python dependencies
└── README.md                       # This file
```

---

## 🔌 API Endpoints

The backend provides REST API endpoints:

### GET /api/health
Health check - verify server is running
```bash
curl http://localhost:5000/api/health
```

### GET /api/emotions
Get list of supported emotions
```bash
curl http://localhost:5000/api/emotions
```

### POST /api/recommend (Main Endpoint)
Get movie recommendations based on emotion & intensity
```bash
curl -X POST http://localhost:5000/api/recommend \
  -H "Content-Type: application/json" \
  -d '{
    "emotion": "joy",
    "intensity": 0.8,
    "count": 10
  }'
```

**Request Parameters:**
- `emotion` (required) - One of: joy, sadness, fear, anger, disgust, surprise, trust
- `intensity` (optional) - 0.0 to 1.0, default 0.5
- `count` (optional) - 1-50 results, default 10

**Response Example:**
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
      "cast": ["Actor1", "Actor2"],
      "emotion": "joy",
      "intensity": 0.85,
      "confidence": 0.92,
      "score": 0.89,
      "description": "A classic silent film..."
    },
    ...
  ]
}
```

### POST /api/journey
Get emotion progression journey (mood progression sequence)

### GET /api/popular
Get top-rated popular movies

---

## 🛠️ Development

### Backend Development

Python files are in `scripts/`:
- `api_server.py` - Flask REST API wrapper
- `recommendation_engine.py` - Recommendation algorithms
- `sparql_recommender.py` - RDF/SPARQL query logic

To modify backend:
1. Edit files in `scripts/`
2. Restart backend: `python api_server.py`

### Frontend Development

React/TypeScript files are in `frontend/src/`:
- `pages/Index.tsx` - Main recommendation page
- `EmotionSelector.tsx` - Emotion selection component
- `MovieCard.tsx` - Movie display component
- `hooks/useRecommendations.ts` - React Query hooks for API

To modify frontend:
1. Edit files in `frontend/src/`
2. Changes auto-reload (hot module replacement)

---

## 🎨 Emotions Supported

| Emotion | Icon | Description |
|---------|------|-------------|
| Joy | 😊 | Happy, positive, uplifting movies |
| Sadness | 😢 | Melancholic, dramatic, emotional movies |
| Fear | 👻 | Scary, suspenseful, horror movies |
| Anger | 😠 | Intense, action-packed, rage movies |
| Disgust | 🤢 | Disturbing, dark, negative movies |
| Surprise | ✨ | Unexpected, plot-twist, astonishing movies |
| Trust | ❤️ | Reliable, wholesome, trustworthy movies |

---

## 🗄️ Knowledge Base

**File:** `movie-emotions.ttl`

The system uses an RDF/Turtle knowledge base containing:
- 700+ movies with metadata (title, director, cast)
- Emotional annotations for each movie
- Confidence scores from NLP analysis
- Intensity values for emotional impact

Query format: SPARQL over RDF graph using RDFLib

---

## 🐛 Troubleshooting

### Backend won't start - "ModuleNotFoundError"
```bash
# Install missing Python packages
pip install -r requirements.txt
```

### Frontend won't start - "EADDRINUSE"
Port 5173 is already in use
```bash
# Kill existing process and try again
# On Windows:
taskkill /F /IM node.exe
# On Mac/Linux:
lsof -ti:5173 | xargs kill -9
```

### API returns no movies
- Check that `movie-emotions.ttl` exists in project root
- Verify backend is running: `curl http://localhost:5000/api/health`
- Check backend console for errors

### Movies have no descriptions
- Descriptions come from RDF data
- Some movies may not have description fields
- This is normal behavior

---

## 📦 Production Deployment

For production deployment:

### Frontend
```bash
cd frontend
npm run build
# Deploy the 'dist' folder to:
# - Vercel, Netlify, GitHub Pages, or any static host
```

### Backend
Deploy to:
- Heroku (with Procfile)
- Railway
- Render
- AWS Lambda
- Google Cloud Run

Update frontend API URL in `frontend/src/hooks/useRecommendations.ts`:
```typescript
const API_BASE_URL = 'https://your-api-domain.com/api';
```

---

## 📚 Technology Stack

**Frontend:**
- React 18 + TypeScript
- Vite (fast bundler)
- TanStack React Query (data fetching)
- Axios (HTTP client)
- Tailwind CSS (styling)
- shadcn/ui (UI components)
- Lucide React (icons)

**Backend:**
- Python 3.x
- Flask (REST API)
- Flask-CORS (cross-origin requests)
- RDFLib (RDF/OWL handling)
- SPARQL queries

**Knowledge Base:**
- RDF/Turtle format
- Semantic Web standards
- SPARQL query language

---

## 📖 Documentation

- **[QUICK_REFERENCE.md](QUICK_REFERENCE.md)** - Commands & quick tips
- **[INTEGRATION_GUIDE.md](INTEGRATION_GUIDE.md)** - Complete setup guide
- **[ARCHITECTURE.md](ARCHITECTURE.md)** - System architecture & design

---

## 🤝 Contributing

Want to add features or fix bugs?

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📝 License

This project is open source and available under the ISC License.

---

## 🙋 Support

Having issues? Check:
1. **[QUICK_REFERENCE.md](QUICK_REFERENCE.md)** - Common questions
2. **[INTEGRATION_GUIDE.md](INTEGRATION_GUIDE.md)** - Troubleshooting section
3. Verify both servers are running
4. Check that `movie-emotions.ttl` is in the root directory

---

## 🎓 Learn More

- **React Query:** https://tanstack.com/query
- **Flask:** https://flask.palletsprojects.com
- **SPARQL:** https://www.w3.org/TR/sparql11-query/
- **RDF/Turtle:** https://www.w3.org/TR/turtle/

---

**Status:** ✅ Production Ready

Built with ❤️ for emotion-based movie recommendations
