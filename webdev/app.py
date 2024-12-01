#Import necessary libraries
#type: ignore
import os
import folium
import signal
import time
import pandas as pd
from ridge_model import train_ridge_model  #Import the Ridge model training function
from random_forest_model import train_random_forest_model  #Import the Random Forest training function
from flask import Flask, render_template, request  #Flask framework for web app creation
from geopy.distance import geodesic  #Geopy library to calculate distances
from folium.plugins import HeatMap  #Folium plugin for heatmap visualization

#Initialize the Flask application
app = Flask(__name__)

#Function to load data from a file
def get_data():
    file_path = "webdev/data/dynamic_dataset.csv"
    data = pd.read_csv(file_path)
    return data

#Create the output folder for maps if it doesn't exist
output_folder = "static/maps"
os.makedirs(output_folder, exist_ok=True)

#Route to find the nearest data point to a clicked location
@app.route('/get_nearest_data', methods=['POST'])
def get_nearest_data():
    #Load the dataset
    data = get_data()

    #Get the clicked point's latitude and longitude from the request
    clicked_point = request.json
    click_lat = clicked_point['latitude']
    click_lng = clicked_point['longitude']
    
    #Function to calculate the geodesic distance between two points
    def calculate_distance(row):
        return geodesic((row['latitude'], row['longitude']), (click_lat, click_lng)).miles

    #Apply the distance calculation to all rows and find the nearest one
    data['distance'] = data.apply(calculate_distance, axis=1)
    nearest_row = data.loc[data['distance'].idxmin()]
    
    #Return the nearest row as a JSON object
    return nearest_row.to_json()

#Route to get heatmap data for a selected year
@app.route('/get_heatmap_data', methods=['POST'])
def get_heatmap_data():
    #Get the selected year from the request
    selected_year = request.json['year']

    #Load the dataset
    data = get_data()

    #Check if the selected year exists in the dataset
    if selected_year not in data.columns:
        return {'error': f'Year {selected_year} is not available in the dataset.'}, 400

    #Extract relevant data for the heatmap
    heatmap_data = data[['latitude', 'longitude', selected_year]].dropna()
    heatmap_list = heatmap_data.values.tolist()

    #Return the heatmap data as a JSON response
    return {'heatmap_data': heatmap_list}, 200

#Route to render the index page
@app.route('/')
def index():
    #Load the dataset and extract available years
    data = get_data()
    years = [col for col in data.columns if col.isdigit()]
    return render_template('index.html', years=years)

#Route to generate a heatmap for a selected year
@app.route('/generate_heatmap', methods=['POST'])
def generate_heatmap():
    #Get the selected year from the form data
    selected_year = request.form['year']

    #Load the dataset
    data = get_data()

    #Check if the selected year exists in the dataset
    if selected_year not in data.columns:
        return f"Year {selected_year} is not available in the dataset."
    print(selected_year, " found in dataset")

    #Extract data for heatmap generation
    heatmap_data = data[['latitude', 'longitude', selected_year]].dropna()
    heatmap_list = heatmap_data.values.tolist()

    #Create a folium map centered on Florida
    florida_map = folium.Map(location=[27.994402, -81.760254], zoom_start=7)

    #Add the heatmap layer to the map
    HeatMap(heatmap_list, radius=15).add_to(florida_map)

    #Save the generated heatmap to a file
    output_file = os.path.join('static', 'maps', f"florida_heatmap_{selected_year}.html")
    florida_map.save(output_file)

    #Render the map in the template
    return render_template('map.html', year=selected_year, map_file=f"maps/florida_heatmap_{selected_year}.html")

#Route to render the Random Forest training page
@app.route('/train_random_forest')
def train_rf():
    return render_template('train_rf.html')

#Route to render the Ridge Regression training page
@app.route('/train_ridge_regression')
def train_rr():
    return render_template('train_rr.html')

#Route to handle Ridge Regression model training
@app.route('/train_model_rr', methods=['POST'])
def train_model_rr():
    print("starting training")

    #Check if a file was uploaded
    if 'file' not in request.files:
        return "No file uploaded", 400

    file = request.files['file']
    if file.filename == '':
        return "No selected file", 400

    #Save the uploaded file
    file_path = os.path.join('uploads', file.filename)
    os.makedirs('uploads', exist_ok=True)
    file.save(file_path)

    try:
        #Load the data and train the Ridge Regression model
        data = pd.read_csv(file_path)
        print(data.head())
        trained_model = train_ridge_model(data)
        return "Model trained successfully!", 200
    except Exception as e:
        return f"An error occurred: {e}", 500

#Route to handle Random Forest model training
@app.route('/train_model_rf', methods=['POST'])
def train_model_rf():
    print("starting training")

    #Check if a file was uploaded
    if 'file' not in request.files:
        return "No file uploaded", 400

    file = request.files['file']
    if file.filename == '':
        return "No selected file", 400

    #Save the uploaded file
    file_path = os.path.join('uploads', file.filename)
    os.makedirs('uploads', exist_ok=True)
    file.save(file_path)

    try:
        #Load the data and train the Random Forest model
        data = pd.read_csv(file_path)
        print(data.head())
        trained_model = train_random_forest_model(data)  #Call the imported function
        return "Model trained successfully!", 200
    except Exception as e:
        return f"An error occurred: {e}", 500

#Route to reset the dataset to its original state
@app.route('/reset_dataset', methods=['POST'])
def reset_dataset():
    try:
        #Restore the original dataset
        cleaned_file_path = "webdev/data/dynamic_dataset.csv"
        untouched_file_path = "webdev/data/original_dataset.csv"
        untouched_data = pd.read_csv(untouched_file_path)
        untouched_data.to_csv(cleaned_file_path, index=False)

        return '', 204  #Return no content on success
    except Exception as e:
        return f"An error occurred: {e}", 500

#Route to shut down the server
@app.route('/shutdown', methods=['POST'])
def shutdown():
    #Function to delay shutdown to allow for a response
    def delayed_shutdown():
        time.sleep(3)  
        os.kill(os.getpid(), signal.SIGINT)

    from threading import Thread
    Thread(target=delayed_shutdown).start()

#Main entry point to run the Flask application
if __name__ == '__main__':
    app.run(debug=True)
