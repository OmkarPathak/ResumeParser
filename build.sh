#!/usr/bin/env bash
# exit on error
set -o errexit

# Install dependencies
pip install -r resume_parser/requirements.txt
pip install ./pyresparser

# Download NLTK data
python -m nltk.downloader stopwords
python -m nltk.downloader punkt
python -m nltk.downloader wordnet

# Collect static files
python resume_parser/manage.py collectstatic --no-input

# Migration
python resume_parser/manage.py migrate
