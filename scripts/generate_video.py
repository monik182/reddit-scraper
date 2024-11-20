import os
import moviepy.editor as mp
from pathlib import Path
import moviepy.audio.fx.all as afx
from moviepy.video.tools.subtitles import SubtitlesClip
import subprocess


SHORTEST_VIDEO_DURATION = 60


def resize_video_ffmpeg(input_path, output_path, target_width, target_height):
    command = [
        "ffmpeg",
        "-i", input_path,
        "-vf", f"scale={target_width}:{target_height}:flags=lanczos",
        "-c:v", "libx264",
        "-crf", "18",  # Lower CRF gives better quality (recommended range is 18-23)
        "-preset", "slow",  # "slow" preset improves quality but takes longer
        output_path
    ]
    subprocess.run(command)


def generator(txt):
    max_chars_per_line = 25
    words = txt.split()
    lines = []
    current_line = []
    current_length = 0

    for word in words:
        if current_length + len(word) + 1 > max_chars_per_line:
            lines.append(" ".join(current_line))
            current_line = [word]
            current_length = len(word)
        else:
            current_line.append(word)
            current_length += len(word) + 1

    lines.append(" ".join(current_line))
    final_text = "\n".join(lines).upper()

    return mp.TextClip(
        final_text,
        font='Arial-Black',
        fontsize=80,
        color='white',
        stroke_color='black',
        stroke_width=5,
        align='center',
        kerning=2,
    )


def generate_video(video_path, audio_path, output_path, cc_path = None, short = False):
    video_path = str(video_path)
    audio_path = str(audio_path)
    output_path = str(output_path)
    target_width = 1080
    target_height = 1920

    video = mp.VideoFileClip(video_path)

    video = video.resize(
        height=target_height if video.h < target_height else video.h,
        width=target_width if video.w < target_width else video.w
    )
    video = video.on_color(size=(target_width, target_height), color=(0, 0, 0), col_opacity=1)

    new_audio = mp.AudioFileClip(audio_path)

    if short:
        duration = min(SHORTEST_VIDEO_DURATION, new_audio.duration)
        new_audio = new_audio.subclip(0, duration)
        video = video.subclip(0, duration)
    else:
        duration = new_audio.duration

    new_audio = new_audio.set_duration(duration).set_duration(duration)
    video = video.set_audio(new_audio).set_duration(duration)

    new_audio = afx.audio_normalize(new_audio)
    video = video.set_audio(new_audio)

    if cc_path:
        subtitles = SubtitlesClip(str(cc_path), generator).set_duration(duration)
        video = mp.CompositeVideoClip([video, subtitles.set_position(('center', 'center'))])
    elif cc_path is None or os.path.getsize(cc_path) == 0:
        print("Warning: Subtitle file is empty or not created. No subtitles will be added.")
    
    video.write_videofile(output_path, codec='libx264', audio_codec='aac', bitrate='5000k', preset='medium')
