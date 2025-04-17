# run_cache.py
from app.scraper import fetch_and_cache_news
from datetime import datetime

def log(msg):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{now}] {msg}")

if __name__ == "__main__":
    log("Cache update started...")

    try:
        articles = fetch_and_cache_news()
        log(f"Cache update completed successfully. {len(articles)} articles saved.")
    except Exception as e:
        log(f"Cache update failed: {e}")
