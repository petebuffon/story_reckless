
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
        if m := re.match(".*Episode (\d)", self.title):
            episode = m[1]
        elif "Postmortem" in self.title:
            self.episode = "Postmortem"
        self.latest = (datetime.now() - self.upload).seconds > 86400
    
    def __repr__(self):
        return self.video_id


def get_latest_episode(channel):
    ydl_opts = {
        "playlist_items": 1
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        tmp_dict = ydl.extract_info(channel, False)
    episode = Episode(tmp_dict)
    # if episode.latest:
    #     return episode
    return episode


channel = "https://www.youtube.com/channel/UC3b1prOA-wTLQ5EFJEqQh-A"

episode = get_latest_episode(channel)
print(episode.title)
print(episode.latest)
