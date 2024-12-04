#Import necessary libraries
#type: ignore   
from sklearn.linear_model import Ridge
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error, r2_score
import pandas as pd
import joblib
import os

def train_model(data):
    #Add a new column '2029' to the dataset, calculated using linear extrapolation
    data['2029'] = data['2024'] - (data['2019'] - data['2024'])

    #Define the feature columns (independent variables) and target column (dependent variable)
    X = data[['2014', '2019', '2024']]
    y = data['2029']

    #Standardize the feature values to have a mean of 0 and standard deviation of 1
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    #Split the data into training and testing sets (80% training, 20% testing)
    X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

    #Initialize the Ridge Regression model with a regularization parameter (alpha)
    model = Ridge(alpha=1.0)

    #Train the Ridge model on the training data
    model.fit(X_train, y_train)

    #Predict the target variable for the testing set
    y_pred = model.predict(X_test)

    #Calculate the Mean Squared Error and R^2 Score for model evaluation
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)

    #Print the evaluation metrics
    print(f"Mean Squared Error: {mse}")
    print(f"R^2 Score: {r2}")

    #Extract and display the coefficients of the trained Ridge model
    coefficients = pd.DataFrame({
        'Feature': ['2014', '2019', '2024'],  #Feature names
        'Coefficient': model.coef_           #Corresponding coefficients
    }).sort_values(by='Coefficient', ascending=False)

    print("\nFeature Coefficients:")
    print(coefficients)

    #Save the trained Ridge model to a file
    model_file = 'models/model.pkl'
    os.makedirs('models', exist_ok=True)  #Create the 'models' directory if it doesn't exist
    joblib.dump(model, model_file)  #Save the model


def generate_data(data):
    #Load the saved Ridge model for inference
    model_file = 'models/model.pkl'
    model = joblib.load(model_file)

    #Prepare a new DataFrame for generating predictions
    new_data_df = data

    #Extract input features for prediction
    input_features = new_data_df[['2014', '2019', '2024']]

    #Standardize the feature values
    scaler = StandardScaler()
    scaled_features = scaler.fit_transform(input_features)

    #Generate predictions using the Ridge model
    new_data_df['2029'] = model.predict(scaled_features)

    #Round the predictions to one decimal place
    new_data_df['2029'] = new_data_df['2029'].round(1)

    #Save the updated dataset with predictions to a CSV file
    output_file_path = 'data/dynamic_dataset.csv'
    new_data_df.to_csv(output_file_path, index=False)

    print(f"Updated dataset saved to {output_file_path}")
