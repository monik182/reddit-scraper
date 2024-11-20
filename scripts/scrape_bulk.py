import os
import praw
import json
from pathlib import Path
from dotenv import load_dotenv
import time

load_dotenv()

reddit = praw.Reddit(
    client_id=os.getenv('REDDIT_CLIENT_ID'),
    client_secret=os.getenv('REDDIT_CLIENT_SECRET'),
    user_agent=os.getenv('REDDIT_USER_AGENT')
)

output_dir = Path("output_reddit_posts")

logs_dir = Path("logs")
output_dir = Path("output")
resources_dir = Path("resources")
videos_dir = Path("videos")
output_dir.mkdir(exist_ok=True)


def load_logged_post_ids(subreddit_name):
    log_file = logs_dir / f"{subreddit_name}_scraped_posts_log.txt"
    if not log_file.exists():
        return set()
    with open(log_file, "r", encoding="utf-8") as log:
        return set(line.split("|")[1].strip() for line in log.readlines())


def scrape_long_posts(subreddit_name, limit=3):
    subreddit = reddit.subreddit(subreddit_name)

    scraped_count = 0
    logged_post_ids = load_logged_post_ids(subreddit_name)
    log_file = logs_dir / f"{subreddit_name}_scraped_posts_log.txt"

    submissions = subreddit.top(limit=None, time_filter='all')

    for submission in submissions:
        if scraped_count >= limit:
            break
        if submission.id in logged_post_ids:
            continue

        if len(submission.selftext) >= 1000:

            timestamp = time.strftime('%Y%m%d-%H%M%S', time.gmtime(submission.created_utc))
            filename = f"{submission.id}-{subreddit_name}-{timestamp}.json"
            filepath = output_dir / filename

            with open(filepath, "w", encoding="utf-8") as file:
                json.dump(submission.__dict__, file, default=str, indent=4)

            with open(log_file, "a", encoding="utf-8") as log:
                log.write(f"{time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(submission.created_utc))} | {submission.id} | {submission.url}\n")

            scraped_count += 1
