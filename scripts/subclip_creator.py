import os
import moviepy.editor as mp
from pathlib import Path


def create_subclips(video_paths, output_folder, subclip_duration):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for video_path in video_paths:
        try:
            video = mp.VideoFileClip(str(video_path))  # Convert PosixPath to string
            video_filename = os.path.basename(str(video_path))
            video_name, _ = os.path.splitext(video_filename)

            num_subclips = int(video.duration // subclip_duration)

            for i in range(num_subclips):
                start_time = i * subclip_duration
                end_time = start_time + subclip_duration
                subclip = video.subclip(start_time, end_time)

                output_filename = f"{video_name}_subclip_{i+1}.mp4"
                output_path = os.path.join(output_folder, output_filename)

                subclip.write_videofile(output_path, codec="libx264", preset="slow", bitrate="5000k", audio_codec="aac")

            print(f"Subclips created successfully for video: {video_filename}")
        except Exception as e:
            print(f"Error processing video {video_path}: {e}")


videos_dir = Path("videos")
video_input_dir = videos_dir / "input_videos"
video_files = list(video_input_dir.glob("*.mp4"))
selected_video = video_files[1]
print(f"Selected video: {selected_video}")

video_list = [selected_video]
output_directory = "output_subclips"
clip_duration = 60

create_subclips(video_list, output_directory, clip_duration)
