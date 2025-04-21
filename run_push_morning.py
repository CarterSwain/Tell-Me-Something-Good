from app import create_app, db
from app.scraper import fetch_and_cache_news


app = create_app()

with app.app_context():
    fetch_and_cache_news(
        title="☀️ Good Morning!",
        body="Start your day with a smile and a headline."
    )
