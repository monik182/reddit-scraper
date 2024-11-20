import os
import json
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
from googleapiclient.http import MediaFileUpload
from dotenv import load_dotenv
from datetime import datetime, timedelta
import googleapiclient.errors

load_dotenv()

SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]
TEMP_CLIENT_SECRETS_FILE = os.getenv("TEMP_CLIENT_SECRETS_FILE")
CLIENT_SECRETS = os.getenv("YOUTUBE_CLIENT_SECRETS")


def upload_video(video_file_path, title, description, tags, thumbnail_path=None, short=False, category_id="22", privacy_status="private", publish_at=None):
    with open(TEMP_CLIENT_SECRETS_FILE, 'w', encoding='UTF-8') as f:
        json.dump(json.loads(CLIENT_SECRETS), f)
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        TEMP_CLIENT_SECRETS_FILE, SCOPES)
    credentials = flow.run_local_server(port=0)
    youtube = googleapiclient.discovery.build("youtube", "v3", credentials=credentials)
    os.remove(TEMP_CLIENT_SECRETS_FILE)

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

    if publish_at:
        publish_at_iso = publish_at.isoformat("T") + "Z"
        body["status"].update({"publishAt": publish_at_iso, "privacyStatus": "private"})

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

# # Example usage
# if __name__ == "__main__":
#     video_path = "output/nfcpai-MaliciousCompliance-20210518-145150/nfcpai-MaliciousCompliance-20210518-145150_final_video.mp4"
#     title = "Sample Video Title"
#     description = "This is a sample video description."
#     tags = ["sample", "video", "test"]
#     thumbnail_path = "output/nfcpai-MaliciousCompliance-20210518-145150/nfcpai-MaliciousCompliance-20210518-145150_thumbnail.png"
#     # Schedule the post 1 day from now
#     # publish_time = datetime.utcnow() + timedelta(days=1)
#     publish_time = datetime.utcnow() + timedelta(hours=2)
#     upload_video(video_path, title, description, tags, thumbnail_path=thumbnail_path, publish_at=publish_time)
