import os

import redis
from flask import Flask, jsonify

app = Flask(__name__)
client = redis.Redis(
    host=os.environ.get("REDIS_HOST", "redis"),
    port=int(os.environ.get("REDIS_PORT", "6379")),
    decode_responses=True,
)


@app.route("/health")
def health():
    try:
        pong = client.ping()
    except Exception as exc:
        return jsonify({"status": "error", "redis": "down", "error": str(exc)}), 503
    return jsonify({"status": "ok", "redis": "up" if pong else "down"})


@app.route("/counter")
def counter():
    hits = client.incr("hits")
    return jsonify({"hits": hits})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
