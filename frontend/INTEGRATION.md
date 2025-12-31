# 🎬 Movie Recommender - Integration Complete!

## ✨ What Has Been Implemented

### Backend (Python)
✅ **Flask API Server** ([scripts/api_server.py](../scripts/api_server.py))
- REST API wrapper around RecommendationEngine
- CORS enabled for frontend on localhost:8080
- 5 main endpoints for recommendations, emotions, and journeys

### Frontend (React/TypeScript)
✅ **Main Recommendation Page** ([src/pages/Index.tsx](./src/pages/Index.tsx))
- Emotion selector (6 emotions)
- Intensity slider (0-100%)
- Recommendation count selector
- Live movie grid with loading/error states

✅ **React Query Hooks** ([src/hooks/useRecommendations.ts](./src/hooks/useRecommendations.ts))
- `useRecommendations()` - Get movies by emotion/intensity
- `useJourney()` - Get emotion progression sequence
- `usePopularMovies()` - Get top-rated movies
- `useEmotions()` - Get supported emotions

✅ **NotFound Page** ([src/pages/NotFound.tsx](./src/pages/NotFound.tsx))
- 404 error handling with navigation

### Existing Components
✅ **EmotionSelector.tsx** - 6 emotion buttons (joy, sadness, fear, anger, trust, surprise)
✅ **IntensitySlider.tsx** - 0-100% intensity control
✅ **MovieCard.tsx** - Movie display with emotion tag and confidence

---

## 🚀 Quick Start

### Option 1: Use the Start Script (Recommended)
```bash
# From project root
start.bat
```
This opens two console windows and launches both servers + browser.

### Option 2: Manual Start

**Terminal 1 - Backend:**
```bash
cd scripts
python api_server.py
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

Then open: http://localhost:8080

---

## 📋 Prerequisites

- ✅ Python 3.x with Flask & Flask-CORS installed
- ✅ Node.js 16+ with npm
- ✅ movie-emotions.ttl in project root

---

## 🔄 How It Works

```
Browser (React)
    ↓
[EmotionSelector: joy] [IntensitySlider: 80%]
    ↓
POST http://localhost:5000/api/recommend
    ↓
Flask Server
    ↓
RecommendationEngine (Python)
    ↓
SPARQLRecommender → Query RDF Graph
    ↓
Score & Return Movies
    ↓
React Displays [MovieCard, MovieCard, ...]
```

---

## 📝 Emotions Supported

**Backend supports 7 emotions:**
- `joy` - Happy, positive movies
- `sadness` - Melancholic, dramatic movies
- `fear` - Scary, suspenseful movies
- `anger` - Intense, action-packed movies
- `disgust` - Disturbing, dark movies
- `surprise` - Unexpected, plot-twist movies
- `trust` - Reliable, wholesome movies

**Frontend shows 6 emotions:**
(Excludes `disgust` for user preference)

---

## 🎯 Key Features

| Feature | Details |
|---------|---------|
| **Emotion Selection** | 6 buttons for quick selection |
| **Intensity Control** | Slider for fine-tuning recommendation strength |
| **Result Count** | Choose 5, 10, 15, or 20 recommendations |
| **Loading States** | Animated spinner while fetching |
| **Error Handling** | Alert if API unavailable |
| **Toast Feedback** | Real-time user feedback |
| **Responsive UI** | Works on mobile & desktop |
| **Dark Mode Ready** | Full theme support |

---

## 🔌 API Integration

The frontend uses **React Query** + **Axios** to communicate with the backend.

### Example: Getting Recommendations
```typescript
// In component
const { data: movies, isLoading } = useRecommendations(
  selectedEmotion,      // "joy"
  intensity / 100,      // 0.8 (80%)
  count                 // 10
);

// Automatically handles:
// - HTTP request to POST /api/recommend
// - Caching & revalidation
// - Loading/error states
// - Data transformation
```

### Example: Manual API Call
```typescript
const { mutate, isPending } = useRecommendationsMutation();

