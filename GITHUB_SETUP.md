# GitHub Setup Instructions

## For Repository Maintainers

Follow these steps to push this project to GitHub for your friends to use.

---

## Step 1: Create a GitHub Repository

1. Go to https://github.com/new
2. Enter Repository name: `Semantic-Movie-Recommender`
3. Add description: "Emotion-based movie recommender using semantic web & SPARQL"
4. Choose Public (so anyone can see it)
5. Do NOT initialize with README (we already have one)
6. Click "Create Repository"

---

## Step 2: Initialize Git (First Time Only)

From the project root directory:

```bash
git init
git add .
git commit -m "Initial commit: Emotion-based movie recommender"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/Semantic-Movie-Recommender.git
git push -u origin main
```

Replace `YOUR_USERNAME` with your actual GitHub username.

---

## Step 3: Share with Friends

Give your friends this link:
```
https://github.com/YOUR_USERNAME/Semantic-Movie-Recommender
```

---

## For Friends Downloading the Project

### Step 1: Clone Repository
```bash
git clone https://github.com/YOUR_USERNAME/Semantic-Movie-Recommender.git
cd Semantic-Movie-Recommender
```

### Step 2: Run Setup (Choose Your OS)

**On Windows:**
```bash
setup.bat
```

**On Mac/Linux:**
```bash
bash setup.sh
```

This will automatically install all Python and Node.js dependencies.

### Step 3: Start the Application

**Option A: Automatic (Recommended)**

Windows:
```bash
start_all.bat
```

Mac/Linux:
```bash
bash start_all.sh
```

**Option B: Manual (Two Terminals)**

Terminal 1:
```bash
cd scripts
python api_server.py
```

Terminal 2:
```bash
cd frontend
npm run dev
```

### Step 4: Open in Browser

Visit: **http://localhost:5173**

Done! 🎉

---

## What Files Are Included?

✅ **Complete Source Code**
- Backend (Flask API + recommendation engine)
- Frontend (React + TypeScript)
- Knowledge base (RDF/Turtle)

✅ **Setup Scripts**
- `setup.bat` - Windows setup
- `setup.sh` - Mac/Linux setup
- `start_all.bat` - Windows quick start
- `start_all.sh` - Mac/Linux quick start

✅ **Documentation**
- `README.md` - Main documentation
- `requirements.txt` - Python dependencies
- `frontend/package.json` - Node dependencies

✅ **Configuration**
- `.gitignore` - Git exclusions
- All necessary config files

---

## Troubleshooting for Friends

If they have issues:

1. **Python not found**
   - Install from https://www.python.org/
   - Make sure to check "Add Python to PATH" during installation

2. **Node.js not found**
   - Install from https://nodejs.org/
   - Latest LTS version is recommended

3. **Port already in use**
   - Kill existing processes:
     - Windows: `taskkill /F /IM python.exe /IM node.exe`
     - Mac/Linux: `lsof -ti:5000,5173 | xargs kill -9`

4. **Dependencies won't install**
   - Clear cache: `pip cache purge` (Python) or `npm cache clean --force` (Node)
   - Try again: `pip install -r requirements.txt` or `npm install`

5. **More help**
   - Check `README.md` in the repository
   - Check `QUICK_REFERENCE.md` for common commands
   - Check `INTEGRATION_GUIDE.md` for detailed setup

---

## Making Updates

When you update the code:

```bash
git add .
git commit -m "Description of changes"
git push origin main
```

Your friends can get updates by running:
```bash
git pull
```

---

## Best Practices

1. **Don't commit node_modules or __pycache__**
   - These are excluded in `.gitignore`
   - Friends will install them with `npm install` and `pip install`

2. **Keep README.md updated**
   - Update it when you make major changes
   - Make sure it matches current setup

3. **Use meaningful commit messages**
   - "Fixed movie deduplication" ✅
   - "Updates" ❌

4. **Create branches for new features**
   ```bash
   git checkout -b feature/my-feature
   # Make changes
   git push origin feature/my-feature
   # Create Pull Request on GitHub
   ```

---

## Summary for Friends

Your friend needs to:

1. **Clone:** `git clone <repo-url>`
2. **Setup:** Run `setup.bat` (Windows) or `bash setup.sh` (Mac/Linux)
3. **Start:** Run `start_all.bat` (Windows) or `bash start_all.sh` (Mac/Linux)
4. **Open:** Visit http://localhost:5173
5. **Enjoy:** Select emotions and get movie recommendations! 🎬🍿

That's it!

---

**Questions?** Check the README.md or QUICK_REFERENCE.md in the repository.
