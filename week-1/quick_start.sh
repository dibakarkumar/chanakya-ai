#!/bin/bash

# Chanakya Week 1 Quick Start Script
# Run this after Python, Git, and Ollama are installed

echo "🚀 Chanakya Week 1 Quick Start"
echo "================================"
echo ""

# Check Python
echo "Checking Python..."
python --version || { echo "❌ Python not found"; exit 1; }

# Install pip packages for Week 1
echo ""
echo "Installing Python packages..."
pip install -r requirements.txt

echo ""
echo "Downloading Ollama models..."
echo "This will take 5-10 minutes..."
ollama pull llama3.2
ollama pull llama3.1:8b

echo ""
echo "Starting Ollama server..."
ollama serve &
OLLAMA_PID=$!

sleep 5

echo ""
echo "Installing Open WebUI..."
pip install open-webui

echo ""
echo "Starting Open WebUI on localhost:8080..."
echo "Opening browser..."
open-webui serve &

sleep 3

echo ""
echo "✅ Setup complete!"
echo ""
echo "Open your browser: http://localhost:8080"
echo "Select model: llama3.2"
echo "Start chatting with Chanakya!"
echo ""
echo "Press Ctrl+C to stop"
