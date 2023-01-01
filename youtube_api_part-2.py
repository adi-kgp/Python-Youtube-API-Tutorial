""" 
This script demonstrates how to:
Find or sort the most popular videos in a youtube channel playlist (video with most view count printed at top)
"""

from googleapiclient.discovery import build 

api_key = 'AIzaSyDkGmMMlDoc9XcNJ17lN2Ptc6peBx7sGtY'

youtube = build('youtube', 'v3', developerKey=api_key)

playlist_id = "PL8uoeex94UhFrNUV2m5MigREebUms39U5"

videos = []

nextPageToken = None

while True:
    pl_request = youtube.playlistItems().list(
        part="contentDetails",
        playlistId = playlist_id,
        maxResults = 50,
        pageToken= nextPageToken
    )

    pl_response = pl_request.execute()

    vid_ids = []
    for item in pl_response['items']:
        vid_ids.append(item['contentDetails']['videoId'])
        
    # print(','.join(vid_ids))

    vid_request = youtube.videos().list(
        part="statistics",
        id=','.join(vid_ids)
    )

    vid_response = vid_request.execute()

    for item in vid_response['items']:

        vid_views = item['statistics']['viewCount']

        vid_id = item['id']
        yt_link = f"https://youtu.be/{vid_id}"

        videos.append(
            {
                'views': int(vid_views),
                'url': yt_link
            }
        )

    nextPageToken = pl_response.get('nextPageToken')

    if not nextPageToken:
        break

videos.sort(key=lambda vid: vid['views'], reverse=True)

for video in videos:
    print(video['url'], video['views'])

# print(len(videos)) # prints the sum of all video lengths in a playlist

