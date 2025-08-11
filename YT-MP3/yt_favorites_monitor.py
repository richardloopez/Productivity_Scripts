import os
import time
from yt_dlp import YoutubeDL
import json

# ====================== CONFIG ======================

with open('ytmp3_config.json', 'r', encoding='utf-8') as f:
    config = json.load(f)

FAVORITES_URL = config['FAVORITES']['url']
DESTINATION_FOLDER = config['PATHS']['destination_folder']
FFMPEG_LOCATION = config['PATHS']['ffmpeg_location']
INTERVAL_MINUTES = int(config['SETTINGS']['interval_minutes'])
SESSION_GROUP_ID = config['SETTINGS']['session_group_id']
HISTORY_FILE = f"{SESSION_GROUP_ID}_downloaded.txt"
FAILED_FILE = f"{SESSION_GROUP_ID}_failed.txt"

MAX_RETRIES = 10

# ====================== FUNCTIONS ======================

def load_list(file_path):
    """Load IDs from a file into a set."""
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            return set(line.strip() for line in f.readlines())
    return set()

def save_to_file(file_path, video_id):
    """Append a video ID to a file."""
    with open(file_path, "a", encoding="utf-8") as f:
        f.write(f"{video_id}\n")

def count_downloaded_files():
    """Count the number of already downloaded videos to get the next index."""
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            lines = f.readlines()
            return len(lines) + 1
    else:
        return 1

def get_new_videos():
    """Fetch the list of videos from the YouTube playlist."""
    ydl_opts = {
        'quiet': True,
        'extract_flat': True,
        'force_generic_extractor': True,
    }

    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(FAVORITES_URL, download=False)
        entries = info.get("entries", [])
        entries.reverse()  # Oldest first
        return [(entry['id'], entry['title']) for entry in entries]

def download_audio(video_id, file_number):
    """Download a single video's audio as MP3."""
    url = f"https://www.youtube.com/watch?v={video_id}"
    ydl_opts = {
        'format': 'bestaudio/best',
        "outtmpl" : os.path.join(DESTINATION_FOLDER, f"{SESSION_GROUP_ID}{file_number}#%(title)s.%(ext)s"),
        'ffmpeg_location': FFMPEG_LOCATION,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '320',
        }],
        'quiet': False,
    }

    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

# ====================== MAIN ======================

def main():
    print("Starting YouTube favorites monitor...")

    downloaded = load_list(HISTORY_FILE)
    failed = load_list(FAILED_FILE)

    while True:
        try:
            new_videos = get_new_videos()
            for video_id, title in new_videos:
                if video_id in downloaded:
                    continue
                if video_id in failed:
                    continue

                print(f"New video: {title}")
                file_number = count_downloaded_files()
                print(f"Downloading file number: {file_number}")

                success = False
                for attempt in range(1, MAX_RETRIES + 1):
                    try:
                        print(f"Attempt {attempt}/{MAX_RETRIES} for video: {title}")
                        download_audio(video_id, file_number)
                        save_to_file(HISTORY_FILE, video_id)
                        downloaded.add(video_id)
                        success = True
                        print(f"Downloaded successfully: {title}")
                        break
                    except Exception as e:
                        print(f"Attempt {attempt} failed: {e}")
                        time.sleep(2)  # optional delay

                if not success:
                    print(f"Giving up on: {title}")
                    save_to_file(FAILED_FILE, video_id)
                    failed.add(video_id)

            print(f"Waiting {INTERVAL_MINUTES} minutes...")
        except Exception as e:
            print(f"Error: {e}")

        time.sleep(INTERVAL_MINUTES * 60)

if __name__ == "__main__":
    main()
