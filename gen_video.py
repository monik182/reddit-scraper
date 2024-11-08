import moviepy.editor as mp
from pathlib import Path
import moviepy.audio.fx.all as afx

def replace_audio(video_path, audio_path, output_path):
    video_path = str(video_path)
    audio_path = str(audio_path)
    output_path = str(output_path)

    video = mp.VideoFileClip(video_path)
    new_audio = mp.AudioFileClip(audio_path)
    
    video = video.set_audio(new_audio).set_duration(new_audio.duration)

    # new_audio = new_audio.volumex(1.5)
    new_audio = mp.AudioFileClip(audio_path)
    
    # Normalize the audio volume to ensure it is audible
    new_audio = afx.audio_normalize(new_audio)
    video = video.set_audio(new_audio)
    
    video.write_videofile(output_path, codec='libx264', audio_codec='aac')

def main():
    video_file = Path("output_videos/video1.mp4")
    english_audio_file = Path("en.mp3")
    output_video_file = Path("output_video_with_new_audio.mp4")
    
    replace_audio(video_file, english_audio_file, output_video_file)

if __name__ == "__main__":
    main()
