from flask import Blueprint, jsonify, request
from .scraper import get_random_happy_news

main = Blueprint('main', __name__)

@main.route('/api/news')
def news():
    limit = request.args.get("limit", default=5, type=int)
    return jsonify(get_random_happy_news(limit))