# scraper.py
import requests
from bs4 import BeautifulSoup

def scrape_yahoo_finance():
    url = 'https://finance.yahoo.com/topic/latest-news/'
    headers = {'User-Agent': 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'}
    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        news_headlines = []
        for item in soup.select('h3.Mb\\(5px\\)'):
            title = item.text.strip()
            link = 'https://finance.yahoo.com' + item.find('a')['href']
            description = item.find_next_sibling('p').text if item.find_next_sibling('p') else "No description available."
            news_headlines.append((title, link, description))
        
        return news_headlines
    except Exception as e:
        print(f"Error scraping Yahoo Finance news: {e}")
        return []

# Example usage
if __name__ == "__main__":
    headlines = scrape_yahoo_finance()
    for title, link, description in headlines:
        print(f"Title: {title}\nLink: {link}\nDescription: {description}\n")

