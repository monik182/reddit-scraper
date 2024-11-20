import os
import json
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
from googleapiclient.http import MediaFileUpload
from dotenv import load_dotenv

load_dotenv()

SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]
CLIENT_SECRETS_FILE = os.getenv("YOUTUBE_CLIENT_SECRETS_FILE")


def upload_video(video_file_path, title, description, tags, thumbnail_path=None, short=False, category_id="22", privacy_status="public"):
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        CLIENT_SECRETS_FILE, SCOPES)
    credentials = flow.run_local_server(port=0)
    youtube = googleapiclient.discovery.build("youtube", "v3", credentials=credentials)

    if len(title) > 70:
        title = title[:60] + "..."
    
    if short:
        title = f"{title} #shorts"

    body = {
        "snippet": {
            "title": title,
            "description": description,
            "tags": tags,
            "categoryId": category_id
        },
        "status": {
            "privacyStatus": privacy_status
        }
    }
    print(f"Uploading video: {video_file_path}")
    print(f"Body>>>>: {body}")

    media = MediaFileUpload(video_file_path, resumable=True)
    print(f"Media>>>>: {media}")
    request = youtube.videos().insert(
        part="snippet,status",
        body=body,
        media_body=media
    )
    print(f"Request>>>>: {request}")

    response = None
    while response is None:
        status, response = request.next_chunk()
        if status:
            print(f"Uploaded {int(status.progress() * 100)}%...")

    print("Upload complete!")
    print(f"Video ID: {response['id']}")

    if thumbnail_path:
        youtube.thumbnails().set(
            videoId=response['id'],
            media_body=MediaFileUpload(thumbnail_path)
        ).execute()
        print("Thumbnail uploaded successfully!")
