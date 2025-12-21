#!/bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$DIR"

echo "Applying fix for macOS Gatekeeper..."
echo "Removing quarantine attributes from all files in this directory..."

# Remove quarantine attributes recursively
xattr -cr .

echo "------------------------------------------------"
echo "✅ Success! The app has been repaired."
echo "You can now run 'run_portable_app.command'."
echo "------------------------------------------------"
echo "You can close this window."
