from pytubefix import YouTube
from pytubefix.cli import on_progress

from proxy.proxy import setup_proxy


def download_video(url):
    """
    Скачивает видео с YouTube в максимальном доступном разрешении.
    
    Функция настраивает прокси, подключается к YouTube с использованием OAuth,
    получает поток видео в наивысшем разрешении и скачивает его в указанную директорию.
    
    :param url: Ссылка на видео YouTube
    """
    setup_proxy()

    yt = YouTube(url, on_progress_callback=on_progress, use_oauth=True, allow_oauth_cache=True)
    print(yt.title)

    ys = yt.streams.get_highest_resolution()
    ys.download(output_path='downloaded_videos', max_retries=10)
