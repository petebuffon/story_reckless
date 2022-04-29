import xml.etree.ElementTree as ET
from collections import deque
import requests

from downloader import get_episode, download
from normalizer import loudnorm
from uploader import anchor_upload


def get_titles(url):
    r = requests.get(url)
    root = ET.fromstring(r.content)
    titles = set()
    for title in root.findall("./channel/item/title"):
        titles.add(title.text)
    return titles
    

def norm(episode, filename, download_dir):
    input_path = download_dir + filename
    output_path = download_dir + episode.video_id + "_norm.m4a"
    loudnorm(input_path, output_path)


def upload(episode, filename, download_dir):
    input_path = download_dir + filename
    try:
        anchor_upload(episode, input_path)
    except Exception as e:
        print(e, " , upload failed.")


rss_url = "https://anchor.fm/s/6a41bc24/podcast/rss"
channel = "https://www.youtube.com/channel/UC3b1prOA-wTLQ5EFJEqQh-A"
download_dir = "/tmp/"

titles = get_titles(rss_url)
episodes = deque()
playlist_item = 1

while True:
    episode = get_episode(channel, playlist_item)
    if episode.title in titles:
        print(f"{episode.title} already uploaded...")
        break
    else:
        playlist_item += 1
        episodes.append(episode)

while episodes:
    episode = episodes.popleft()
    download(episode.video_id, download_dir)
    norm(episode, episode.video_id + ".m4a", download_dir)
    upload(episode, episode.video_id + "_norm.m4a", download_dir)

