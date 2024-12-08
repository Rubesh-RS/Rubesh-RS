#Author: updated 8_12_24
from flask import Flask, render_template, request, send_file
import pandas as pd
import matplotlib
matplotlib.use('Agg')  # Use Agg backend for non-GUI usage
import matplotlib.pyplot as plt
import os
from sklearn.linear_model import LinearRegression
import numpy as np
from datetime import datetime

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

@app.route('/', methods=['GET', 'POST'])
def index():
    plot_url = None

    if request.method == 'POST':
        dataset_choice = request.form['dataset']
        if dataset_choice == 'upload':
            if 'file' not in request.files:
                return "No file part"
            file = request.files['file']
            if file.filename == '':
                return "No selected file"
            if file:
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
                file.save(filepath)
                print(filepath)
                df = pd.read_excel(filepath)
        else:
            df = pd.read_excel('Valorant_Weapon_Usage_Summary.xlsx')

        # Convert 'Date' column to datetime
        df['Date'] = pd.to_datetime(df['Date'])

        # Predict the next step
        def predict_next_step(data):
            X = np.arange(len(data)).reshape(-1, 1)  # Day numbers
            y_vandal = data['Vandal_Users'].values
            y_phantom = data['Phantom_Users'].values

            model_vandal = LinearRegression()
            model_vandal.fit(X, y_vandal)
            next_vandal_users = model_vandal.predict([[len(data)]])[0]

            model_phantom = LinearRegression()
            model_phantom.fit(X, y_phantom)
            next_phantom_users = model_phantom.predict([[len(data)]])[0]

            return next_vandal_users, next_phantom_users

        next_vandal_users, next_phantom_users = predict_next_step(df)
        next_date = df['Date'].max() + pd.Timedelta(days=1)

        # Append the prediction to the dataframe
        next_row = pd.DataFrame({'Date': [next_date], 'Total Vandal Users': [next_vandal_users], 'Total Phantom Users': [next_phantom_users]})
        df = pd.concat([df, next_row], ignore_index=True)

        predicted_value = {
        'Date': next_date.strftime('%Y-%m-%d'),
        'Total Vandal Users': int(next_vandal_users),
        'Total Phantom Users': int(next_phantom_users)
        }


        # Plot the graph
        plt.figure(figsize=(10, 6))
        plt.plot(df['Date'], df['Vandal_Users'], label='Vandal Users')
        plt.plot(df['Date'], df['Phantom_Users'], label='Phantom Users')
        # Highlight the predicted point
        plt.scatter(next_date, next_vandal_users, color='red', label='Predicted Vandal Users')
        plt.scatter(next_date, next_phantom_users, color='orange', label='Predicted Phantom Users')
        plt.xlabel('Date')
        plt.ylabel('Number of Users')
        plt.title('Vandal and Phantom Users Over Time')
        plt.legend()

        # Save the plot as an image
        image_path = 'static/plot.png'
        if not os.path.exists('static'):
            os.makedirs('static')
        plt.savefig(image_path)
        plt.close()
        plot_url = image_path

    return render_template('index.html', plot_url=plot_url)

@app.route('/plot')
def plot():
    return send_file('static/plot.png', mimetype='image/png')

if __name__ == '__main__':
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    app.run(debug=True)
