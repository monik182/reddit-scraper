# Reddit Video Generation Pipeline

## Overview

This repository contains scripts to automatically generate YouTube videos from Reddit posts. The main script ties together various components including scraping Reddit posts, generating audio, creating thumbnails, generating subtitles (closed captions), and compiling everything into a video.

## Main Script

The primary script is `main.py`, which does the following:

1. **Reads Log of Generated Videos**: Loads the log of previously generated videos and compares it to scraped Reddit posts to identify new posts that haven't yet been used to generate videos.
2. **Scrapes Reddit Posts**: If there are no new posts available, it scrapes more posts from the specified subreddit.
3. **Selects a Post**: Selects one post from those that haven't yet been turned into videos.
4. **Generates Audio**: Generates an audio file using the content of the selected Reddit post, with profanity censored.
5. **Generates Closed Captions (CC)**: Generates subtitles based on the audio.
6. **Generates Video**: Creates a video using a random video clip, generated audio, and subtitles.
7. **Generates a Thumbnail**: Creates a thumbnail for the video.
8. **Logs the Generated Video**: Logs the video details to prevent reuse of the same post.

## How to Use

### Requirements
- Python 3.7+
- Install the required packages by running:
  ```sh
  pip install -r requirements.txt
  ```
- Set up your environment variables in a `.env` file for Reddit API and OpenAI API keys.

### Running the Main Script
You can run the main script by specifying the subreddit name as a command-line argument. For example:
```sh
python main.py <Subreddit>
```
This command will start the entire video generation pipeline using posts from the **{Subreddit}** subreddit.

## Folder Structure
- **output/**: The main directory where generated videos, audio files, closed captions, thumbnails, and metadata are stored. Each generated video has its own folder named after the Reddit post ID.
- **output_reddit_posts/**: Directory where scraped Reddit posts are stored in JSON format.
- **output_videos/**: Directory containing random video clips that will be used in the final video generation.
- **output_thumbnails/**: Directory where generated thumbnails are saved.
- **generated_videos_log.txt**: A log file that keeps track of which posts have been used to generate videos.

## Environment Variables
Ensure you have a `.env` file with the following environment variables set up:
- `REDDIT_CLIENT_ID`: Your Reddit API client ID.
- `REDDIT_CLIENT_SECRET`: Your Reddit API client secret.
- `REDDIT_USER_AGENT`: Your Reddit API user agent.
- `OPENAI_API_KEY`: Your OpenAI API key.

## Scripts
- **scrape_bulk.py**: Scrapes long posts from a specific subreddit.
- **generate_audio.py**: Generates audio from text using OpenAI's API.
- **generate_thumbnail.py**: Creates a thumbnail for a video.
- **generate_video.py**: Combines video, audio, and closed captions to generate a final video.
- **youtube_metadata.py**: Generates YouTube metadata, including video descriptions and tags.
- **profanity_censor.py**: Censors profane words in the text.

## Future Improvements
- Add more sophisticated text analysis to select the most interesting Reddit posts.
- Improve thumbnail generation by adding more dynamic visuals and elements.
- Incorporate more advanced NLP models for better summarization and storytelling.

## License
This project is licensed under the MIT License.

## Acknowledgments
- **OpenAI**: For the language model and text-to-speech capabilities.
- **Reddit**: For providing a vast collection of interesting user-generated content.
