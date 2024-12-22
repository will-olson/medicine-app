from flask import Flask, request, jsonify
import requests
from config import db, create_app
from models import DrugSearchLog, AdverseEvent, DrugRecall

app = create_app()


@app.route("/search", methods=["GET"])
def search_drug():
    query = request.args.get("query")
    if not query:
        return jsonify({"error": "Query parameter is required"}), 400

    
    rxnav_url = f"{app.config['RXNORM_API_BASE_URL']}/drugs.json?name={query}"
    try:
        rxnav_response = requests.get(rxnav_url)
        rxnav_response.raise_for_status()
        drug_data = rxnav_response.json()
    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Error fetching drug data: {str(e)}"}), 500

    
    new_log = DrugSearchLog(query=query, response_data=drug_data)
    db.session.add(new_log)
    db.session.commit()

    return jsonify(drug_data)

@app.route("/interactions", methods=["POST"])
def check_interactions():
    drug_list = request.json.get("drugs")
    if not drug_list:
        return jsonify({"error": "Drug list is required"}), 400

    interaction_url = f"{app.config['RXNORM_API_BASE_URL']}/interaction/list.json?rxcuis={','.join(drug_list)}"
    try:
        interaction_response = requests.get(interaction_url)
        interaction_response.raise_for_status()
        interaction_data = interaction_response.json()
    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Error fetching interaction data: {str(e)}"}), 500

    return jsonify(interaction_data)

@app.route("/adverse-events", methods=["GET"])
def adverse_events():
    drug_name = request.args.get("drug_name")
    if not drug_name:
        return jsonify({"error": "Drug name is required"}), 400

    
    openfda_url = f"{app.config['OPENFDA_API_BASE_URL']}/drug/event.json?search=patient.drug.medicinalproduct:{drug_name}"
    try:
        response = requests.get(openfda_url, headers={"Authorization": app.config['OPENFDA_API_KEY']})
        response.raise_for_status()
        event_data = response.json()
    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Error fetching adverse event data: {str(e)}"}), 500

    if not event_data.get("results"):
        return jsonify({"error": "No adverse event data found"}), 404

    
    for event in event_data.get("results", []):
        new_event = AdverseEvent(
            drug_name=drug_name,
            event_description=event.get("reaction", "No description available"),
            demographics=event.get("patient", {}).get("patientonsetage", "Unknown")
        )
        db.session.add(new_event)

    db.session.commit()
    return jsonify(event_data)

@app.route("/recalls", methods=["GET"])
def drug_recalls():
    recall_url = f"{app.config['OPENFDA_API_BASE_URL']}/drug/enforcement.json"
    try:
        response = requests.get(recall_url, headers={"Authorization": app.config['OPENFDA_API_KEY']})
        response.raise_for_status()
        recall_data = response.json()
    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Error fetching recall data: {str(e)}"}), 500

    if not recall_data.get("results"):
        return jsonify({"error": "No recall data found"}), 404

    return jsonify(recall_data)

if __name__ == "__main__":
    app.run(debug=True)
