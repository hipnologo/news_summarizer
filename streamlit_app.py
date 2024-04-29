import streamlit as st
import requests
import time
from urllib.parse import quote
from scraper import scrape_yahoo_finance # Own function
from openai import OpenAI
import os
# For sentiment analysis
from textblob import TextBlob  
from transformers import pipeline
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer


# Set your Assistant ID and instantiate the OpenAI client.
ASSISTANT_ID = "asst_Of2rJSAhLl8qNRc2m9Y9VuMj"

# Download VADER lexicon
nltk.download('vader_lexicon')

# Initialize the classifier globally if you are going to use Streamlit to prevent reloading for each call
classifier = pipeline('sentiment-analysis', model="ProsusAI/finbert")

# Function to analyze sentiment using NLTK's VADER
def analyze_sentiment_nltk(text):
    sid = SentimentIntensityAnalyzer()
    scores = sid.polarity_scores(text)
    return scores

# Function to analyze sentiment using BERT
def analyze_sentiment_bert(text):
    # Truncate the text to the maximum length of 512 tokens for BERT
    max_length = 512  # BERT's maximum token length
    
    # Tokenize the text and truncate if it's too long
    inputs = classifier.tokenizer.encode(text, add_special_tokens=True, truncation=True, max_length=max_length)
    
    # Convert tokens back to text
    truncated_text = classifier.tokenizer.decode(inputs, skip_special_tokens=True)
    
    # Perform sentiment analysis
    results = classifier(truncated_text)
    return results

# Function to analyze sentiment using TextBlob
def analyze_sentiment(text):
    return TextBlob(text).sentiment

@st.cache_data
def fetch_gnews(query, api_key):
    base_url = "https://gnews.io/api/v4/search"
    full_url = f"{base_url}?q={quote(query)}&lang=en&country=us&max=10&token={api_key}"
    try:
        response = requests.get(full_url)
        articles = response.json().get('articles', [])
        return [(article['title'], article['description'], article['url']) for article in articles]
    except Exception as e:
        st.error(f"Failed to fetch data from GNews: {str(e)}")
        return []

def create_openai_thread(content):
    try:
        thread = client.beta.threads.create(messages=[{"role": "user", "content": content}])
        run = client.beta.threads.runs.create(thread_id=thread.id, assistant_id=ASSISTANT_ID)
        while run.status != "completed":
            run = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
            time.sleep(1)
        message_response = client.beta.threads.messages.list(thread_id=thread.id)
        messages = message_response.data
        return messages[0].content[0].text.value
    except Exception as e:
        return f"Error in OpenAI Assistant API: {str(e)}"

    
# Main area for displaying results or additional features
st.set_page_config(layout='wide')

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    OPENAI_API_KEY = st.sidebar.text_input("Please enter your OpenAI API key: ")
client = OpenAI()

st.sidebar.text("Disclaimer: Demo purposes only.")

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
        
        assistant_response = create_openai_thread(content)
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
        assistant_response = create_openai_thread(content)
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
            
            assistant_response = create_openai_thread(url_content)
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
        assistant_response = create_openai_thread(content)
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
        assistant_response = create_openai_thread(content)
        response = assistant_response.replace("<br>-", "-")
        st.write("Assistant Response:")
        st.markdown(response, unsafe_allow_html=True)
