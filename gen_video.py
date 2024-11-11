import os
import moviepy.editor as mp
from pathlib import Path
import moviepy.audio.fx.all as afx
from moviepy.video.tools.subtitles import SubtitlesClip

def format_time(seconds):
    hours, remainder = divmod(int(seconds), 3600)
    minutes, seconds = divmod(remainder, 60)
    milliseconds = int((seconds - int(seconds)) * 1000)
    return f"{hours:02}:{minutes:02}:{int(seconds):02},{milliseconds:03}"


def generator(txt):
    max_chars_per_line = 25
    words = txt.split()
    lines = []
    current_line = []
    current_length = 0

    for word in words:
        if current_length + len(word) + 1 > max_chars_per_line:  # +1 for space
            lines.append(" ".join(current_line))
            current_line = [word]
            current_length = len(word)
        else:
            current_line.append(word)
            current_length += len(word) + 1
    
    lines.append(" ".join(current_line))
    final_text = "\n".join(lines)
    
    return mp.TextClip(
        final_text,
        font='Helvetica-Bold',
        fontsize=70,
        color='white',
        stroke_color='black',
        stroke_width=4,
        align='center',
        kerning=2,
    )


def generate_video(video_path, audio_path, output_path, cc_path = None):
    video_path = str(video_path)
    audio_path = str(audio_path)
    output_path = str(output_path)

    video = mp.VideoFileClip(video_path)

    target_width = 1080
    target_height = 1920

    video = video.resize(height=target_height if video.h < target_height else None, width=target_width if video.w < target_width else None)
    video = video.on_color(size=(target_width, target_height), color=(0, 0, 0), col_opacity=1)

    new_audio = mp.AudioFileClip(audio_path)

    video = video.set_audio(new_audio).set_duration(new_audio.duration)

    new_audio = mp.AudioFileClip(audio_path)

    new_audio = afx.audio_normalize(new_audio)
    video = video.set_audio(new_audio)

    if cc_path:
        subtitles = SubtitlesClip(str(cc_path), generator)
        video = mp.CompositeVideoClip([video, subtitles.set_position(('center', 'center'))])
    elif cc_path is None or os.path.getsize(cc_path) == 0:
        print("Warning: Subtitle file is empty or not created. No subtitles will be added.")
    
    video.write_videofile(output_path, codec='libx264', audio_codec='aac', bitrate='5000k', preset='medium')


def main():
    video_file = Path("output_videos/video1.mp4")
    english_audio_file = Path("en.mp3")
    output_video_file = Path("cropped_output_video_with_new_audio_SUBTITLES_STYLED3.mp4")
    cc_path = Path("en.srt")

    generate_video(video_file, english_audio_file, output_video_file, cc_path)


if __name__ == "__main__":
    main()
