#!/bin/bash
# Start the AI Influencer Platform

cd "$(dirname "$0")"

echo "🚀 Starting AI Influencer Platform..."
echo ""

# Kill any existing server
lsof -ti:5001 | xargs kill -9 2>/dev/null
pkill -f "python.*simple_server" 2>/dev/null
sleep 2

# Start server
echo "📡 Starting server on port 5001..."
python3 simple_server.py


