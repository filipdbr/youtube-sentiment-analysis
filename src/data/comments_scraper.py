import os
from dotenv import load_dotenv
from googleapiclient.discovery import build
from typing import Any, Dict
import json

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

# function getting and saving comments and metadata
def save_data(video_ids: list[str], path: str = 'youtube_data.json') -> None:
    '''
    Get and save the data for each video
    :param video_ids: a list of video IDs as strings
    :param path: a path to save the file
    :return: JSON
    '''

    # ensure the directory exists
    directory = os.path.dirname(path)
    if directory:
        os.makedirs(directory, exist_ok=True)

    # open output file for writing (overwrite existing data)
    with open(path, 'w', encoding='utf-8') as f:
        #create an empty list to store data
        dataset = []
        for video in video_ids:
            print(f"Processing video {video}")
            # call functions to get the data
            comments = get_comments(video)
            metadata = get_metadata(video)

            # prompt user to label the video as clickbait or not
            info = input(f"Is \"{metadata['title']}\" a clickbait? (yes/no): ").strip().lower()
            is_clickbait = info.startswith("y")

            # build a record
            json_entry = {
                "video_id": video,
                "clickbait": is_clickbait,
                "metadata": metadata,
                "comments": comments
            }
            # add to the dataset
            dataset.append(json_entry)

        # save the file
        json.dump(dataset, f, indent=2, ensure_ascii=False)

        #close the file
        f.close()

        print(f"Saved {len(dataset)} videos to {path}")


def load_videos(path: str,) -> list[str]:
    '''
    The function load videos from the file
    :param path: path to the file containing the videos (line by line)
    :return: list of video IDs as strings
    '''
    with open(path, 'r', encoding='utf-8') as f:
        return [record.strip() for record in f if record.strip()]