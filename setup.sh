#!/bin/bash
# Setup script for Semantic Movie Recommender on Mac/Linux
# Run this once to install all dependencies

clear
echo "============================================================"
echo "    MOVIE RECOMMENDER - SETUP SCRIPT (Mac/Linux)"
echo "============================================================"
echo ""

# Check Python
echo "Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed"
    echo "Please install Python from https://www.python.org/"
    exit 1
fi

# Check Node.js
echo "Checking Node.js installation..."
if ! command -v node &> /dev/null; then
    echo "ERROR: Node.js is not installed"
    echo "Please install Node.js from https://nodejs.org/"
    exit 1
fi

echo ""
echo "✓ Python and Node.js found"
echo ""

# Install Python dependencies
echo "Installing Python dependencies..."
pip3 install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to install Python dependencies"
    exit 1
fi

echo "✓ Python dependencies installed"
echo ""

# Install frontend dependencies
echo "Installing frontend dependencies..."
cd frontend
npm install
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to install frontend dependencies"
    cd ..
    exit 1
fi
cd ..

echo "✓ Frontend dependencies installed"
echo ""

echo "============================================================"
echo "✓ SETUP COMPLETE!"
echo "============================================================"
echo ""
echo "Next steps:"
echo "1. Run: bash start_all.sh (to start both servers)"
echo "   OR manually start servers:"
echo "   - Terminal 1: cd scripts && python3 api_server.py"
echo "   - Terminal 2: cd frontend && npm run dev"
echo ""
echo "2. Open browser: http://localhost:5173"
echo ""
echo "3. Select an emotion to get movie recommendations!"
echo ""
echo "============================================================"
echo ""
