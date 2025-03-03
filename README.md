# Flash News App

## Demo
[App](https://mighty-brook-89788-170c96668c0b.herokuapp.com/)

## Overview
This is a Flask-based web application that scrapes and displays the latest news articles from the *Times of India* website. The application categorizes news based on Indian states and updates the news articles periodically using a background scheduler.

## Features
- Scrapes news articles from *Times of India*
- Categorizes news based on state names found in article content
- Displays the latest news articles on the blog page
- Updates news every 20 minutes using the *APScheduler* library
- Provides a "Back to Top" button for smooth navigation

## Technologies Used
- **Flask**: For building the web application
- **BeautifulSoup**: For web scraping
- **Requests**: For making HTTP requests
- **APScheduler**: For scheduling periodic news updates
- **Jinja2**: For templating in HTML
- **Bootstrap/CSS**: For styling

## Installation
1. Clone the repository:
   ```sh
   git clone https://github.com/your-repo/news-aggregator.git
   cd news-aggregator
   ```
2. Create a virtual environment (optional but recommended):
   ```sh
   python -m venv venv
   source venv/bin/activate  # For macOS/Linux
   venv\Scripts\activate  # For Windows
   ```
3. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```

## Running the Application
1. Start the Flask server:
   ```sh
   python app.py
   ```
2. Open a browser and go to:
   ```
   http://127.0.0.1:5000/
   ```

## Project Structure
```
├── app.py               # Main Flask application
├── templates
│   ├── index.html       # Home page
│   ├── blog.html        # Blog page with news articles
├── static
│   ├── styles.css       # CSS file for styling
├── requirements.txt     # List of dependencies
├── README.md            # Project documentation
```

## API Endpoints
- **`/`** → Home Page
- **`/blog`** → News Blog Page (Displays categorized news articles)

## Deployment
This project can be deployed on **Heroku**, **Render**, or any cloud platform supporting Flask.
1. Create a `Procfile` with the following content:
   ```
   web: gunicorn app:app
   ```
2. Install Gunicorn:
   ```sh
   pip install gunicorn
   ```
3. Deploy using Heroku CLI:
   ```sh
   heroku create your-app-name
   git push heroku main
   ```

## Future Enhancements
- Add more news sources
- Implement user authentication
- Enable keyword-based filtering
- Implement a database to store news articles

## License
This project is open-source and available under the MIT License.

---

### Author
- **M. Gokulan**
- Email: mgokulan06@gmail.com
- GitHub: [gokulan006](https://github.com/gokulan006)

