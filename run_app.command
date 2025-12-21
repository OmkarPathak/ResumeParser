#!/bin/bash

# Get the directory where the script is located
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$DIR/resume_parser"

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "Python 3 could not be found. Please install Python 3 to run this application."
    exit 1
fi

# Create a virtual environment if it doesn't exist
if [ ! -d "env" ]; then
    echo "Creating virtual environment..."
    python3 -m venv env
fi

# Activate the virtual environment
source env/bin/activate

# Install dependencies
if [ -f "requirements.txt" ]; then
    # Check if dependencies are already installed
    if python3 -c "import pyresparser; import spacy" &> /dev/null; then
         echo "Dependencies already installed. Skipping installation."
    else
        echo "Installing dependencies..."
        pip install -r requirements.txt
        
        # Install pyresparser from local source
        echo "Installing local pyresparser..."
        pip install -e ../pyresparser
    fi
fi

# Apply migrations
if [ ! -f "db.sqlite3" ]; then
    echo "Applying database migrations..."
    python manage.py makemigrations
    python manage.py migrate
fi

# Create media directory if it doesn't exist
if [ ! -d "media" ]; then
    mkdir media
fi

# Open the browser automatically after 20 seconds (in the background)
# This allows the server time to start up
(sleep 20 && open "http://127.0.0.1:8000") &
echo "Browser will open in 20 seconds..."

# Run the server
echo "Starting server..."
python manage.py runserver

# Deactivate virtual environment on exit (though script exit handles this)
deactivate
