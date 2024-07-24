import pathlib
from pytube import YouTube
src = "https://youtube.com/watch?v=mkmWERwd_KE"

yt = YouTube(src)
if yt is None:
    raise Exception("The audio can't be found")

song = yt.streams.filter(only_audio=True).first().download()