mutate({
  emotion: "joy",
  intensity: 0.8,
  count: 10
});
```

---

## 📦 Dependencies

### Backend
- `flask` - Web server
- `flask-cors` - Cross-origin requests
- `rdflib` - RDF graph handling (already in scripts)

### Frontend
- `react` - UI framework
- `react-router-dom` - Routing
- `@tanstack/react-query` - Data fetching
- `axios` - HTTP client
- `tailwindcss` - Styling
- `shadcn/ui` - UI components
- `lucide-react` - Icons

---

## 🧪 Testing

### Test Backend
```bash
# Test API health
curl http://localhost:5000/api/health

# Get emotions
curl http://localhost:5000/api/emotions

# Get recommendations
curl -X POST http://localhost:5000/api/recommend \
  -H "Content-Type: application/json" \
  -d '{"emotion":"joy","intensity":0.8,"count":5}'
```

### Test Frontend
1. Open http://localhost:8080
2. Click emotion button (e.g., "Joy")
3. Adjust intensity slider
4. See recommendations appear
5. Check network tab (F12) for API calls

---

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| **Connection refused on :5000** | Backend server not running. Run `python scripts/api_server.py` |
| **Loading spinner never stops** | Check browser console (F12) for network errors. Verify backend health. |
| **CORS error** | Backend Flask-CORS is enabled. Check API server console for errors. |
| **No movies showing** | Check movie-emotions.ttl exists. Verify backend can read RDF file. |
| **Module not found error (Python)** | Run `python api_server.py` from `scripts/` directory, not root. |

---

## 📁 Project Structure

```
Semantic-Movie-Recommender/
├── frontend/
│   ├── src/
│   │   ├── pages/
│   │   │   ├── Index.tsx ✨ NEW - Main page
│   │   │   └── NotFound.tsx ✨ NEW - 404 page
│   │   ├── hooks/
│   │   │   └── useRecommendations.ts ✨ NEW - API hooks
│   │   ├── App.tsx (routing configured)
│   │   ├── EmotionSelector.tsx (existing)
│   │   ├── IntensitySlider.tsx (existing)
│   │   ├── MovieCard.tsx (existing)
│   │   └── ...
│   ├── package.json
│   └── vite.config.ts
│
├── scripts/
│   ├── api_server.py ✨ NEW - Flask server
│   ├── recommendation_engine.py (existing)
│   ├── sparql_recommender.py (existing)
│   └── ...
│
├── start.bat ✨ NEW - Quick start script
├── INTEGRATION_GUIDE.md ✨ NEW - Full integration docs
├── movie-emotions.ttl (knowledge base)
└── package.json
```

---

## 🎓 Learning & Extension

### Want to add a feature?

1. **Add new emotion:**
   - Backend: Emotion already in `recommendation_engine.py` list
   - Frontend: Add button to `EmotionSelector.tsx` + color styling

2. **Add reasoning explanation:**
   - Use existing `ReasoningPanel.tsx` component
   - Display in `MovieCard.tsx`
   - Add to API response in `api_server.py`

3. **Add user preferences:**
   - Store in localStorage or backend
   - Filter recommendations by preferences
   - Add settings page

4. **Add search:**
   - Create new API endpoint `/api/search`
   - Add search input to `Index.tsx`
   - Display combined results

---

## 🌐 Deployment

### Frontend
```bash
npm run build      # Creates optimized dist/
# Deploy dist/ to Vercel, Netlify, or any static host
```

### Backend
```bash
# Deploy to:
# - Heroku (free dyno)
# - Railway
# - Render
# - AWS Lambda

# Update frontend API_BASE_URL to deployed backend URL
# In: frontend/src/hooks/useRecommendations.ts
const API_BASE_URL = 'https://your-api.example.com/api';
```

---

## 📞 Support

- **Frontend Issues:** Check `frontend/` console (F12)
- **Backend Issues:** Check Flask console output
- **API Issues:** Test with curl commands
- **Network Issues:** Ensure both servers are running on correct ports

---

## ✅ Checklist Before Going Live

- [ ] Backend server starts without errors
- [ ] Frontend loads at localhost:8080
- [ ] Selecting emotion triggers API call
- [ ] Movies load and display
- [ ] Intensity slider works
- [ ] No console errors (F12)
- [ ] movie-emotions.ttl is valid
- [ ] CORS working (no 403 errors)

---

**Status: ✅ Integration Complete & Ready to Use!**

🎬 Happy recommending! 🍿
