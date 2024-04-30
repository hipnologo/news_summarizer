"""
News Summarizer & Sentiment Analysis App
Copyright (c) 2024 Fabio Carvalho @hipnologo

This program is licensed under the Apache 2.0 License.
You should have received a copy of the Apache 2.0 License along with this program.
If not, see <https://opensource.org/license/apache-2-0>.
"""

import streamlit as st
import requests
from urllib.parse import quote
from scraper import scrape_yahoo_finance  # Own function
from openai import OpenAI
import os
import time
from textblob import TextBlob
from transformers import pipeline
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer

nltk.download('vader_lexicon')

# Set your Assistant ID and instantiate the OpenAI client.
ASSISTANT_ID = "asst_Of2rJSAhLl8qNRc2m9Y9VuMj"

st.set_page_config(
    page_title="News Summarizer & Sentiment Analysis",
    page_icon="🗞️",
    layout="wide",
    initial_sidebar_state="expanded"
    # menu_items={
    #     'Get Help': 'https://www.myapp.com/help',
    #     'Report a bug': "https://www.myapp.com/bug",
    #     'About': "# This is a header. This is an *extremely* cool app!"
    # }
)

# Using cache to load models
@st.cache_resource
def load_models():
    # Load sentiment analysis models
    classifier = pipeline('sentiment-analysis', model="ProsusAI/finbert")
    sid = SentimentIntensityAnalyzer()
    return classifier, sid

classifier, sid = load_models()

# Function to analyze sentiment using NLTK's VADER
def analyze_sentiment_nltk(text):
    scores = sid.polarity_scores(text)
    return scores

# Function to analyze sentiment using BERT
def analyze_sentiment_bert(text):
    max_length = 512  # BERT's maximum token length
    inputs = classifier.tokenizer.encode(text, add_special_tokens=True, truncation=True, max_length=max_length)
    truncated_text = classifier.tokenizer.decode(inputs, skip_special_tokens=True)
    results = classifier(truncated_text)
    return results

# Function to analyze sentiment using TextBlob
def analyze_sentiment(text):
    return TextBlob(text).sentiment

@st.cache_resource(ttl=300)  # 👈 Cache data for 300 seconds
def get_openai_client(api_key):
    # Cache the OpenAI client to avoid reinitialization
    return OpenAI(api_key=api_key)

# Caching the API request
@st.cache_data(show_spinner="Fetching News...")
def fetch_gnews(query, api_key):
    base_url = "https://gnews.io/api/v4/search"
    full_url = f"{base_url}?q={quote(query)}&lang=en&country=us&max=10&token={api_key}"
    response = requests.get(full_url)
    articles = response.json().get('articles', [])
    return [(article['title'], article['description'], article['url']) for article in articles]

def create_openai_thread(content, api_key):
    client = get_openai_client(api_key)
    thread = client.beta.threads.create(messages=[{"role": "user", "content": content}])
    run = client.beta.threads.runs.create(thread_id=thread.id, assistant_id=ASSISTANT_ID)
    while run.status != "completed":
        run = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
        time.sleep(1)
    message_response = client.beta.threads.messages.list(thread_id=thread.id)
    messages = message_response.data
    return messages[0].content[0].text.value

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY") or st.sidebar.text_input("Please enter your OpenAI API key:")
if not OPENAI_API_KEY:
    st.error("OpenAI API key is required to run this app.")
    st.stop()

st.title("News Summarizer & Sentiment Analysis")
st.write("Results will appear here based on the input method selected in the sidebar.")

# Sidebar for input options
st.sidebar.title("Input Options")
option = st.sidebar.selectbox("Choose your input method:", ["Upload a File", "Paste Text", "Fetch from URL", "GNews API", "Yahoo Finance News"])

st.sidebar.title("Sentiment Analysis Options")
analysis_method = st.sidebar.selectbox("Choose the sentiment analysis method:",
                                       ["NLTK", "TextBlob", "BERT"])

