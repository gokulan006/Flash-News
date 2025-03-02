from flask import Flask, render_template
import requests
from bs4 import BeautifulSoup
from apscheduler.schedulers.background import BackgroundScheduler
import atexit

from transformers import pipeline

ner = pipeline("ner", grouped_entities=True)



app = Flask(__name__)

# Initialize scheduler
scheduler = BackgroundScheduler()
scheduler.start()
atexit.register(lambda: scheduler.shutdown())

# Global variable to store latest news
latest_news = []

states=['Andhra Pradesh', 'Arunachal Pradesh', 'Assam', 'Bihar', 'Chhattisgarh', 'Delhi', 'Goa', 'Gujarat', 'Haryana', 'Himachal Pradesh', 'Jammu and Kashmir', 'Jharkhand', 'Kerala', 'Karnataka', 'Ladakh', 'Madhya Pradesh', 'Maharashtra', 'Manipur', 'Meghalaya', 'Mizoram', 'Nagaland', 'Odisha', 'Puducherry', 'Punjab', 'Rajasthan', 'Sikkim', 'Tamil Nadu', 'Telangana', 'Tripura', 'Uttar Pradesh', 'Uttarakhand', 'West Bengal']
def find_partial_match(text, states=states):
    for state in states:
        if state in text:
            return state
    return None
 
def classify_headline(item):
  headline=item['Content']
  doc = ner(headline)
  locations = [item['word'] for item in doc]
  state=find_partial_match(headline)
  if state:
    item['state']=state
  else:
    item['state']=None
  return  
def extract_news():
    base_url = "https://timesofindia.indiatimes.com/india"
    home_url = "https://timesofindia.indiatimes.com"
    num_pages = 9# Reduce pages for efficiency
    news_data = []

    for i in range(2, num_pages + 1):
        url = f"{base_url}/{i}"
        try:
            response = requests.get(url)
            response.raise_for_status()
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
                    article_response.raise_for_status()
                except requests.exceptions.RequestException as e:
                    print(f"Failed to fetch article {link}. Error: {e}")
                    continue

                article_soup = BeautifulSoup(article_response.content, "html.parser")
                
                content_div = article_soup.find("div", class_="_s30J clearfix")
                article_text = content_div.get_text(strip=True) if content_div else "Content not found"

                date_element = article_soup.find("div", class_="xf8Pm byline")
                published_date = date_element.find("span").text.strip() if date_element and date_element.find("span") else "Date not found"
                
                news_data.append({
                    "link": link,
                    "Title": span.text,
                    "Content": article_text,
                    
                    "Published_date": published_date
                })

    # Filter valid articles
    global latest_news
    latest_news = [item for item in news_data if item["Content"] != "Content not found" and item["Published_date"] != "Date not found"]
    for item in latest_news:
      classify_headline(item)
    
    for item in latest_news:
      if item['state']==None:
        item['state']='General News'
     
    
# Schedule news extraction every 24 hours
scheduler.add_job(extract_news, 'interval', minutes=20)

# Fetch news at startup
extract_news()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/blog')
def blog():
    return render_template('blog.html', news_articles=latest_news)

if __name__ == "__main__":
    app.run(debug=True)
