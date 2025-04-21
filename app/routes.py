from flask import Blueprint, jsonify, request
from .scraper import get_random_happy_news
from .firebase_util import send_push_notification
from .models import PushToken
from . import db
import os

main = Blueprint('main', __name__)

@main.route('/api/news')
def news():
    """Return a randomized list of happy news headlines."""
    limit = request.args.get("limit", default=5, type=int)
    return jsonify(get_random_happy_news(limit))


@main.route('/register_token', methods=["POST"])
def register_token():
    """Register a new Expo push token in the database."""
    data = request.json
    token = data.get("token")

    if not token or not token.startswith("ExponentPushToken["):
        return jsonify({"error": "Invalid Expo token"}), 400

    existing = PushToken.query.filter_by(token=token).first()
    if not existing:
        new_token = PushToken(token=token)
        db.session.add(new_token)
        db.session.commit()

    print(f"✅ Registered Expo token: {token}")
    return jsonify({"message": "Token registered successfully!"}), 200


@main.route('/unregister_token', methods=["POST"])
def unregister_token():
    """Unregister a previously saved Expo push token."""
    data = request.json
    token = data.get("token")

    if not token:
        return jsonify({"error": "Missing token"}), 400

    existing = PushToken.query.filter_by(token=token).first()
    if existing:
        db.session.delete(existing)
        db.session.commit()
        print(f"🗑️ Unregistered Expo token: {token}")
        return jsonify({"message": "Token unregistered successfully."}), 200
    else:
        return jsonify({"message": "Token not found."}), 404


@main.route('/send_push', methods=["POST"])
def send_push():
    """Send a push notification to a single Expo token."""
    data = request.json

    title = data.get("title", "🌞 Here's your good news!")
    body = data.get("body", "A moment of joy is coming your way.")
    token = data.get("token")

    if not token:
        return jsonify({"error": "Missing push token"}), 400

    try:
        response = send_push_notification(title, body, token)
        return jsonify({"message": "Notification sent!", "response": response}), 200
    except Exception as e:
        print("❌ Push error:", e)
        return jsonify({"error": str(e)}), 500


@main.route('/broadcast_push', methods=["POST"])
def broadcast_push():
    """Send a push notification to all registered Expo tokens."""
    data = request.json
    title = data.get("title", "📰 Daily Good News!")
    body = data.get("body", "Something good just happened!")

    tokens = PushToken.query.all()
    results = []

    for t in tokens:
        try:
            result = send_push_notification(title, body, t.token)
            results.append(result)
        except Exception as e:
            print(f"❌ Failed to send to {t.token}: {e}")
            results.append({"token": t.token, "error": str(e)})

    return jsonify({"message": "Broadcast complete", "results": results}), 200


# Dev-only route to debug stored tokens
if os.environ.get("FLASK_ENV") == "development":
    @main.route('/debug_tokens')
    def debug_tokens():
        """Return a list of all registered Expo push tokens (dev only)."""
        tokens = PushToken.query.all()
        print("🧪 /debug_tokens accessed")
        return jsonify({"tokens": [t.token for t in tokens]})
