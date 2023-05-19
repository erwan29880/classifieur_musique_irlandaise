FROM python:3.8

WORKDIR /home
RUN apt update
RUN apt install -y ffmpeg
RUN pip install Flask pydub numpy librosa matplotlib opencv-python pandas flask-cors psycopg2-binary pymongo pytest
RUN pip install tensorflow keras

