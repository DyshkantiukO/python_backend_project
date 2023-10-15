FROM python:3.11.1-slim-bullseye


WORKDIR /app


COPY requirements.txt .


RUN python -m pip install -r requirements.txt


COPY . /app


CMD flask --app myapplication run -h 0.0.0.0 -p $PORT
