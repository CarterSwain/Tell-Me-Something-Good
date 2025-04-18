from flask import Blueprint, jsonify, request
from .scraper import get_random_happy_news
from .firebase_util import send_push_notification 

main = Blueprint('main', __name__)

@main.route('/api/news')
def news():
    limit = request.args.get("limit", default=5, type=int)
    return jsonify(get_random_happy_news(limit))

# Route to send a push notification
@main.route('/send_push', methods=["POST"])
def send_push():
    data = request.json

    title = data.get("title", "🌞 Here's your good news!")
    body = data.get("body", "A moment of joy is coming your way.")

    try:
        response = send_push_notification(title, body)
        return jsonify({"message": "Notification sent!", "id": response}), 200
    except Exception as e:
        print("❌ Push error:", e)
        return jsonify({"error": str(e)}), 500
