from flask import Blueprint, jsonify, request
from .scraper import get_random_happy_news
from .firebase_util import send_push_notification

main = Blueprint('main', __name__)

# Temporary in-memory store (you can replace with a database)
REGISTERED_TOKENS = set()

@main.route('/api/news')
def news():
    limit = request.args.get("limit", default=5, type=int)
    return jsonify(get_random_happy_news(limit))


# Register a user's Expo push token
@main.route('/register_token', methods=["POST"])
def register_token():
    data = request.json
    token = data.get("token")

    if not token or not token.startswith("ExponentPushToken["):
        return jsonify({"error": "Invalid Expo token"}), 400

    REGISTERED_TOKENS.add(token)
    print(f"✅ Registered Expo token: {token}")
    return jsonify({"message": "Token registered successfully!"}), 200

# Check if a user's Expo push token. Remove if found.
@main.route('/unregister_token', methods=["POST"])
def unregister_token():
    data = request.json
    token = data.get("token")

    if not token:
        return jsonify({"error": "Missing token"}), 400

    if token in REGISTERED_TOKENS:
        REGISTERED_TOKENS.remove(token)
        print(f"🗑️ Unregistered Expo token: {token}")
        return jsonify({"message": "Token unregistered successfully."}), 200
    else:
        return jsonify({"message": "Token not found."}), 404



# 📬 Send a push to a specific token
@main.route('/send_push', methods=["POST"])
def send_push():
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


# 🌍 Broadcast to all registered tokens
@main.route('/broadcast_push', methods=["POST"])
def broadcast_push():
    data = request.json
    title = data.get("title", "📰 Daily Good News!")
    body = data.get("body", "Something good just happened!")

    results = []
    for token in REGISTERED_TOKENS:
        try:
            result = send_push_notification(title, body, token)
            results.append(result)
        except Exception as e:
            print(f"❌ Failed to send to {token}: {e}")
            results.append({"token": token, "error": str(e)})

    return jsonify({"message": "Broadcast complete", "results": results}), 200
