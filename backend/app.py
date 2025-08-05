from flask import Flask, request, jsonify, redirect
from datetime import datetime, timedelta
import string, random
from logging_middleware import Log
from flask_cors import CORS




app = Flask(__name__)
CORS(app)

# === CONFIGURATION ===
url_store = {}
DEFAULT_EXPIRY_MINUTES = 30
BASE_URL = "http://localhost:5000/"

def generate_shortcode(length=6):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def is_valid_shortcode(code):
    return code.isalnum() and 4 <= len(code) <= 20

# === MAIN SHORTEN URL ENDPOINT ===
@app.route('/api/v1/urls/shorten', methods=['POST'])
def shorten_url():
    try:
        data = request.get_json()
        original_url = data.get("url")
        custom_code = data.get("customCode")
        expires_at = data.get("expiresAt")  # optional ISO string

        if not original_url:
            return jsonify({"success": False, "error": "Missing URL"}), 400

        if expires_at:
            expiry_time = datetime.fromisoformat(expires_at.replace("Z", ""))
        else:
            expiry_time = datetime.utcnow() + timedelta(minutes=DEFAULT_EXPIRY_MINUTES)

        if custom_code:
            if not is_valid_shortcode(custom_code):
                return jsonify({"success": False, "error": "Invalid shortcode"}), 400
            if custom_code in url_store:
                return jsonify({"success": False, "error": "Shortcode already exists"}), 409
            shortcode = custom_code
        else:
            while True:
                shortcode = generate_shortcode()
                if shortcode not in url_store:
                    break

        url_store[shortcode] = {
            "url": original_url,
            "created": datetime.utcnow(),
            "expiry": expiry_time,
            "clicks": 0,
            "click_details": []
        }

        Log("backend", "info", "shorten", f"Created: {shortcode}")

        response_data = {
            "shortUrl": BASE_URL + shortcode,
            "shortCode": shortcode,
            "originalUrl": original_url,
            "qrCode": None,  # Not implemented
            "createdAt": datetime.utcnow().isoformat() + "Z"
        }

        return jsonify({"success": True, "data": response_data}), 201

    except Exception as e:
        Log("backend", "fatal", "shorten", f"Error: {str(e)}")
        return jsonify({"success": False, "error": "Internal Server Error"}), 500

# === REDIRECT SHORT URL ===
@app.route('/<shortcode>', methods=['GET'])
def redirect_to_url(shortcode):
    entry = url_store.get(shortcode)
    if not entry:
        return jsonify({"error": "Shortcode does not exist"}), 404

    if datetime.utcnow() > entry["expiry"]:
        return jsonify({"error": "Shortcode expired"}), 410

    entry["clicks"] += 1
    entry["click_details"].append({
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "referer": request.headers.get("Referer", "direct")
    })

    return redirect(entry["url"], code=302)


@app.route('/shorturls/<shortcode>', methods=['GET'])
def get_stats(shortcode):
    entry = url_store.get(shortcode)
    if not entry:
        return jsonify({"error": "Shortcode does not exist"}), 404

    return jsonify({
        "url": entry["url"],
        "created": entry["created"].isoformat() + "Z",
        "expiry": entry["expiry"].isoformat() + "Z",
        "clicks": entry["clicks"],
        "click_details": entry["click_details"]
    })

# === HEALTH CHECK ===
@app.route('/')
def home():
    return jsonify({"message": "URL Shortener running"}), 200

if __name__ == '__main__':
    app.run(debug=True)
