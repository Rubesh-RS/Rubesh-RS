from flask import Flask, render_template, request, redirect, url_for, send_file
import pandas as pd
import matplotlib.pyplot as plt
import os
from sklearn.linear_model import LinearRegression
import numpy as np

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
PLOT_FOLDER = 'static/plots'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PLOT_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "No file part"
    file = request.files['file']
    if file.filename == '':
        return "No selected file"
    
    # Save the uploaded file
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)
    
    # Process the file and generate plot
    predicted_value, plot_path = process_and_plot(file_path)
    
    return render_template('result.html', plot_url=plot_path, prediction=predicted_value)

def process_and_plot(file_path):
    # Load the Excel file into a DataFrame
    df = pd.read_excel(file_path)
    
    # Assuming the data is in a column named 'Value'
    if 'Value' not in df.columns:
        return "Column 'Value' not found in the Excel file", None
    data = df['Value'].values
    
    # Generate x values
    x = np.arange(len(data)).reshape(-1, 1)
    y = data.reshape(-1, 1)
    
    # Train a linear regression model
    model = LinearRegression()
    model.fit(x, y)
    
    # Predict the next step
    next_step = len(data)
    predicted_value = model.predict([[next_step]])[0][0]
    
    # Generate the plot
    plt.figure(figsize=(10, 6))
    plt.plot(data, label='Original Data', marker='o')
    plt.plot(next_step, predicted_value, 'ro', label='Next Prediction')
    plt.axhline(y=predicted_value, color='r', linestyle='--', alpha=0.5)
    plt.title('Data and Prediction')
    plt.xlabel('Steps')
    plt.ylabel('Value')
    plt.legend()
    
    # Save the plot
    plot_filename = os.path.join(PLOT_FOLDER, 'plot.png')
    plt.savefig(plot_filename)
    plt.close()
    
    return predicted_value, plot_filename

if __name__ == '__main__':
    app.run(debug=True)
