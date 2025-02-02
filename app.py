from flask import Flask, render_template, request, redirect
import pandas as pd
import requests
import json

app = Flask(__name__)

# Route for the home page
@app.route('/')
def index():
    return render_template('index.html')

# Route for handling the questionnaire submission
@app.route('/submit', methods=['POST'])
def submit():
    # Collecting data from the form
    land_size = float(request.form.get('land_size'))
    num_habitats = int(request.form.get('num_habitats'))
    native_species = int(request.form.get('native_species'))

    # Process and store the data
    questionnaire_data = {
        'land_size': land_size,
        'num_habitats': num_habitats,
        'native_species': native_species
    }

    # Fetch CBS data and combine it with the questionnaire data
    cbs_data = fetch_cbs_data()

    # Compute biodiversity score
    biodiversity_score = compute_biodiversity_score(questionnaire_data, cbs_data)

    # Return results to the user
    return render_template('results.html', questionnaire_data=questionnaire_data, cbs_data=cbs_data, biodiversity_score=biodiversity_score)

def fetch_cbs_data():
    # Example CBS data URL (replace with actual API endpoint or correct CSV)
    url = "https://opendata.cbs.nl/ODataApi/odata/80783ned"  # CBS data API endpoint
    response = requests.get(url)

    if response.status_code == 200:
        cbs_json = response.json()
        return cbs_json
    else:
        return {"error": "Failed to fetch CBS data"}

def compute_biodiversity_score(questionnaire_data, cbs_data):
    # Example scoring logic based on questionnaire and CBS data
    # This needs to be adapted based on the specific scoring criteria from the user guide

    land_size = questionnaire_data['land_size']
    num_habitats = questionnaire_data['num_habitats']
    native_species = questionnaire_data['native_species']

    # Initialize biodiversity score
    score = 0

    # Basic scoring logic (this can be expanded based on the user guide)
    score += land_size * 0.5  # Weight for land size
    score += num_habitats * 2  # Weight for number of habitats
    score += native_species * 1  # Weight for native species count

    # Further adjustments can be made based on CBS data
    if 'value' in cbs_data:
        # Example: Adjust score based on specific CBS metrics if available
        cbs_metric = cbs_data['value']  # Assuming there is a relevant metric
        score += cbs_metric * 0.1  # Example adjustment

    return score

if __name__ == '__main__':
    app.run(debug=True)
