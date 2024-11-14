import json
import random
from pathlib import Path
from profanity_censor import censor_profanities
from generate_audio import generate_audio
from generate_thumbnail import generate_thumbnail
from generate_video import generate_video
from scraper import generate_cc
from youtube_metadata import generate_youtube_metadata
from scrape_bulk import scrape_long_posts
from youtube_upload import upload_video
from dotenv import load_dotenv
import argparse

load_dotenv()


output_dir = Path("output")
root_dir = Path(".")
reddit_output_dir = Path("output_reddit_posts")
video_input_dir = Path("output_videos")
thumbnail_output_dir = Path("output_thumbnails")
output_dir.mkdir(exist_ok=True)
video_log_file = root_dir / "generated_videos_log.txt"
template_image = root_dir / "template_image.png"


def load_logged_video_ids():
    if not video_log_file.exists():
        return set()
    with open(video_log_file, "r", encoding="utf-8") as log:
        return set(line.split("|")[1].strip() for line in log.readlines())


def log_generated_video(post_id, video_path):
    with open(video_log_file, "a", encoding="utf-8") as log:
        log.write(f"{post_id} | {video_path}\n")


def main(subreddit_name="learnpython"):
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
    print(f"1. ----------- Selected post: {subreddit_name}/{post_id} -----------")
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
        generate_audio(full_text, str(audio_path))

    print(f"3. ----------- Generating CC for post: {post_id} -----------")
    cc_path = generate_cc(str(audio_path))

    video_files = list(video_input_dir.glob("*.mp4"))
    if not video_files:
        raise FileNotFoundError("No video files found in the video folder.")
    selected_video = random.choice(video_files)
    print(f"4. ----------- Selected video from {video_input_dir}: {len(video_files)} | {selected_video} -----------")


    print("5. ----------- Generate Thumbnail -----------")
    generate_thumbnail(censored_title, template_image, str(output_folder / f"{post_id}_thumbnail.png"))

    print("6. ----------- Generate metadata -----------")
    metadata_path = output_folder / f"{post_id}_metadata.json"
    metadata = generate_youtube_metadata(selected_post, metadata_path)

    print(f"7. ----------- Generating video for post: {post_id} -----------")
    output_video_path = output_folder / f"{post_id}_final_video.mp4"
    generate_video(str(selected_video), str(audio_path), str(output_video_path), str(cc_path))

    print(f"8. ----------- Logging generated video: {post_id} -----------")
    log_generated_video(post_id, str(output_video_path))

    print(f"9. ----------- Upload generated video to YouTube: {post_id} -----------")
    metadata = json.loads(metadata_path.read_text())
    tags = metadata.get("tags", [])
    description = f"{metadata.get('summary', '')} \n\nTags: {', '.join([f'#{tag}' for tag in tags])}"
    upload_video(output_video_path, censored_title, description, tags)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run the main video generation pipeline.")
    parser.add_argument("subreddit_name", type=str, help="The name of the subreddit to scrape posts from.")
    args = parser.parse_args()

    main(subreddit_name=args.subreddit_name)
