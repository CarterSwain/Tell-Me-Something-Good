import requests, random, json, os
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from .firebase_util import send_push_notification

CACHE_FILE = "cached_news.json"
CACHE_EXPIRY_HOURS = 24



def get_happy_news():
    """ Scrape Good News Network Headlines. """
    url = "https://www.goodnewsnetwork.org/category/news/"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    headlines = []
    for article in soup.select("h3.entry-title")[:10]:
        title = article.text.strip()
        link = article.find("a")["href"]
        headlines.append({
            "headline": title,
            "link": link,
            "source": "Good News Network",
            "summary": None
        })
    return headlines



def get_positive_news():
    """ Scrape Positive News Headlines. """
    url = "https://www.positive.news/society/"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    headlines = []
    for article in soup.select("h2.entry-title")[:10]:
        title = article.text.strip()
        link = article.find("a")["href"]
        headlines.append({
            "headline": title,
            "link": link,
            "source": "Positive News",
            "summary": None
        })
    return headlines



def get_optimist_daily():
    """ Scrape Optimist Daily Headlines. """
    url = "https://www.optimistdaily.com/category/news/"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    headlines = []
    for article in soup.select("h3.entry-title")[:10]:
        title = article.text.strip()
        link = article.find("a")["href"]
        headlines.append({
            "headline": title,
            "link": link,
            "source": "The Optimist Daily",
            "summary": None
        })
    return headlines



def get_random_happy_news(limit=5):
    """ Collect all News Headlines and randomize into just five. """
    all_articles = get_happy_news() + get_positive_news() + get_optimist_daily()
    random.shuffle(all_articles)
    return all_articles[:limit]



def remove_duplicates(articles):
    """ Function to make sure there are no duplicate headlines shown. """
    seen = set()
    unique_articles = []

    for article in articles:
        key = article["headline"].strip().lower()
        if key not in seen:
            seen.add(key)
            unique_articles.append(article)

    return unique_articles



def fetch_and_cache_news():
    """Fetches new headlines, compares them to the cache, sends push if changed, and updates cache."""
    new_articles = get_happy_news() + get_positive_news() + get_optimist_daily()
    new_articles = remove_duplicates(new_articles)
    random.shuffle(new_articles)

    # Load cached articles if present
    cached_articles = []
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, "r") as f:
            try:
                cached_data = json.load(f)
                cached_articles = cached_data["articles"]
            except:
                pass

    # Compare and push if the articles changed
    if new_articles != cached_articles:
        print("New headlines detected — sending push.")
        try:
            send_push_notification(
                "🌞 Here's some good news!",
                new_articles[0]["headline"]
            )
        except Exception as e:
            print(f"❌ Failed to send push notification: {e}")
    else:
        print("Headlines unchanged — no push sent.")

    # Update the cache regardless
    data = {
        "timestamp": datetime.utcnow().isoformat(),
        "articles": new_articles
    }

    with open(CACHE_FILE, "w") as f:
        json.dump(data, f)

    return new_articles



def get_cached_news():
    """ Function to retrieve cached news. """
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, "r") as f:
            data = json.load(f)

        timestamp = datetime.fromisoformat(data["timestamp"])
        if datetime.utcnow() - timestamp < timedelta(hours=CACHE_EXPIRY_HOURS):
            return data["articles"]

    # If no cache or expired
    return fetch_and_cache_news()



def get_random_happy_news(limit=5):
    """ Expose News. """
    articles = get_cached_news()
    random.shuffle(articles)
    return articles[:limit]



