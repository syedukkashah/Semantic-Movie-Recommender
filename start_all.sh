#!/bin/bash
# Quick Start Script for Movie Recommender (Mac/Linux)
# Starts both Frontend and Backend servers

clear
echo ""
echo "============================================================"
echo "    MOVIE RECOMMENDER - QUICK START (Mac/Linux)"
echo "============================================================"
echo ""

# Check if we're in the right directory
if [ ! -f "scripts/api_server.py" ]; then
    echo "ERROR: api_server.py not found!"
    echo "Please run this script from the project root directory."
    exit 1
fi

if [ ! -f "frontend/package.json" ]; then
    echo "ERROR: frontend/package.json not found!"
    echo "Please run this script from the project root directory."
    exit 1
fi

echo "✓ Project files found"
echo ""
echo "Starting servers..."
echo ""

# Start backend
echo "1. Starting Backend API Server (Port 5000)..."
cd scripts
python3 api_server.py &
BACKEND_PID=$!
cd ..

sleep 3

# Start frontend
echo ""
echo "2. Starting Frontend Development Server (Port 5173)..."
cd frontend
npm run dev &
FRONTEND_PID=$!
cd ..

sleep 2

echo ""
echo "============================================================"
echo "✓ Both servers are starting!"
echo ""
echo "Frontend:  http://localhost:5173"
echo "Backend:   http://localhost:5000"
echo ""
echo "Check the console output above for startup messages."
echo "Press Ctrl+C to stop both servers."
echo "============================================================"
echo ""

# Open browser (Mac specific)
if [[ "$OSTYPE" == "darwin"* ]]; then
    sleep 2
    open http://localhost:5173
fi

echo "Enjoy emotion-based movie recommendations! 🍿"
echo ""

# Wait for both processes
wait $BACKEND_PID $FRONTEND_PID
