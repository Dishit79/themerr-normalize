
# Themerr-normalize

Lower and normalize volume of theme songs pulled by [Themerr](https://github.com/LizardByte/Themerr-jellyfin) or [jellyfin plugin themesongs](https://github.com/danieladov/jellyfin-plugin-themesongs) 



## Installation

To install this project 

```bash
  docker run -d \
  --name themerr-normalize \
  -e PUID=1000 \
  -e PGID=1000 \
  -e SLEEP_DURATION=43200 \
  -e MEDIA_PATH=/media \
  -v {MEDIA_PATH}:/media \
  --restart unless-stopped \
  themerr-normalize

```

or use the docker-compose.yml 

```docker-compse
services:
  themerr-normalize:
    image: themerr-normalize
    container_name: themerr-normalize
    environment:
      - SLEEP_DURATION=43200
      - MEDIA_PATH=/media
    volumes:
      - /home/nawaf/Documents/media/:/media
    restart: unless-stopped
```
