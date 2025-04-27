from importlib.metadata import distribution

import pandas as pd

def create_dataframe(input_path: str) -> pd.DataFrame:
    """
    1. Load raw JSON into a dataframe
    2. Turn each list of comments into its own row
    3. Rename that column to text
    :param input_path: path of a source file (raw data fetched by comments_scraper)
    :return: structured dataframe
    """
    # read the JSON with raw data
    data = pd.read_json(input_path)

    # split the list of comments so that each comment gets its own row
    dataFrame = data.explode("comments").reset_index(drop = True)

    # rename 'comments' to 'txt'
    dataFrame = dataFrame.rename(columns = {"comments": "text"})

    return dataFrame

if __name__ == "__main__":

    # run the function to create a dataframe
    dataFrame = create_dataframe("data/raw/youtube_data.json")

    # show a few first raws
    print(dataFrame.head())

    # see how many comments come form clickbait vs non-clickbait
    print("\nClickbait distribution:")
    print(dataFrame["clickbait"].value_counts())