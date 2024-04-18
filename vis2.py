from seatable_api import Base, context
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error
import matplotlib.pyplot as plt

def fetch_temperature_data():
    """
    Fetches temperature data from the Seatable database.

    Returns:
        list: List of temperature data.
    """
    try:
        server_url = context.server_url or 'https://cloud.seatable.io'
        api_token = context.api_token or '082f58664512a2bb8b9b5bf2e8b5b5e878751bd2'

        base = Base(api_token, server_url)
        base.auth()

        rows = base.list_rows("Data")

        temp = []

        # Fetch temperature data from rows
        for row in rows:
            temp_value = row.get('Temperature')
            if temp_value:
                temp.append(float(temp_value.replace('b','').replace("'","")))

        # Convert temperature data to float
        temp = [float(t) for t in temp]

        return temp

    except Exception as e:
        print("An error occurred while fetching temperature data:", e)
        return None

def analyze_temperature_data(temp):
    """
    Analyzes the temperature data.

    Args:
        temp (list): List of temperature data.
    """
    try:
        if temp:
            X = np.arange(len(temp)).reshape(-1, 1)
            y = np.array(temp)
            reg = LinearRegression().fit(X, y)

            # Predict temperatures using linear regression
            y_pred = reg.predict(X)

            # Plot temperature data
            plt.figure(figsize=(10, 6))
            plt.plot(X, temp, marker='o', linestyle='-', label='Temperature Data')

            # Plot linear regression line
            plt.plot(X, y_pred, color='red', linestyle='--', label='Linear Regression')

            # Calculate statistics
            mean_temp = np.mean(temp)
            median_temp = np.median(temp)
            std_dev_temp = np.std(temp)

            print("Mean Temperature:", mean_temp)
            print("Median Temperature:", median_temp)
            print("Standard Deviation of Temperature:", std_dev_temp)

            # Model evaluation metrics
            r_squared = r2_score(y, y_pred)
            mae = mean_absolute_error(y, y_pred)
            mse = mean_squared_error(y, y_pred)
            rmse = np.sqrt(mse)

            print("R-squared:", r_squared)
            print("Mean Absolute Error (MAE):", mae)
            print("Mean Squared Error (MSE):", mse)
            print("Root Mean Squared Error (RMSE):", rmse)

            # Predict temperatures for future samples
            future_samples = 10
            future_X = np.arange(len(temp), len(temp) + future_samples).reshape(-1, 1)
            future_y_pred = reg.predict(future_X)

            print("\nPredicted temperatures for future samples:")
            for i, temp_pred in enumerate(future_y_pred):
                print(f"Sample {len(temp) + i + 1}: {temp_pred:.2f} °C")

            # Plot predicted temperatures for future samples
            plt.plot(future_X, future_y_pred, color='blue', marker='o', linestyle='--', label='Predicted Temperatures')

            plt.title('Temperature Data and Linear Regression')
            plt.xlabel('Sample')
            plt.ylabel('Temperature (°C)')
            plt.grid(True)
            plt.legend()
            plt.show()

        else:
            print("No temperature data available.")

    except Exception as e:
        print("An error occurred during temperature data analysis:", e)

def main():
    # Fetch temperature data
    temp = fetch_temperature_data()

    # Analyze temperature data
    analyze_temperature_data(temp)

if __name__ == "__main__":
    main()