if option == "Upload a File":
    uploaded_file = st.sidebar.file_uploader("Choose a file")
    if uploaded_file is not None:
        content = uploaded_file.getvalue().decode("utf-8")
        
        # Sentiment analysis
        if analysis_method == "NLTK":
            sentiment = analyze_sentiment_nltk(content)
        elif analysis_method == "BERT":
            sentiment = analyze_sentiment_bert(content)
        elif analysis_method == "TextBlob":
            sentiment = analyze_sentiment(content)

        st.write("Sentiment:", sentiment)
        
        assistant_response = create_openai_thread(content, OPENAI_API_KEY)
        response = assistant_response.replace("<br>-", "-")
        st.write("Assistant Response:")
        st.markdown(response, unsafe_allow_html=True)

elif option == "Paste Text":
    text = st.sidebar.text_area("Paste your text here:")
    if st.sidebar.button("Analyze"):
        if analysis_method == "NLTK":
            sentiment = analyze_sentiment_nltk(text)
        elif analysis_method == "BERT":
            sentiment = analyze_sentiment_bert(text)
        elif analysis_method == "TextBlob":
            sentiment = analyze_sentiment(text)

        st.write("Sentiment:", sentiment)

        content = text
        assistant_response = create_openai_thread(content, OPENAI_API_KEY)
        response = assistant_response.replace("<br>-", "-")
        st.write("Assistant Response:")
        st.markdown(response, unsafe_allow_html=True)

elif option == "Fetch from URL":
    url = st.sidebar.text_input("Enter URL:")
    if st.sidebar.button("Fetch"):
        try:
            url_response = requests.get(url)
            url_content = url_response.text
            
            # Sentiment analysis
            if analysis_method == "NLTK":
                sentiment = analyze_sentiment_nltk(url_content)
            elif analysis_method == "BERT":
                sentiment = analyze_sentiment_bert(url_content)
            elif analysis_method == "TextBlob":
                sentiment = analyze_sentiment(url_content)

            st.write("Sentiment:", sentiment)
            
            assistant_response = create_openai_thread(url_content, OPENAI_API_KEY)
            response = assistant_response.replace("<br>-", "-")            
            st.write("Assistant Response:")
            st.markdown(response, unsafe_allow_html=True)
            st.write("Fetched Content:")
            st.markdown(content, unsafe_allow_html=True)
        except Exception as e:
            st.error("Failed to fetch content from URL")

elif option == "GNews API":
    query = st.sidebar.text_input("Enter search query:")
    if "GNEWS_API_KEY" in os.environ:
        api_key = os.environ["GNEWS_API_KEY"]
    else:
        api_key = st.text_input("Enter API Key:", help="API key not found in environment variables.")
    if st.sidebar.button("Fetch News"):
        articles = fetch_gnews(query, api_key)
        content = "\n".join([title for title, _, _ in articles])
        # Sentiment analysis
        if analysis_method == "NLTK":
            sentiment = analyze_sentiment_nltk(content)
        elif analysis_method == "BERT":
            sentiment = analyze_sentiment_bert(content)
        elif analysis_method == "TextBlob":
            sentiment = analyze_sentiment(content)

        st.write("Sentiment:", sentiment)
        # OpenAI Assistant
        assistant_response = create_openai_thread(content, OPENAI_API_KEY)
        response = assistant_response.replace("<br>-", "-")
        st.write("Assistant Response:")
        st.markdown(response, unsafe_allow_html=True)

elif option == "Yahoo Finance News":
    if st.sidebar.button("Fetch News"):
        articles = scrape_yahoo_finance()
        content = "\n".join([title for title, _, _ in articles])
        # Sentiment Analysis
        if analysis_method == "NLTK":
            sentiment = analyze_sentiment_nltk(content)
        elif analysis_method == "BERT":
            sentiment = analyze_sentiment_bert(content)
        elif analysis_method == "TextBlob":
            sentiment = analyze_sentiment(content)

        st.write("Sentiment:", sentiment)
        
        # OpenAI Assistant
        assistant_response = create_openai_thread(content, OPENAI_API_KEY)
        response = assistant_response.replace("<br>-", "-")
        st.write("Assistant Response:")
        st.markdown(response, unsafe_allow_html=True)

st.sidebar.markdown("Disclaimer: The information provided in this app is for demonstration purposes only and should not be considered as financial, investment, or professional advice. The app's functionality and results are based on publicly available data and models, which may not always be accurate or up-to-date. Users are advised to conduct their own research and consult with a qualified professional before making any financial decisions. Use this app at your own risk.")
