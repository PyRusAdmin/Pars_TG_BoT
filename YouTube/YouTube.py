from pytubefix import YouTube
from pytubefix.cli import on_progress

from proxy.proxy import setup_proxy, password, user, port, ip


def download_video(url):
    setup_proxy(user, password, ip, port)

    yt = YouTube(url, on_progress_callback=on_progress)
    print(yt.title)

    ys = yt.streams.get_highest_resolution()
    ys.download()
