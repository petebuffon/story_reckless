import sys
import re
from datetime import datetime
import yt_dlp


class Episode():
    def __init__(self, entry):
        self.video_id = entry["id"]
        self.title = entry["title"]
        self.description = entry["description"]
        self.upload = datetime.strptime(entry["upload_date"], "%Y%m%d")
        self.season = re.match(".*Adventure (\d)*", self.title)[1]
        if m := re.match(".*Episode (\d)*", self.title):
            self.episode = m[1]
        elif "Postmortem" in self.title:
            self.episode = "Postmortem"
        elif "Prologue" in self.title:
            self.episode = "Prologue"
        self.latest = (datetime.now() - self.upload).total_seconds() < 86400
    
    def __repr__(self):
        return self.video_id


def get_latest_episode(channel):
    ydl_opts = {
        "playlist_items": "1",
        "quiet": True
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        tmp_dict = ydl.extract_info(channel, False)
    episode = Episode(tmp_dict["entries"][0])
    if episode.latest:
        return episode
    else:
        sys.exit("Episode not uploaded within last 24h.")
    return episode


def download(video_id, download_dir):
    ydl_opts = {
        "outtmpl": download_dir + video_id + ".m4a",
        "format": "bestaudio/best",
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "m4a"
        }]
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download(["https://www.youtube.com/watch?v=" + video_id])
