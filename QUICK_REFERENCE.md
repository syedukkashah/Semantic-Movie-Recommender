# 🎬 Movie Recommender - Quick Reference Card

## 🚀 Start Servers (Choose One Method)

### Method 1: One Command (Easiest)
```bash
start.bat
```
✅ Opens 2 console windows + browser automatically

### Method 2: Manual (Two Terminals)
**Terminal 1:**
```bash
cd scripts
python api_server.py
```

**Terminal 2:**
```bash
cd frontend
npm run dev
```

Then open: **http://localhost:8080**

---

## 🔗 Port Reference

| Service | Port | URL |
|---------|------|-----|
| Frontend | 8080 | http://localhost:8080 |
| Backend API | 5000 | http://localhost:5000 |

---

## 📋 What Each Component Does

| Component | Purpose | Location |
|-----------|---------|----------|
| **Index Page** | Main recommendation UI | `frontend/src/pages/Index.tsx` |
| **EmotionSelector** | 6 emotion buttons | `frontend/src/EmotionSelector.tsx` |
| **IntensitySlider** | 0-100% intensity control | `frontend/src/IntensitySlider.tsx` |
| **MovieCard** | Individual movie display | `frontend/src/MovieCard.tsx` |
| **useRecommendations** | API hooks for data fetching | `frontend/src/hooks/useRecommendations.ts` |
| **Flask API Server** | Backend API wrapper | `scripts/api_server.py` |
| **RecommendationEngine** | Core recommendation logic | `scripts/recommendation_engine.py` |

---

## 🎯 User Flow

```
1. Select emotion (6 buttons)
   ↓
2. Adjust intensity (slider 0-100%)
   ↓
3. Choose result count (5/10/15/20)
   ↓
4. See recommendations (movie grid)
```

---

## 📡 API Endpoints

### Get Recommendations (Main)
```bash
curl -X POST http://localhost:5000/api/recommend \
  -H "Content-Type: application/json" \
  -d '{
    "emotion": "joy",
    "intensity": 0.8,
    "count": 10
  }'
```

### Get Emotions List
```bash
curl http://localhost:5000/api/emotions
```

### Get Popular Movies
```bash
curl http://localhost:5000/api/popular?count=10
```

### Health Check
```bash
curl http://localhost:5000/api/health
```

---

## 🎨 Emotions Supported

| Backend | Frontend | Icon |
|---------|----------|------|
| joy | ✅ | 😊 |
| sadness | ✅ | 😢 |
| fear | ✅ | 👻 |
| anger | ✅ | 😠 |
| disgust | Maps to sadness | 🤢 |
| surprise | ✅ | ✨ |
| trust | ✅ | ❤️ |

---

## ⚡ Quick Troubleshooting

| Problem | Fix |
|---------|-----|
| **Port 5000 refused** | Kill other process: `netstat -ano \| findstr :5000` |
| **Port 8080 refused** | Try `npm run dev -- --port 3000` |
| **Module not found** | Run from `scripts/` directory, not root |
| **No movies showing** | Check movie-emotions.ttl exists in root |
| **CORS error** | Ensure `api_server.py` is running |
| **Loading forever** | Check browser F12 console for network errors |

---

## 📚 Documentation Files

- **[INTEGRATION_GUIDE.md](INTEGRATION_GUIDE.md)** - Full setup & API docs
- **[frontend/INTEGRATION.md](frontend/INTEGRATION.md)** - Frontend specifics
- **[IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md)** - What was built

---

## ✅ Pre-Flight Checklist

Before running:
- [ ] Python 3.x installed
- [ ] Node.js 16+ installed
- [ ] In project root directory
- [ ] Flask installed: `pip install flask flask-cors`
- [ ] Frontend dependencies: `cd frontend && npm install`
- [ ] movie-emotions.ttl exists

---

## 🧪 Test the Integration

### Test 1: Backend Health
```bash
curl http://localhost:5000/api/health
# Expected: {"status": "ok", "message": "..."}
```

### Test 2: Get Emotions
```bash
curl http://localhost:5000/api/emotions
# Expected: {"emotions": ["joy", "sadness", ...]}
```

### Test 3: Get Recommendations
```bash
curl -X POST http://localhost:5000/api/recommend \
  -H "Content-Type: application/json" \
  -d '{"emotion":"joy","intensity":0.8,"count":5}'
# Expected: {"success":true,"recommendations":[...]}
```

### Test 4: Frontend
Open **http://localhost:8080**
1. Click emotion button
2. Adjust slider
3. See movies appear
4. Check network tab (F12)

---

## 🔑 Key Technologies

**Frontend:**
- React + TypeScript
- React Router (routing)
- TanStack React Query (data)
- Axios (HTTP)
- Tailwind CSS (styling)
- shadcn/ui (components)
- Vite (bundler)

**Backend:**
- Flask (API server)
- Flask-CORS (cross-origin)
- RDFLib (RDF handling)
- SPARQL (knowledge base query)

---

## 📦 Installation Checklist

```bash
# Backend dependencies
pip install flask flask-cors
✅ Already done!

# Frontend dependencies
cd frontend
npm install
✅ Ready!

# No other installations needed
```

---

## 🌐 API Response Format

```json
{
  "success": true,
  "emotion": "joy",
  "intensity": 0.8,
  "count": 3,
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
```

---

## 💾 File Size Reference

| File | Lines | Purpose |
|------|-------|---------|
| api_server.py | 271 | Flask API wrapper |
| useRecommendations.ts | 198 | React Query hooks |
| Index.tsx | 241 | Main page |
| NotFound.tsx | 42 | 404 page |

---

## 🎓 Learning Resources

- **React Query docs:** https://tanstack.com/query
- **Flask docs:** https://flask.palletsprojects.com
- **SPARQL guide:** https://www.w3.org/TR/sparql11-query/
- **RDF/Turtle:** https://www.w3.org/TR/turtle/

---

## 📞 Common Commands

```bash
# Install backend deps
pip install flask flask-cors

# Install frontend deps
cd frontend && npm install

# Run backend
cd scripts && python api_server.py

# Run frontend
cd frontend && npm run dev

# Build frontend (production)
cd frontend && npm run build

# Kill process on port
lsof -i :5000  (Mac/Linux)
netstat -ano | findstr :5000 (Windows)
taskkill /PID <PID> /F (Windows)
```

---

## ✨ Status

✅ **All Components Ready**
✅ **Dependencies Installed**
✅ **Documentation Complete**
✅ **Ready to Run**

```
🎬 Start with: start.bat
📖 Read: INTEGRATION_GUIDE.md
🚀 Go to: http://localhost:8080
```

---

**Created:** January 1, 2026
**Status:** Production Ready (Local Development)
**Version:** 1.0
