import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

# Replace with your Congress.gov API key
API_KEY = "62IOPonysOx2wbWE1rawvQaf02ufD09zOlSgWrvK"
BASE_URL = "https://api.congress.gov/v3"


@app.route("/get_law", methods=["GET"])
def get_law():
    query = request.args.get("query")
    if not query:
        return jsonify({"error": "Query parameter is required"}), 400

    # API Call
    url = f"{BASE_URL}/bill?search={query}"
    headers = {"X-Api-Key": API_KEY}
    response = requests.get(url, headers=headers)

    # Debugging Information
    print(f"Request URL: {url}")
    print(f"Response Status Code: {response.status_code}")
    print(f"Response Text: {response.text}")

    if response.status_code == 200:
        data = response.json()
        return jsonify(data)
    else:
        return jsonify({"error": f"Unable to fetch data. Status code: {response.status_code}"}), response.status_code


if __name__ == "__main__":
    app.run(debug=True)
