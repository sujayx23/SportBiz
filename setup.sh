#!/bin/bash

# SportStore AI Setup Script
# This script sets up the SportStore AI project with all dependencies

echo "🚀 Setting up SportStore AI - Intelligent Sports Business Assistant"
echo "================================================================"

# Check if Python 3.8+ is installed
python_version=$(python3 --version 2>&1 | awk '{print $2}' | cut -d. -f1,2)
required_version="3.8"

if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" != "$required_version" ]; then
    echo "❌ Error: Python 3.8 or higher is required. Current version: $python_version"
    exit 1
fi

echo "✅ Python version check passed: $python_version"

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "⬆️ Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "📚 Installing dependencies..."
pip install -r requirements.txt

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "🔑 Creating .env file..."
    cp env_example.txt .env
    echo "⚠️  Please edit .env file and add your OpenAI API key"
    echo "   You can get one at: https://platform.openai.com/api-keys"
fi

# Create necessary directories
echo "📁 Creating project directories..."
mkdir -p agents tools data memory ui

# Make test script executable
chmod +x test_enhanced_features.py

echo ""
echo "🎉 Setup completed successfully!"
echo ""
echo "📋 Next steps:"
echo "1. Edit .env file and add your OpenAI API key"
echo "2. Activate virtual environment: source venv/bin/activate"
echo "3. Run the application: streamlit run main.py"
echo "4. Test the features: python test_enhanced_features.py"
echo ""
echo "🔗 Useful commands:"
echo "   streamlit run main.py          # Start the application"
echo "   python test_enhanced_features.py  # Run tests"
echo "   source venv/bin/activate       # Activate virtual environment"
echo "   deactivate                     # Deactivate virtual environment"
echo ""
echo "📖 Documentation: README.md"
echo "📊 Project Summary: PROJECT_SUMMARY.md"
echo ""
echo "✨ SportStore AI is ready to use!" 