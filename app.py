from flask import Flask, render_template
import requests
from bs4 import BeautifulSoup
from apscheduler.schedulers.background import BackgroundScheduler
import atexit

app = Flask(__name__)

# Initialize scheduler
scheduler = BackgroundScheduler()
scheduler.start()
atexit.register(lambda: scheduler.shutdown())  # Corrected typo

# Global variable to store latest news
latest_news = []

def extract_news():
    base_url = "https://timesofindia.indiatimes.com/india"
    home_url = "https://timesofindia.indiatimes.com"
    num_pages = 5
    news_data = []

    for i in range(2, num_pages + 1):
        url = f"{base_url}/{i}"
        try:
            response = requests.get(url)
            response.raise_for_status()  # Raise an error for bad status codes
        except requests.exceptions.RequestException as e:
            print(f"Failed to fetch page {i}. Error: {e}")
            continue

        soup = BeautifulSoup(response.content, "html.parser")

        article_divs = soup.find_all("div", id="c_wdt_list_1")
        if not article_divs:
            print(f"Warning: No articles found on page {i}")
            continue

        for article_div in article_divs:
            for span in article_div.find_all("span", class_="w_tle"):
                link_tag = span.find("a")
                if not link_tag or "href" not in link_tag.attrs:
                    continue

                link = link_tag["href"]
                if link.startswith("/"):
                    link = home_url + link

                try:
                    article_response = requests.get(link)
                    article_response.raise_for_status()  # Raise an error for bad status codes
                except requests.exceptions.RequestException as e:
                    print(f"Failed to fetch article {link}. Error: {e}")
                    continue

                article_soup = BeautifulSoup(article_response.content, "html.parser")

                content_div = article_soup.find("div", class_="_s30J clearfix")
                if content_div:
                    for br in content_div.find_all("br"):
                        br.replace_with("\n")
                    article_text = content_div.get_text().strip()
                else:
                    print(f"Content not found {link}")
                    article_text = "Content not found"

                date_element = article_soup.find("div", class_="xf8Pm byline")
                published_date = "Date not found"
                if date_element:
                    span_element = date_element.find("span")
                    if span_element:
                        published_date = span_element.text.strip()

                news_data.append({
                    "link": link,
                    "Title": span.text,
                    "Content": article_text,
                    "Published_date": published_date
                })

    # Filter out articles with missing content or date
    news_articles = [item for item in news_data if item["Content"] != "Content not found" and item["Published_date"] != "Date not found"]
    global latest_news
    latest_news = news_articles
    print("News articles fetched successfully.")

# Schedule the extract_news function to run every 24 hours
scheduler.add_job(extract_news, 'interval', hours=24)

# Fetch news immediately on startup
extract_news()

@app.route('/')
def index():
    return render_template('index.html')  # Corrected typo

@app.route('/blog')
def blog():
    global latest_news
    return render_template('blog.html', news_articles=latest_news)  # Corrected typo

if __name__ == "__main__":
    app.run(debug=True)