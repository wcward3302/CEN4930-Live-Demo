# CEN4930-Live-Demo
[![OpenSSF Scorecard](https://api.securityscorecards.dev/projects/github.com/wcward3302/CEN4930-Live-Demo/badge)](https://securityscorecards.dev/viewer/?uri=github.com/wcward3302/CEN4930-Live-Demo)

[![OpenSSF Best Practices](https://www.bestpractices.dev/projects/10328/badge)](https://www.bestpractices.dev/projects/10328)

Repo for Flask server which will run frontend and AI model training for soil organic carbon level mapping and prediction. Final output demo is hosted on AWS EC2 instance, as shown here.

https://github.com/user-attachments/assets/df5cbf91-9c60-4856-9f9f-e64d1bea2a1e



# Members
- William Ward
- Alyssa Chiego
- Joshua Wurtenberg
- Caleb Newman
- Julio Lapon
- Jonathan Howard
- Arnulfo Villicana
- Niel Patel

# Machine Learning Web Application

This repository contains a web application for training and predicting using machine learning models. The application is built using Flask and includes functionalities for data visualization and model training.

## Project Structure

- **app.py**: Main Flask application file that handles routing and server logic.
- **dynamic_dataset.csv**: The dataset used for generating the heat map.
- **static/**: Directory containing CSS and JavaScript files.
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
    source venv/bin/activate  # On Windows use `venv\Scripts\activate` or .\venv\Scripts\activate
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
- **Train Model**: Offer the ability to train a model with a provided dataset (please use the 'download file' link as the data to train the model, as this is a demo only)
- **Generate Heatmap**: Visualize data on a heatmap based on the selected year.
- **Reset Dataset**: Reset the dataset to its original state.

## License

This project is licensed under the MIT License.
