# The project in progress 

# YouTube Sentiment Analysis: Clickbait Impact

I decided to analyse YouTube comments to understand how **clickbait titles influence viewer sentiment**. The app uses the YouTube Data API to fetch comments, applies text preprocessing and sentiment classification, and exposes predictions via a REST API.

## Video Selection & Dataset Overview

- **Total videos:** 20 (manually selected)  
  - **Clickbait:** 10  
  - **Non-clickbait:** 10  
- **View count range:** from ~100 000 up to several million views, to capture both niche and highly popular content  
- **Topic:** “how to lose weight” and “how to get abs” — an area rich in both clickbait and non-clickbait, informative titles  
- **Audience:** content aimed at both men and women interested in fitness and weight loss  
- **IDs file:** All video IDs are listed in [`videos_ids.txt`](./videos_ids.txt)  
- **Raw Dataset** in [`youtube_data.json`](./data/raw/youtube_data.json)

This balanced, topic-focused sample gives me a clear, controlled basis for comparing how title style (clickbait vs. non-clickbait) correlates with viewer sentiment.

## Features 

### Data Collection
  - Fetches top‐level comments for any video ID via the YouTube Data API  
  - Retrieves metadata (title, description, channel, view/like/comment counts)
  - Saves everything into a structured JSON file 

### Data Preparation
  - Reads the raw JSON into a pandas DataFrame
  - Splits each comment into its own row (one comment per row, carrying video metadata)
  - Renames the comment column to text for clarity 
  - Provides a quick check of clickbait vs. non-clickbait distribution

### Upcoming features
- Cleans data for analysis
- Trains a sentiment analysis model using machine learning
- Compares sentiment distributions between clickbait and non-clickbait videos
- Exposes a FastAPI endpoint for real-time predictions

## Hypothesis

> Videos with clickbait titles lead to more **negative** viewer sentiment in the comments compared to videos with descriptive, non-clickbait titles.

## Tech Stack

- **Python**
- **YouTube Data API v3**
- **Scikit-Learn** / **Transformers**
- **Pandas, NumPy**
- **FastAPI**
- **Docker** 
- **.env config** with `dotenv`

## Setup

1. Clone the repository
```shell
git clone https://github.com/yourusername/youtube-sentiment-analysis.git
cd youtube-sentiment-analysis
```
2. Install dependencies:
```shell
pip install -r requirements.txt
```
3. Create your environment configuration:
Make a copy of the example file:
  ```bash
  cp .env.example .env
  ```
Open `.env` and replace the placeholder with your actual [YouTube API key](https://console.cloud.google.com/).

You can view the example file here: [.env.example](./.env.example)

## Quickstart
1. Collect raw data:
You can add videos of your choice by updating the content of [`videos_ids.txt`](./videos_ids.txt).
2. Run the comments scraper
```shell
python src/data/comments_scraper.py
```
3. Prepare data by running: 
```shell
python src/data_preparation.py
```
Output:
* Raw JSON: [`youtube_data.json`](./data/raw/youtube_data.json)
* Prepared DataFrame: displayed in your console


