from flask import Flask, request, jsonify
import os

app = Flask(__name__)

# ------------------------------
# Sample Data (Temporary DB)
# ------------------------------
DRUGS = {
    "1": {
        "id": "1",
        "name": "Paracetamol",
        "pros": ["Pain relief"],
        "cons": ["Liver damage (overdose)"],
        "source": "FDA",
        "last_updated": "2024-01-01"
    },
    "2": {
        "id": "2",
        "name": "Ibuprofen",
        "pros": ["Pain relief", "Anti-inflammatory"],
        "cons": ["Stomach irritation"],
        "source": "WHO",
        "last_updated": "2024-02-01"
    }
}

# ------------------------------
# Routes
# ------------------------------


# Get all drugs
@app.route("/api/v1/drugs")
def get_all_drugs():
    return jsonify(list(DRUGS.values()))

# Get one drug
@app.route("/api/v1/drugs/<drug_id>")
def get_drug(drug_id):
    record = DRUGS.get(drug_id)

    if not record:
        return jsonify({"error": "not_found"}), 404

    return jsonify(record)
@app.route("/")
def home():
    return jsonify({
        "message": "Drug API is running",
        "endpoints": [
            "/api/v1/drugs",
            "/api/v1/drugs/<id>",
            "/api/v1/search?q=name"
        ]
    })
# Search drugs
@app.route("/api/v1/search")
def search_drugs():
    query = request.args.get("q", "").lower()

    results = [
        drug for drug in DRUGS.values()
        if query in drug["name"].lower()
    ]

    return jsonify(results)

# ------------------------------
# Run App
# ------------------------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)