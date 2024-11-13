import os
import yt_dlp


def download_videos(video_list, save_folder):
    if not os.path.exists(save_folder):
        os.makedirs(save_folder)

    for idx, video_url in enumerate(video_list):
        output_name = f"video{idx}-yt"
        
        try:
            ydl_opts = {
                'merge_output_format': 'mp4',
                'outtmpl': os.path.join(save_folder, f"{output_name}.mp4")
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([video_url])
                print(f"Downloaded: {output_name}")
        except Exception as e:
            print(f"Failed to download {video_url}: {e}")
