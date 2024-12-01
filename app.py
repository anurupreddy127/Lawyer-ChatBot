import requests
from flask import Flask, request, jsonify, render_template

# Flask application setup
app = Flask(__name__)

# Congress.gov API configuration
# Replace with your actual API key
API_KEY = "62IOPonysOx2wbWE1rawvQaf02ufD09zOlSgWrvK"
BASE_URL = "https://api.congress.gov/v3"


@app.route("/")
def home():
    """
    Root route to render the index.html page.
    """
    return render_template("index.html")


@app.route("/get_law", methods=["GET"])
def get_law():
    """
    Endpoint to fetch legal data from the Congress.gov API based on a query.
    """
    query = request.args.get("query")
    if not query:
        return jsonify({"error": "Query parameter is required"}), 400

    # Call Congress.gov API
    url = f"{BASE_URL}/bill?search={query}"
    headers = {"X-Api-Key": API_KEY}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        bills = data.get("bills", [])
        formatted_bills = []

        # Format the data to exclude the URL field
        for bill in bills:
            formatted_bills.append({
                "title": bill.get("title", "No title available"),
                "number": bill.get("number", "No number available"),
                "congress": bill.get("congress", "No congress session info"),
                "originChamber": bill.get("originChamber", "Unknown"),
                "latestAction": bill.get("latestAction", {}).get("text", "No recent action")
            })

        return jsonify({"query": query, "results": formatted_bills})
    else:
        return jsonify({"error": f"Unable to fetch data. Status code: {response.status_code}"}), response.status_code


if __name__ == "__main__":
    # Run the Flask app in debug mode
    app.run(debug=True)
