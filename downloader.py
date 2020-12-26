from pytube import YouTube
import re

class Downloader:
    song = 0
    title = "Unknown Song"
    author = "Unknown Author"

    def __init__(self,src):
        yt = YouTube(src)
        if yt is None:
            raise Exception("The audio can't be found")
        self.song = yt.streams.filter(only_audio=True).first().download()
        self.title = yt.title or self.title
        self.author = yt.author or self.author
        if self.song is None:
            raise Exception("The audio can't be downloaded")
        self.extract_author_n_title()

    def extract_author_n_title(self):
        pattern = "(.*)-(.*)"
        matchObject = re.match(pattern,self.title)
        if matchObject is not None:
            self.author =  matchObject.group(1).rstrip() or self.author
            self.title = matchObject.group(2).strip() or self.title
