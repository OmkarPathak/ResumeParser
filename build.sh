#!/usr/bin/env bash
# exit on error
set -o errexit

# Install dependencies
pip install -r resume_parser/requirements.txt
pip install ./pyresparser

# Download NLTK data
# Download NLTK data to local directory
# Download NLTK data to local directory
python -m nltk.downloader stopwords -d resume_parser/nltk_data
python -m nltk.downloader punkt -d resume_parser/nltk_data
python -m nltk.downloader wordnet -d resume_parser/nltk_data
python -m nltk.downloader maxent_ne_chunker -d resume_parser/nltk_data
python -m nltk.downloader words -d resume_parser/nltk_data
python -m nltk.downloader averaged_perceptron_tagger -d resume_parser/nltk_data

# Collect static files
python resume_parser/manage.py collectstatic --no-input

# Migration
python resume_parser/manage.py migrate
