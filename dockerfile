FROM python:3.9-alpine

WORKDIR /app

COPY . /app

RUN apk add ffmpeg
RUN pip install -r requirements.txt

ENV MEDIA_PATH= \
 SLEEP_DURATION=43200


CMD ["python", "main.py"]