#!/bin/bash
set -e

# Setup directories
APP_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$APP_DIR/resume_parser"

echo "Building Resume Parser on macOS..."

# 1. Setup Virtual Environment
if [ -d "env" ]; then
    echo "Using existing virtual environment..."
else
    echo "Creating virtual environment..."
    python3 -m venv env
fi

source env/bin/activate

# 2. Install Dependencies
echo "Installing dependencies..."
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
pip install -e ../pyresparser
pip install pyinstaller

# 3. Download NLTK Data locally
echo "Downloading NLTK data..."
mkdir -p nltk_data
python -m nltk.downloader -d nltk_data stopwords punkt punkt_tab wordnet maxent_ne_chunker words averaged_perceptron_tagger averaged_perceptron_tagger_eng

# 4. Cleanup previous builds
rm -rf build dist

# 5. Run PyInstaller
echo "Running PyInstaller..."
pyinstaller ResumeParser.spec --noconfirm

# 6. Post-build Verification
if [ -f "dist/ResumeParser/ResumeParser" ]; then
    echo "Build success! Executable is at resume_parser/dist/ResumeParser/ResumeParser"
else
    echo "Build failed! Executable not found."
    exit 1
fi
