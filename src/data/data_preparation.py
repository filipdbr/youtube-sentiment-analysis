from importlib.metadata import distribution
from text_preprocessing import preprocess_comments # import the preprocessing function

import pandas as pd

def create_dataframe(input_path: str, preprocess: bool = True) -> pd.DataFrame:
    """
    1. Load raw JSON into a dataframe
    2. Turn each list of comments into its own row
    3. Rename that column to text
    4. Preprocess text for analysis
    :param input_path: path of a source file (raw data fetched by comments_scraper)
    :param preprocess: whether to apply text preprocessing (default: True)
    :return: structured dataframe
    """
    # read the JSON with raw data
    data = pd.read_json(input_path)

    # split the list of comments so that each comment gets its own row
    dataFrame = data.explode("comments").reset_index(drop = True)

    # rename 'comments' to 'txt'
    dataFrame = dataFrame.rename(columns = {"comments": "text"})

    # preprocess text
    if preprocess:
        print("Preprocessing text...")
        dataFrame['cleaned_text'] = dataFrame['text'].apply(preprocess_comments)
        print("Text preprocessing completed")

    return dataFrame

if __name__ == "__main__":

    # run the function to create a dataframe
    data_frame = create_dataframe("data/raw/youtube_data.json")

    # show a few first raws
    print(data_frame.head())

    # see how many comments come form clickbait vs non-clickbait
    print("\nClickbait distribution:")
    print(data_frame["clickbait"].value_counts())

    # if data was pre-processed print the text sample and a few first raws
    if 'cleaned_text' in data_frame.columns:
        print("\nSample cleaned text:")
        print(data_frame[['text', 'cleaned_text']].head())