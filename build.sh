#!/usr/bin/env bash
# exit on error
set -o errexit

# Install dependencies
pip install -r resume_parser/requirements.txt
pip install ./pyresparser

# Download NLTK data
# Download NLTK data to local directory
python -m nltk.downloader stopwords -d nltk_data
python -m nltk.downloader punkt -d nltk_data
python -m nltk.downloader wordnet -d nltk_data

# Collect static files
python resume_parser/manage.py collectstatic --no-input

# Migration
python resume_parser/manage.py migrate
