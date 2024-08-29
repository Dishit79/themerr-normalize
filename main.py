import os
import json
import subprocess
import datetime
import time
import logging

import dotenv
from dotenv import load_dotenv

load_dotenv()
logging.basicConfig(level=logging.INFO)

def get_media_files_from_settings():
    """
    Reads the .env file and returns a list of all directories
    specified in the MEDIA_PATH setting.
    """
    media_paths = []
    for media_path in os.environ.get('MEDIA_PATH').split(','):
        media_paths.append(media_path)
    return media_paths


def enumerate_through_media_paths(media_paths):
    """
    search through all media directories and normalize all
    theme files.
    """
    theme_files = []

    for path in media_paths:

        for root, dirnames, filenames in os.walk(path):

            for filename in filenames:
                if filename.endswith('theme.mp3'):
                    # Check if the directory has already been normalized
                    # by checking for the existence of the
                    # themerr-normalize.json file.
                    if check_if_normalized(root):

                        logtxt = f'{root} already normalized'
                        logging.info(logtxt)
                        continue
                    else:
                        normalize_theme_files(root)

def check_if_normalized(path):
    """
    Checks if a directory has already been normalized by
    looking for the existence of the themerr-normalize.json
    file. If it exists, returns True, otherwise False.

    Args:
        path (str): The path to the directory to check

    Returns:
        bool: Whether the directory has been normalized
    """
    # Check if the directory has already been normalized
    # by looking for the existence of the
    # themerr-normalize.json file.
    if os.path.exists(os.path.join(path, 'themerr-normalize.json')):
        return True
    return False

def normalize_theme_files(path):
    """
    Normalizes the theme.mp3 file in the given directory by
    calling normalize_audio() and then stamping the directory
    with a themerr-normalize.json file.

    Args:
        path (str): The path to the directory to normalize
    """

    logtxt = f'normalizing {path}'
    logging.info(logtxt)

    # Normalize the theme.mp3 file
    normalize_audio(os.path.join(path, 'theme.mp3'))

    # Stamp the directory with a themerr-normalize.json file
    stamp_audio(path)
   

def normalize_audio(path):
    """
    Normalizes the volume of an MP3 file using ffmpeg-normalize.

    Args:
        path (str): The path to the MP3 file to normalize

    Returns:
        None
    """
    # Rename the file to add '_orig' to the end of the filename
    renamed_path = path.replace('.mp3', '_orig.mp3')
    os.rename(path, renamed_path)

    # Run the ffmpeg-normalize command
    subprocess.run([
        "ffmpeg-normalize", renamed_path,
        "-o", path,
        "-c:a", "libmp3lame",  # Specify the MP3 codec
        "-nt", "ebu",          # Use EBU R128 normalization
        "-t", "-24",           # Target loudness level in LUFS
        "-lrt", "11",          # Set a higher loudness range target
        "--keep-loudness-range-target",  # Keep the target loudness range
        "-ar", "44100",        # Set the output sample rate
        "-b:a", "192k"         # Set the output bitrate
    ])

    # Delete the original file
    os.remove(renamed_path)
    logtxt = f'Normalized {path}'
    logging.info(logtxt)

def stamp_audio(path):
    """
    Stamps the given directory with a themerr-normalize.json file
    that contains the time at which the directory was normalized.

    Args:
        path (str): The path to the directory to stamp
    """
    # Create the themerr-normalize.json file
    with open(os.path.join(path, 'themerr-normalize.json'), 'w') as f:
        # Dump the current timestamp to the file
        json.dump({"normalized_at": datetime.datetime.now().isoformat()}, f)


def main():
    """
    The main entry point for the script.

    This function reads the .env file to get the list of directories
    to normalize, and then calls enumerate_through_media_paths()
    to normalize the theme files in each directory.
    """
    media_paths = get_media_files_from_settings()
    enumerate_through_media_paths(media_paths)


while True:
    main()
    sleep_timer = os.environ.get('SLEEP_DURATION')
    logtxt = f'Sleeping for {sleep_timer} seconds'
    logging.info(logtxt)
    time.sleep(int(sleep_timer))
