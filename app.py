import os
from typing import Callable
from flask import Flask, request, jsonify

from user_ids import get_psn_user_id, get_steam_user_id

app = Flask("Profile Finder")

def get_platform(platform_func: Callable):
    username = request.args.get("username", "").strip()
    if not username:
        return jsonify(error="Missing `username` in query!"), 400

    try:
        user = platform_func(username.strip())
    except ValueError:
        return jsonify(error=f"Server Error retreiving username {username}"), 400

    if not user:
        return jsonify(error=f"Couldn't find user {user}"), 404

    return jsonify(user_id=user)

@app.get("/platform/psn")
def get_psn():
    return get_platform(get_psn_user_id)

@app.get("/platform/steam")
def get_steam():
    return get_platform(get_steam_user_id)

@app.get("/platform/hydra")
def get_hydra():
    return jsonify(error="Not yet implemented"), 503

@app.get("/find")
def find_any():
    username = request.args.get("username", "").strip()
    if not username:
        return jsonify(error="Missing `username` in query!"), 400
    
    platform = request.args.get("platform", "").strip().lower()
    if not platform:
        return jsonify(error="Missing `platform` in query!"), 400
    
    if platform == "psn":
        return get_psn()
    elif platform == "steam":
        return get_steam()
    elif platform == "hydra":
        return get_hydra()
    
    return jsonify(error=f"Unsupported platform `{platform}`"), 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))
