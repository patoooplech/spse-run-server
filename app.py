from flask import Flask, request, jsonify
import json
import os

app = Flask(__name__)
DATA_FILE = "players.json"


def load_players():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_players(players):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(players, f, ensure_ascii=False, indent=2)


@app.route("/login", methods=["POST"])
def login():
    data = request.json
    players = load_players()

    for p in players:
        if p["meno"].lower() == data["username"].lower():
            if p["heslo"] == data["password"]:
                return jsonify(p)
            return "Unauthorized", 401

    new_player = {
        "meno": data["username"],
        "heslo": data["password"],
        "score": 0
    }
    players.append(new_player)
    save_players(players)
    return jsonify(new_player)


@app.route("/update_score", methods=["POST"])
def update_score():
    data = request.json
    players = load_players()

    for p in players:
        if p["meno"].lower() == data["username"].lower():
            p["score"] = max(p["score"], data["score"])
            save_players(players)
            return "OK"

    return "Not found", 404


@app.route("/leaderboard")
def leaderboard():
    limit = int(request.args.get("limit", 10))
    players = load_players()
    players.sort(key=lambda x: x["score"], reverse=True)
    return jsonify(players[:limit])


@app.route("/")
def home():
    return "SPSE RUN SERVER BEZI ✅"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
