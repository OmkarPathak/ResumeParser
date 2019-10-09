FROM python:3.6

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# set work directory
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

# copy requirements.txt file
COPY requirements.txt requirements.txt

# install all the requirements
RUN pip install --no-cache-dir -r requirements.txt

# copy entire source code
COPY . .

# install dependencies and migrate django code
RUN python pre_requisites.py
RUN python manage.py makemigrations
RUN python manage.py migrate
# RUN python manage.py collectstatic --no-input

# default command to execute    
CMD exec gunicorn resume_parser.wsgi:application --bind 0.0.0.0:8000 --workers 3


# For running this as single Dockerfile:
# docker build -t django_application_image .