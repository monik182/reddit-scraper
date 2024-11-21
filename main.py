import json
import random
from pathlib import Path
from scripts.youtube_video_downloader import download_videos
from scripts.profanity_censor import censor_profanities
from scripts.generate_audio import generate_audio
from scripts.generate_thumbnail import generate_thumbnail
from scripts.generate_video import generate_video
from scripts.generate_cc import generate_cc
from scripts.youtube_metadata import generate_youtube_metadata
from scripts.scrape_bulk import scrape_long_posts
from scripts.youtube_upload import upload_video
from dotenv import load_dotenv
import argparse

load_dotenv()


root_dir = Path(".")
logs_dir = Path("logs")
output_dir = Path("output")
resources_dir = Path("resources")
videos_dir = Path("videos")

output_dir.mkdir(exist_ok=True)

reddit_output_dir = Path("output_reddit_posts")
thumbnail_output_dir = Path("output_thumbnails")

video_input_dir = videos_dir / "input_videos"
template_image = resources_dir / "template_image.png"
video_log_file = logs_dir / "generated_videos_log.txt"


def load_logged_video_ids():
    if not video_log_file.exists():
        print("---------------> No video log file found.")
        return set()
    with open(video_log_file, "r", encoding="utf-8") as log:
        print("---------------> Loading video log file.")
        return set(line.split("|")[1].strip() for line in log.readlines())


def log_generated_video(post_id, video_path):
    if not video_log_file.exists():
        print("---------------> No generated video log file found.")
        return set()
    with open(video_log_file, "a", encoding="utf-8") as log:
        print(f"---------------> Logging generated video: {post_id}")
        log.write(f"{post_id} | {video_path}\n")


def main(subreddit_name, short=False):
    logged_video_ids = load_logged_video_ids()

    scraped_posts = list(reddit_output_dir.glob("*.json"))

    posts_without_videos = [post for post in scraped_posts if post.stem not in logged_video_ids and subreddit_name in post.stem]

    if not posts_without_videos:
        scrape_long_posts(subreddit_name, limit=10)
        scraped_posts = list(reddit_output_dir.glob("*.json"))
        posts_without_videos = [post for post in scraped_posts if post.stem not in logged_video_ids]
        print(f"0. ----------- Scraped {len(posts_without_videos)} new posts. -----------")

    selected_post = random.choice(posts_without_videos)
    post_id = selected_post.stem
    print(f"1. ----------- Selected post: {subreddit_name}/{selected_post}/{post_id} -----------")
    output_folder = output_dir / post_id
    output_folder.mkdir(exist_ok=True)

    audio_path = output_folder / f"{post_id}.mp3"
    with open(selected_post, "r", encoding="utf-8") as file:
        post_data = json.load(file)
        title = post_data.get("title", "")
        content = post_data.get("selftext", "")
        full_text = title + "\n" + content
        censored_title = censor_profanities(title)
        censored_content = censor_profanities(content)
        full_text = censored_title + "\n" + censored_content
        print(f"2. ----------- Generating audio for post: {post_id} -----------")
        speed = 1.0
        if short:
            speed = 1.4
        generate_audio(full_text, str(audio_path), speed=speed)

    print(f"3. ----------- Generating CC for post: {post_id} -----------")
    cc_path = generate_cc(str(audio_path))

    video_files = list(video_input_dir.glob("*.mp4"))
    if not video_files:
        print("No video files found in the video folder, downloading a YouTube video...")
        download_videos(['https://www.youtube.com/watch?v=u7kdVe8q5zs'], video_input_dir)
        video_files = list(video_input_dir.glob("*.mp4"))
    selected_video = random.choice(video_files)
    print(f"4. ----------- Selected video from {video_input_dir}: {len(video_files)} | {selected_video} -----------")

    print("5. ----------- Generate Thumbnail -----------")
    thumbnail_output_path = output_folder / f"{post_id}_thumbnail.png"
    generate_thumbnail(censored_title, template_image, str(thumbnail_output_path))

    print("6. ----------- Generate metadata -----------")
    metadata_path = output_folder / f"{post_id}_metadata.json"
    metadata = generate_youtube_metadata(selected_post, metadata_path)

    print(f"7. ----------- Generating video for post: {post_id} -----------")
    output_video_path = output_folder / f"{post_id}_final_video.mp4"
    generate_video(str(selected_video), str(audio_path), str(output_video_path), str(cc_path), short)

    print(f"8. ----------- Logging generated video: {post_id} -----------")
    log_generated_video(post_id, str(output_video_path))

    print(f"9. ----------- Upload generated video to YouTube: {post_id} -----------")
    metadata = json.loads(metadata_path.read_text())
    tags = metadata.get("tags", [])
    description = f"{metadata.get('summary', '')} \n\n{', '.join([f'#{tag}' for tag in tags])}"
    upload_video(output_video_path, censored_title, description, tags, str(thumbnail_output_path), short=short)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run the main video generation pipeline.")
    parser.add_argument("subreddit_name", type=str, help="The name of the subreddit to scrape posts from.")
    parser.add_argument("--short", action="store_true", help="Flag to indicate if the video should be uploaded as a YouTube Short.")
    args = parser.parse_args()
    print("short", args.short)
    subreddit_name = args.subreddit_name
    subreddits = ['MaliciousCompliance', 'AmItheAsshole', 'FamilySecrets']

    if args.subreddit_name == 'random':
        subreddit_name = random.choice(subreddits)

    print(f"Generating video for subreddit: {subreddit_name}")
    main(subreddit_name=subreddit_name, short=args.short)
