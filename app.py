from functools import wraps
from flask import Flask, request, jsonify, g

app = Flask(__name__)

def verify_jwt(token):
    return {"sub": "user123", "role": "admin"}

class Drug:
    def __init__(self):
        self.id = "1"
        self.generic_name = "Paracetamol"
        self.approved_indications = ["Pain relief"]
        self.warnings_and_side_effects = ["Liver damage (overdose)"]
        self.authority_reference = "FDA"
        self.version_date = "2024-01-01"

class DrugCatalog:
    def get_by_id(self, drug_id):
        if drug_id == "1":
            return Drug()
        return None

drug_catalog = DrugCatalog()

class AuditLog:
    def write(self, **kwargs):
        print("Audit:", kwargs)

audit_log = AuditLog()

def require_auth(allowed_roles=("verified_reader", "clinician", "admin")):
    def decorator(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            token = request.headers.get("Authorization", "").replace("Bearer ", "")
            user = verify_jwt(token)

            if not user or user["role"] not in allowed_roles:
                return jsonify({"error": "forbidden"}), 403

            g.user = user
            return f(*args, **kwargs)
        return wrapped
    return decorator

@app.route("/api/v1/drugs/<drug_id>")
@require_auth()
def get_drug(drug_id):
    record = drug_catalog.get_by_id(drug_id)
    if not record:
        return jsonify({"error": "not_found"}), 404

    audit_log.write(user_id=g.user["sub"], action="read_drug", resource=drug_id)

    return jsonify({
        "id": record.id,
        "name": record.generic_name,
        "pros": record.approved_indications,
        "cons": record.warnings_and_side_effects,
        "source": record.authority_reference,
        "last_updated": record.version_date,
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)