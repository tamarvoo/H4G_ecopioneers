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
    land_size = request.form.get('land_size')
    num_habitats = request.form.get('num_habitats')
    native_species = request.form.get('native_species')

    # Process and store the data
    questionnaire_data = {
        'land_size': land_size,
        'num_habitats': num_habitats,
        'native_species': native_species
    }

    # Fetch CBS data and combine it with the questionnaire data
    cbs_data = fetch_cbs_data()

    # Return results to the user
    return render_template('results.html', questionnaire_data=questionnaire_data, cbs_data=cbs_data)

def fetch_cbs_data():
    # Example CBS data URL (replace with actual API endpoint or correct CSV)
    url = "https://opendata.cbs.nl/ODataApi/odata/80783ned"  # CBS data API endpoint
    response = requests.get(url)
    
    if response.status_code == 200:
        cbs_json = response.json()
        # You may want to convert this to a DataFrame for easier processing or filtering
        return cbs_json
    else:
        return {"error": "Failed to fetch CBS data"}

if __name__ == '__main__':
    app.run(debug=True)