from flask import Flask, request, jsonify, render_template
import phonenumbers
from phonenumbers import carrier, geocoder, timezone

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/track", methods=["POST"])
def track_number():
    data = request.get_json()
    phone_number = data.get("number")

    try:
        parsed_number = phonenumbers.parse(phone_number)
        country = geocoder.description_for_number(parsed_number, "en")
        service_provider = carrier.name_for_number(parsed_number, "en")
        time_zones = timezone.time_zones_for_number(parsed_number)

        return jsonify({
            "status": "success",
            "country": country,
            "carrier": service_provider,
            "timezones": list(time_zones)
        })

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400

if __name__ == "__main__":
    app.run(debug=True)
