#!/bin/bash
# Start the AI Influencer Recommendation Platform

echo "🚀 Starting AI Influencer Recommendation Platform..."
echo ""

# Check if .env exists
if [ ! -f .env ]; then
    echo "⚠️  .env file not found. Creating from .env.example..."
    cp .env.example .env
    echo "📝 Please edit .env and add your OPENAI_API_KEY"
    echo ""
fi

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt --quiet

# Start the server
echo ""
echo "✅ Starting server..."
echo "🌐 API: http://localhost:5000"
echo "📊 Frontend: Open frontend/index.html in browser"
echo ""
python app.py

