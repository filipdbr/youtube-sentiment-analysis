# The project in progress 

# YouTube Sentiment Analysis: Clickbait Impact

I decided to analyse YouTube comments to understand how **clickbait titles influence viewer sentiment**. The app uses the YouTube Data API to fetch comments, applies text preprocessing and sentiment classification, and exposes predictions via a REST API.

## Features 

- Fetches comments from YouTube videos (done)
- Cleans and prepares text data for analysis
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
2. Install dependencies:
```shell
pip install -r requirements.txt
```
3. Create your environment configuration:
Make a copy of the example file:
  ```bash
  cp .env.example .env
  ```
- Open `.env` and replace the placeholder with your actual [YouTube API key](https://console.cloud.google.com/).

You can view the example file here: [.env.example](./.env.example)



