from downloader import get_latest_episode, download
from normalizer import loudnorm
from uploader import anchor_upload


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


channel = "https://www.youtube.com/channel/UC3b1prOA-wTLQ5EFJEqQh-A"
download_dir = "/tmp/"

episode = get_latest_episode(channel)
download(episode.video_id, download_dir)
norm(episode, episode.video_id + ".m4a", download_dir)
upload(episode, episode.video_id + "_norm.m4a", download_dir)
