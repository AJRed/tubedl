# from ffmpeg import FFmpeg


# class Converter:
    # def __init__(self):
        # mpg = (FFmpeg()
               # .option("y")
               # .input("input.mp4")
               # .output(
            # "output.mp4",
            # {"codec:v": "libx264"},
            # vf="scale=1280:-1",
            # preset="veryslow",
            # crf=24,
        # )
        # )

        # mpg.execute()

import os

PATH = os.getcwd()
SRC_PATH = "../new_videos/"

strip_chars = ["＂", "\"", ":", "："]

if __name__ == "__main__":
    videos = os.listdir(SRC_PATH)
    names = []
    for video_name in videos:
        suffix = video_name[::-1].find("[")
        name = video_name[:len(video_name) - suffix - 1]
        for c in strip_chars:
            name = name.replace(c, '')
        name = name.rstrip()
        video_path = f"{SRC_PATH}{video_name}"
        command = f"./extract_single.sh \"{video_path}\" \"{name}.mp3\""
        os.system(command)
