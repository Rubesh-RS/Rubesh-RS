# Welcome to Vandal/Phantom data graphing and prediction Flask App! 🚀

## Project Overview

This Flask app allows users to:
- Upload their own Excel files or use a sample dataset
- Predict the next step in user data using linear regression
- Generate and display beautiful plots with Matplotlib
- Compare the use of Vandal and Phantom users over the years

## How to Get Started

1. **Clone the repository:**

2. **Install the required packages:**
    Make sure you have Python 3 and `pip` installed. Then, run:
    ```bash
    pip install -r requirements.txt
    ```

3. **Run the Flask application:**
    ```bash
    python app.py
    ```

4. **Open your browser:**
    Navigate to `http://127.0.0.1:5000/` and check out the magic!

## How It Works

### Uploading Data
Users can either upload their own Excel file containing user data or choose to use a sample dataset provided by the application.

### Data Analysis and Prediction
The app reads the data, processes it, and uses linear regression to predict the next step in the user data. This prediction includes:
- **Total Vandal Users:** Predicted number of Vandal users for the next date.
- **Total Phantom Users:** Predicted number of Phantom users for the next date.

### Visualization
The application generates a plot using Matplotlib, which visually compares the usage of Vandal and Phantom users over the years. The plot:
- **Displays historical data:** Shows the trend of Vandal and Phantom users over time.
- **Highlights predictions:** Uses different colors to highlight the predicted data points, making it easy to identify the forecasted values.