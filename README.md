# 🌞 Tell Me Something Good

A feel-good Python/Flask API that scrapes heartwarming headlines from multiple positive news sources like Good News Network, Positive News, and The Optimist Daily.

Designed to power a mobile app that delivers a daily boost of joy — complete with randomized stories, caching, and push notification support.


## Deployed @:

**Backend URL:**  
👉 https://tell-me-something-good.fly.dev/api/news

---

## Features

- Scrapes articles from 3 curated sources of good news
- Returns a randomized selection of uplifting headlines
- Caches results daily to avoid repeat scraping
- Optional `?limit=10` param for custom batch sizes
- Filters out duplicate stories based on headline text
- Simple JSON API, built with Flask

---

## How It Works

The backend scrapes stories using BeautifulSoup, merges and deduplicates them, then returns a fresh mix of headlines via a `/api/news` endpoint.

Cached results are stored in a JSON file and refreshed every 24 hours using a cron job.


---

## Tech Stack

| Layer        | Technology                        |
|--------------|-----------------------------------|
| Backend      | Python, Flask, BeautifulSoup      |
| Scraping     | BeautifulSoup                     |
| Scheduling   | Cron Job or APScheduler           |
| Frontend     | React Native (coming soon)        |
| Notifications| Expo Push API (in progress)       |
| Database     | PostgreSQL                        |
| Deployment   | Fly.io                            |

---

## 🧪 Example API Call

```http
GET /api/news?limit=5 
```

---

### Example Response:

```json
[
  {
    "headline": "Zoo Camera Captures Elephants Protecting Their Young During San Diego Earthquake",
    "link": "https://www.goodnewsnetwork.org/zoo-camera-captures-elephants-protecting-their-young-during-san-diego-earthquake-watch/",
    "source": "Good News Network",
    "summary": null
  }
]
```

---

### Setup: 

1. Clone Repo:

git clone https://github.com/CarterSwain/Tell-Me-Something-Good.git
cd Tell-Me-Something-Good

2. Create a Virtual Environment:

python -m venv venv
source venv/bin/activate

3. Install Dependencies:

pip install -r requirements.txt

4. Run the Server:

python3 run.py

5. Visit the API:

http://localhost:5000/api/news


---

### Coming Soon:

- React Native frontend with a swipeable list of stories

- Expo Push notifications

--- 

### Sources:

Good News Network ( https://www.goodnewsnetwork.org/ )

Positive News ( https://www.positive.news/ )

The Optimist Daily ( https://www.optimistdaily.com/ )