# CEN4930-Live-Demo
Repo for Flask server which will run front end and AI model training for soil organic carbon level mapping and prediction. 

![Screen Recording 2024-12-01 111450](https://github.com/user-attachments/assets/014c1233-fb8d-4b61-b7c1-2be42dcd11ef)

# Members
- William Ward
- Joshua Wurtenberg
- Caleb Newman

# Machine Learning Web Application

This repository contains a web application for training and predicting using machine learning models, specifically Ridge Regression and Random Forest. The application is built using Flask and includes functionalities for data visualization and model training.

## Project Structure

- **app.py**: Main Flask application file that handles routing and server logic.
- **dynamic_dataset.csv**: The dataset used for generating the heat map.
- **random_forest_model.py**: Script for training and predicting using a Random Forest model.
- **ridge_model.py**: Script for training and predicting using a Ridge Regression model.
- **templates/**: Directory containing HTML templates for the web application.
- **original_dataset.csv**: Original dataset before any modifications, used to train the models

## Setup

1. **Clone the repository**:
    ```sh
    git clone <repository-url>
    cd <repository-directory>
    ```

2. **Create a virtual environment**:
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install the dependencies**:
    ```sh
    pip install -r requirements.txt
    ```

## Running the Application

1. **Start the Flask server**:
    ```sh
    python code/app.py
    ```

2. **Open your browser** and navigate to `http://127.0.0.1:5000/` to access the application.

## Usage

- **Train Ridge Regression Model**: Upload a dataset and train a Ridge Regression model.
- **Train Random Forest Model**: Upload a dataset and train a Random Forest model.
- **Generate Heatmap**: Visualize data on a heatmap based on the selected year.
- **Reset Dataset**: Reset the dataset to its original state.

## Contributing

Feel free to submit issues or pull requests if you have any improvements or bug fixes.

## License

This project is licensed under the MIT License.
