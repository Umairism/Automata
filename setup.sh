#!/bin/bash

echo "🚀 Starting Automata Solver Setup..."

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

echo "✓ Python 3 found"

# Check if Graphviz is installed
if ! command -v dot &> /dev/null; then
    echo "⚠️  Graphviz not found. Installing..."
    
    # Detect OS and install Graphviz
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        sudo apt-get update
        sudo apt-get install -y graphviz
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        brew install graphviz
    else
        echo "❌ Please install Graphviz manually from https://graphviz.org/download/"
        exit 1
    fi
else
    echo "✓ Graphviz found"
fi

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📥 Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Create necessary directories
echo "📁 Creating directories..."
mkdir -p static
mkdir -p templates

echo ""
echo "✅ Setup complete!"
echo ""
echo "To run the application:"
echo "  1. Activate virtual environment: source venv/bin/activate"
echo "  2. Run the app: python app.py"
echo "  3. Open browser: http://localhost:5000"
echo ""
