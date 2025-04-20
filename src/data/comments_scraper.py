import os
from dotenv import load_dotenv
from googleapiclient.discovery import build

# load environment variables
load_dotenv()
api_key = os.getenv("api_key")

# build the YouTube API client
youtube = build("youtube", "v3", developerKey=api_key)

# define the function retrieving the comments
def get_comments(video_id):
    """
    Returns a list of comments for a video.
    :param video_id: the ID of the video (string)
    :return: a list of comments as strings
    """

    comments = []               # a list to store comments
    next_page_token = None      # start with first page

    while True:
        # make a request to fetch comments
        request = youtube.commentThreads().list(
            part="snippet",             # fetching only the snipped part
            videoId=video_id,           # ID of the video
            maxResults=100,             # fetch 100 comments per page (max in YouTube Data API)
            pageToken=next_page_token   # start with first page
        ).execute()                     # execute the request

        # extract comments and store them in comments list
        for item in request["items"]:
            comment = item["snippet"]["topLevelComment"]["snippet"]["textDisplay"]
            comments.append(comment)

        # check for next page
        next_page_token = request.get("nextPageToken")
        if not next_page_token:
            break

    # return the list of comments
    return comments

#test
video_id = "th5_9woFJmk"
test_comments = get_comments(video_id, 2)

print(test_comments)