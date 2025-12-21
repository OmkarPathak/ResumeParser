#!/bin/bash

# Get the directory where the script is located
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$DIR"

# Set executable permission for the binary just in case
chmod +x "ResumeParser"

echo "Starting Portable Resume Parser..."
echo "Please wait while the server initializes..."

# Open the browser automatically after 10 seconds (in the background)
(sleep 30 && open "http://127.0.0.1:8000") &
echo "Browser will open in 30 seconds..."

# Run the portable application
./ResumeParser runserver
