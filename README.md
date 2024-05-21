# News Summarizer

This app providers a summary of news along with sentiment analysis on news content using three different methods: NLTK's VADER, TextBlob, and BERT from the transformers library. The news headlines are gathered via various methods offered through the app, then an OpenAI Assistant is called via API to perform the summarization.

[![License: Apache License 2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Forks](https://img.shields.io/github/forks/hipnologo/news_summarizer)](https://github.com/hipnologo/news_summarizer/network/members)
[![Stars](https://img.shields.io/github/stars/hipnologo/news_summarizer)](https://github.com/hipnologo/news_summarizer/stargazers)
[![Issues](https://img.shields.io/github/issues/hipnologo/news_summarizer)](https://github.com/hipnologo/news_summarizer/issues)
[![GitHub contributors](https://img.shields.io/github/contributors/hipnologo/news_summarizer)](https://github.com/hipnologo/news_summarizer/graphs/contributors)

## Features

- Fetch news articles from GNews API and Yahoo Finance.
- Upload text files for sentiment analysis.
- Paste text directly into the app for summarization and analysis.
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

## Contributing
Contributions are welcome! To contribute to News Summarizer, please follow these guidelines:

* Fork the repository.
* Create a new branch for your changes.
* Make your changes and write tests for them.
* Run the tests using pytest to make sure they pass.
* Submit a pull request.


## Support
If you have any questions or need help using News Summarizer, please post a question or [open an issue](https://github.com/hipnologo/news_summarizer/issues) on GitHub.


## License
This project is licensed under the Apache 2.0 License - see the [LICENSE](https://opensource.org/licenses/Apache-2.0) file for details.

<a href="https://www.buymeacoffee.com/hipnologod" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/default-orange.png" alt="Buy Me A Coffee" height="41" width="174"></a>
