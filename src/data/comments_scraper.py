import os
from dotenv import load_dotenv
from googleapiclient.discovery import build
from typing import Any, Dict

from urllib3 import request

# load environment variables
load_dotenv()
api_key = os.getenv("api_key")

# build the YouTube API client
youtube = build("youtube", "v3", developerKey=api_key)

# define the function retrieving the comments
def get_comments(video_id: str) -> list[dict]:
    """
    Returns a list of comments for a video
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

# # I could get metadata in the same function while getting comments,
# but to adhere to the single responsibility principle and improve testing and mintenance, I'm doing it in a separate function.
def get_metadata(video_id: str) -> Dict[str, Any]:
    """
    Returns metadata for a video
    :param video_id: the ID of the video (string)
    :return: metadata as a dictionary
    """
    # make a request to fetch metadata
    request = youtube.videos().list(
        part="snippet, statistics",     # fetch snipped and statistics
        id=video_id,                    # video id provided by the user
    ).execute()                         # execute the request

    # take the first element from items
    response = request["items"][0]

    # store the metadata
    metadata = {
        "title" : response["snippet"]["title"],
        "description" : response["snippet"]["description"],
        "channel": response["snippet"]["channelTitle"],
        "viewCount": response["statistics"]["viewCount"],
        "likeCount": response["statistics"]["likeCount"],
        "commentCount": response["statistics"]["commentCount"]
    }

    return metadata
