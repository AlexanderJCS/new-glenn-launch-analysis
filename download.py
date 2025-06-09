from yt_dlp import YoutubeDL
from moviepy import VideoFileClip


def download():
    ydl_opts = {
        'outtmpl': 'new_glenn.%(ext)s',
        # e.g. 'format': 'bestvideo+bestaudio'
    }
    with YoutubeDL(ydl_opts) as ydl:
        ydl.download(['https://www.youtube.com/watch?v=7ejffAN0Eoc'])

    # load your downloaded file
    clip = VideoFileClip("new_glenn.mp4")

    # subclip(start, end) — use None to go to the end
    trimmed = clip.subclipped(47, 14 * 60 + 38)  # Clip from 00:47 to 14:38

    # write out (this will re-encode)
    trimmed.write_videofile(
        "new_glenn_clipped.mp4",
        codec="libx264",
        audio_codec="aac",
        temp_audiofile="temp-audio.m4a",
        remove_temp=True
    )
