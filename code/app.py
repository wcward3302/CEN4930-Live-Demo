#type: ignore
import os
import folium
import signal
import time
import pandas as pd
from ridge_model import train_model, generate_data  
from flask import Flask, render_template, request 
from geopy.distance import geodesic  
from folium.plugins import HeatMap  

app = Flask(__name__)

def get_data():
    file_path = "data/dynamic_dataset.csv"
    data = pd.read_csv(file_path)
    return data

output_folder = "code/static/maps"
os.makedirs(output_folder, exist_ok=True)


@app.route('/get_nearest_data', methods=['POST'])
def get_nearest_data():
    data = get_data()
    clicked_point = request.json
    click_lat = clicked_point['latitude']
    click_lng = clicked_point['longitude']
    def calculate_distance(row):
        return geodesic((row['latitude'], row['longitude']), (click_lat, click_lng)).miles
    data['distance'] = data.apply(calculate_distance, axis=1)
    nearest_row = data.loc[data['distance'].idxmin()]
    return nearest_row.to_json()


@app.route('/get_heatmap_data', methods=['POST'])
def get_heatmap_data():
    selected_year = request.json['year']
    data = get_data()
    if selected_year not in data.columns:
        return {'error': f'Year {selected_year} is not available in the dataset.'}, 400
    heatmap_data = data[['latitude', 'longitude', selected_year]].dropna()
    heatmap_list = heatmap_data.values.tolist()
    return {'heatmap_data': heatmap_list}, 200


@app.route('/')
def index():
    data = get_data()
    years = [col for col in data.columns if col.isdigit()]
    return render_template('index.html', years=years)


@app.route('/generate_heatmap', methods=['POST'])
def generate_heatmap():
    selected_year = request.form['year']
    data = get_data()
    if selected_year not in data.columns:
        return f"Year {selected_year} is not available in the dataset."
    print(selected_year, " found in dataset")
    heatmap_data = data[['latitude', 'longitude', selected_year]].dropna()
    heatmap_list = heatmap_data.values.tolist()
    florida_map = folium.Map(location=[27.994402, -81.760254], zoom_start=7)
    HeatMap(heatmap_list, radius=15).add_to(florida_map)
    output_file = os.path.join('code','static', 'maps', f"florida_heatmap_{selected_year}.html")
    florida_map.save(output_file)
    return render_template('map.html', year=selected_year, map_file=f"maps/florida_heatmap_{selected_year}.html")


@app.route('/train_model')
def train_rf():
    return render_template('train.html')


@app.route('/generate_prediction')
def generate_prediction():
    return render_template('generate_predictions.html')


@app.route('/train_model', methods=['POST'])
def train_model_func():
    print("starting training")
    if 'file' not in request.files:
        return "No file uploaded", 400
    file = request.files['file']
    if file.filename == '':
        return "No selected file", 400
    file_path = os.path.join('uploads', file.filename)
    os.makedirs('uploads', exist_ok=True)
    file.save(file_path)
    try:
        data = pd.read_csv(file_path)
        print(data.head())
        train_model(data) 
        return "Model trained successfully!", 200
    except Exception as e:
        return f"An error occurred: {e}", 500


@app.route('/generate_prediction_data', methods=['POST'])
def generate_prediction_data():
    print("starting generation")
    if 'file' not in request.files:
        return "No file uploaded", 400
    file = request.files['file']
    if file.filename == '':
        return "No selected file", 400
    file_path = os.path.join('uploads', file.filename)
    os.makedirs('uploads', exist_ok=True)
    file.save(file_path)
    try:
        data = pd.read_csv(file_path)
        print(data.head())
        generate_data(data)  
        return "Model generated data successfully!", 200
    except Exception as e:
        return f"An error occurred: {e}", 500

@app.route('/reset_dataset', methods=['POST'])
def reset_dataset():
    try:
        cleaned_file_path = "data/dynamic_dataset.csv"
        untouched_file_path = "data/original_dataset.csv"
        untouched_data = pd.read_csv(untouched_file_path)
        untouched_data.to_csv(cleaned_file_path, index=False)
        return '', 200  
    except Exception as e:
        return f"An error occurred: {e}", 500

@app.route('/shutdown', methods=['POST'])
def shutdown():
    def delayed_shutdown():
        time.sleep(3)  
        os.kill(os.getpid(), signal.SIGINT)
    from threading import Thread
    Thread(target=delayed_shutdown).start()

@app.route('/download')
def download_file():
    path = "../data/original_dataset.csv"
    return send_file(path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
