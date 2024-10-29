# Import necessary libraries
from flask import Flask, render_template, request
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import mean_squared_error, mean_absolute_error
import os
import logging

# Initialize Flask application
app = Flask(__name__)

# Set up logging
logging.basicConfig(filename='performance_metrics.log', level=logging.INFO, format='%(asctime)s - %(message)s')

# Load the healthcare dataset
df = pd.read_csv('healthcare_satisfaction_data.csv')

# Define features (X) and target (y) for the model
X = df[['Gender', 'Age', 'Condition Type', 'Previous Satisfaction']]
y = df['Predicted Outcome']

# Preprocess categorical and numerical data
preprocessor = ColumnTransformer(
    transformers=[
        ('cat', OneHotEncoder(), ['Gender', 'Condition Type']),
    ],
    remainder='passthrough'
)

# Create a pipeline combining preprocessing and linear regression
model = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('regressor', LinearRegression())
])

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
model.fit(X_train, y_train)

# Make predictions on the test set
y_pred = model.predict(X_test)

# Calculate performance metrics
mse = mean_squared_error(y_test, y_pred)
mae = mean_absolute_error(y_test, y_pred)

# Log performance metrics
logging.info(f'Mean Squared Error (MSE): {mse:.4f}')
logging.info(f'Mean Absolute Error (MAE): {mae:.4f}')

# Define Flask routes
@app.route('/', methods=['GET', 'POST'])
def predict_satisfaction():
    predicted_value = None
    if request.method == 'POST':
        gender = request.form['gender']
        age = int(request.form['age'])
        condition = request.form['condition']
        previous_satisfaction = float(request.form['previous_satisfaction'])

        input_data = pd.DataFrame({
            'Gender': [gender],
            'Age': [age],
            'Condition Type': [condition],
            'Previous Satisfaction': [previous_satisfaction]
        })

        # Make a prediction
        predicted_value = model.predict(input_data)[0]
    
    return render_template('index.html', predicted_value=predicted_value)

# Run Flask app
if __name__ == '__main__':
    app.run(debug=True)
