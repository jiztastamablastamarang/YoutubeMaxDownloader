"""
Download and combine the highest quality video with audio from YouTube
"""
import os
import glob
import shutil
from pytube import YouTube
from moviepy.editor import VideoFileClip, AudioFileClip


class YoutubeVideo:
    """Main class"""

    def __init__(self, url, path):
        self.object = YouTube(url)
        self.path = path
        self.tmp_path = os.path.join(os.getcwd(), "tmp")
        self.media = dict(audio=None, video=None)
        self.set_file_tags()
        self.download()
        self.composite()

    def set_file_tags(self) -> None:
        """define which media files to combine"""
        streams = self.object.streams
        for file_type in self.media:
            params = {
                f"only_{file_type}": True,
                "type": file_type,
                "progressive": False
            }
            order = "resolution" if file_type == "video" else "filesize"
            self.media[file_type] = streams.filter(**params).order_by(order).last()
            print(self.media[file_type])

    def download(self) -> None:
        """download files to tmp dir"""
        if not os.path.exists(self.tmp_path):
            os.mkdir(self.tmp_path)
        for key, stream in self.media.items():
            if not stream:
                raise FileNotFoundError(f"File with {key}")
            stream.download(output_path=self.tmp_path,
                            filename=key)
            print(f"{key} file downloaded successfully.")

    def composite(self) -> None:
        """combine audio and video"""
        files = glob.glob(self.tmp_path + "/*")
        getFile = lambda file_type: next((f for f in files if f.count(file_type)))
        audio = AudioFileClip(getFile("audio"))
        video = VideoFileClip(getFile("video"))
        result = video.set_audio(audio)
        print("adhesion done.")
        if not os.path.exists(self.path):
            os.mkdir(self.path)
        os.chdir(self.path)
        result.write_videofile(filename="result.mp4")
        result.close()
        shutil.rmtree(self.tmp_path)
        print("done!")


if __name__ == "__main__":
    URL = input("enter YouTube video link.")
    PATH = input("enter destination path.")
    youtube = YoutubeVideo(URL, PATH)
