import os, glob
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

print(">> YouTube Uploader - YOUR channel...")

if not os.path.exists('token.json'):
    print("No token.json - video generated but not uploaded. Add YOUTUBE_TOKEN_JSON secret")
    exit(0)

creds = Credentials.from_authorized_user_file('token.json', ['https://www.googleapis.com/auth/youtube.upload'])
youtube = build('youtube', 'v3', credentials=creds)

videos = sorted(glob.glob("video_*.mp4"))
if not videos:
    print("No video found")
    exit(0)

video_file = videos[-1]
scripts = sorted(glob.glob("script_*.txt"))
desc = open(scripts[-1], encoding="utf-8").read()[:2000] if scripts else "Business case study"
title = f"{desc[:60]} | Business Case Study"

print(f"Uploading {video_file}...")
request = youtube.videos().insert(
    part="snippet,status",
    body={
        "snippet": {"title": title[:100], "description": desc + "\n\n#Business", "tags": ["business"], "categoryId": "27"},
        "status": {"privacyStatus": "public", "selfDeclaredMadeForKids": False}
    },
    media_body=MediaFileUpload(video_file, chunksize=-1, resumable=True)
)
resp = request.execute()
print(f"✅ UPLOADED: https://youtube.com/watch?v={resp['id']}")
