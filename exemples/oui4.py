# importing YouTube from pytube

import progressbar as progress
from pytube import YouTube


def progress(streams, chunk: bytes, bytes_remaining: int):
    contentsize = video.filesize
    size = contentsize - bytes_remaining

    print('\r' + '[Download progress]:[%s%s]%.2f%%;' % (
    '█' * int(size*20/contentsize), ' '*(20-int(size*20/contentsize)), float(size/contentsize*100)), end='')


url = 'https://www.youtube.com/watch?v=Om9y6jW8SPo'
yt = YouTube(url, on_progress_callback=progress)
video = yt.streams.get_highest_resolution()
video.download()