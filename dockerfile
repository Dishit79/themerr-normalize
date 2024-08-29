FROM python:3.9-alpine

WORKDIR /app

COPY . /app

RUN pip install python-dotenv

ENV MEDIA_PATH= \
 SLEEP_DURATION=43200


CMD ["python", "main.py"]