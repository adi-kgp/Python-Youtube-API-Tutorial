import os
import pickle
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request


credentials = None

#api_key = 'AIzaSyDkGmMMlDoc9XcNJ17lN2Ptc6peBx7sGtY'

# token.pickle stores the user's credentials from previously successful logins
if os.path.exists('token.pickle'):
    print('Loading Credentials From File...')
    with open('token.pickle', 'rb') as token:
        credentials = pickle.load(token)

# If there are no valid credentials available, then either refresh the token or log in.
if not credentials or not credentials.valid:
    if credentials and credentials.expired and credentials.refresh_token:
        print('Refreshing Access Token...')
        credentials.refresh(Request())
    else:
        print('Fetching New Tokens...')
        flow = InstalledAppFlow.from_client_secrets_file(
            'client_secrets.json',
            scopes=[
                'https://www.googleapis.com/auth/youtube.readonly'
            ]
        )

        flow.run_local_server(port=8080, prompt='consent',
                              authorization_prompt_message='')
        credentials = flow.credentials

        # Save the credentials for the next run
        with open('token.pickle', 'wb') as f:
            print('Saving Credentials for Future Use...')
            pickle.dump(credentials, f)

flow = InstalledAppFlow.from_client_secrets_file(
		'client_secrets.json',
		scopes = ['https://www.googleapis.com/auth/youtube.readonly']
	)

flow.run_local_server(port=8080, prompt='consent', authorization_prompt_message='')

print(credentials.to_json())

youtube = build("youtube", "v3", credentials=credentials)
request = youtube.playlistItems().list(part="status, contentDetails", playlistId="UUCezIgC97PvUuR4_gbFUs5g")
response = request.execute()

for item in response['items']:
	vid_id = item['contentDetails']['videoId']
	yt_link = f"https://youtu.be/{vid_id}"
	print(yt_link)

