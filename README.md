# News Sentiment Analysis

This Streamlit app performs sentiment analysis on news content using three different methods: NLTK's VADER, TextBlob, and BERT from the transformers library.

## Features

- Fetch news articles from GNews and Yahoo Finance.
- Upload text files for sentiment analysis.
- Paste text directly into the app for analysis.
- Perform sentiment analysis using NLTK, TextBlob, or BERT.
- Interact with OpenAI's GPT model to create content based on the news.

## Installation

Before running the app, install the required libraries using:

```bash
pip install streamlit requests textblob transformers nltk
```

You also need to download the VADER lexicon with:
```python
import nltk
nltk.download('vader_lexicon')
```

## Usage
To start the app, run:
```bash
streamlit run streamlit_app.py
```

### Environment Variables
`GNEWS_API_KEY`: To fetch news from the GNews API.
`OPENAI_API_KEY`: For using the OpenAI GPT model.

Ensure these are set in your environment or use the Streamlit interface to input them.

### Input Options
- Upload a File: Upload a text file for sentiment analysis.
- Paste Text: Paste the news text directly into the app.
- Fetch from URL: Provide a URL to fetch content for analysis.
- GNews API: Enter a search query to fetch news from GNews.
- Yahoo Finance News: Get the latest news from Yahoo Finance.
- Sentiment Analysis Options
- Choose between NLTK, TextBlob, and BERT for sentiment analysis.
