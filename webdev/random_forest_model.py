#Import necessary libraries
#type: ignore   
import os
import joblib
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error, r2_score

def train_random_forest_model(data):
    #Add a new column '2029' to the dataset, calculated using linear extrapolation
    data['2029'] = data['2024'] - (data['2019'] - data['2024'])

    #Define the feature columns (independent variables) and target column (dependent variable)
    X = data[['2014', '2019', '2024']]
    y = data['2029']

    #Split the data into training and testing sets (80% training, 20% testing)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    #Define the hyperparameter grid for the Random Forest model
    param_grid = {
        'n_estimators': [100, 200, 500],  #Number of trees in the forest
        'max_depth': [None, 10, 20, 30],  #Maximum depth of the tree
        'min_samples_split': [2, 5, 10],  #Minimum number of samples required to split a node
        'min_samples_leaf': [1, 2, 4]     #Minimum number of samples required at each leaf node
    }

    #Initialize the Random Forest Regressor
    rf = RandomForestRegressor(random_state=42)

    #Perform Grid Search with Cross Validation to find the best hyperparameters
    grid_search = GridSearchCV(estimator=rf, param_grid=param_grid, cv=3, 
                               scoring='neg_mean_squared_error', verbose=2, n_jobs=-1)

    #Fit the model to the training data
    grid_search.fit(X_train, y_train)

    #Extract the best model from the grid search
    best_rf_model = grid_search.best_estimator_

    #Fit the best model to the training data
    best_rf_model.fit(X_train, y_train)

    #Predict the target variable for the testing set
    y_pred = best_rf_model.predict(X_test)

    #Calculate the Mean Squared Error and R^2 Score for model evaluation
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)

    #Print the evaluation metrics
    print(f"Mean Squared Error: {mse}")
    print(f"R^2 Score: {r2}")

    #Calculate and display feature importances
    feature_importances = pd.DataFrame({
        'Feature': ['2014', '2019', '2024'], 
        'Importance': best_rf_model.feature_importances_
    }).sort_values(by='Importance', ascending=False)

    print("\nFeature Importances:")
    print(feature_importances)

    #Save the trained model to a file
    model_file = 'models/optimized_random_forest_2029_model.pkl'
    os.makedirs('models', exist_ok=True)  #Create the 'models' directory if it doesn't exist
    joblib.dump(best_rf_model, model_file)  #Save the model

    print(f"\nOptimized Random Forest model saved to {model_file}.")
    print(f"Running model to generate predictions - {model_file}")

    #Load the saved model for inference
    rf_model = joblib.load(model_file)

    #Generate predictions for the entire dataset
    input_features = data[['2014', '2019', '2024']]
    data['2029'] = rf_model.predict(input_features)

    #Round the predictions to one decimal place
    data['2029'] = data['2029'].round(1)

    #Save the updated dataset with predictions to a CSV file
    output_file_path = 'webdev/dynamic_dataset.csv'
    data.to_csv(output_file_path, index=False)

    print(f"Updated dataset saved to {output_file_path}")
