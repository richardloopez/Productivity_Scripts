import os
import time
from yt_dlp import YoutubeDL
import sys
import json

with open('ytmp3_config.json', 'r', encoding='utf-8') as f:
    config = json.load(f)

FAVORITES_URL = config['FAVORITES']['url']
DESTINATION_FOLDER = config['PATHS']['destination_folder']
FFMPEG_LOCATION = config['PATHS']['ffmpeg_location']
INTERVAL_MINUTES = int(config['SETTINGS']['interval_minutes'])
SESSION_GROUP_ID = config['SETTINGS']['session_group_id']
HISTORY_FILE = f"{SESSION_GROUP_ID}_downloaded.txt"

# ======================

def load_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            return set(line.strip() for line in f.readlines())
    return set()

def count_downloaded_files():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            lines = f.readlines()
            return len(lines) + 1
    else:
        return 1

def save_to_history(video_id):
    with open(HISTORY_FILE, "a", encoding="utf-8") as f:
        f.write(f"{video_id}\n")

def get_new_videos():
    ydl_opts = {
        'quiet': True,
        'extract_flat': True,
        'force_generic_extractor': True,
    }

    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(FAVORITES_URL, download=False)
        entries = info.get("entries", [])
        entries.reverse()  # To get the oldest videos first
        return [(entry['id'], entry['title']) for entry in entries]

def download_audio(video_id, file_number):
    url = f"https://www.youtube.com/watch?v={video_id}"
    ydl_opts = {
        'format': 'bestaudio/best',
        "outtmpl" : os.path.join(DESTINATION_FOLDER, f"{SESSION_GROUP_ID}{file_number}#%(title)s.%(ext)s"),
        'ffmpeg_location': r"E:\T\Programming\Jupyter\Codes\YT-MP3",  # <== CHANGE to your exact path
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '320',
        }],
        'quiet': False,
    }

    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

def main():
    print("Starting YouTube favorites monitor...")
    downloaded = load_history()

    while True:
        try:
            new_videos = get_new_videos()
            for video_id, title in new_videos:
                if video_id not in downloaded:
                    print(f"New video: {title}. Downloading...")
                    file_number = count_downloaded_files()
                    print(f"Downloading file number: {file_number}")
                    download_audio(video_id, file_number)
                    save_to_history(video_id)
                    downloaded.add(video_id)
            print(f"Waiting {INTERVAL_MINUTES} minutes...")
        except Exception as e:
            print(f"Error: {e}")
        time.sleep(INTERVAL_MINUTES * 60)

if __name__ == "__main__":
    main()
