# streamlit_weather_app

This Python code provides a Streamlit web application that allows users to fetch and display weather data for a specified city. The application provides current weather information and information for future hours, including temperature, description, and an icon representing the weather conditions. It also offers a forecast for the next 7 hours, including temperature data, "feels like" temperature, wind speed, and humidity.



## Acknowledgements
This code utilizes the OpenWeatherMap API to fetch weather data. You will need to sign up for an API key on the OpenWeatherMap website (https://openweathermap.org/) and replace the placeholders in the code with your API key.

Please note that the OpenWeatherMap API key placeholders in the code should be replaced with your actual API keys. Additionally, make sure to respect the usage limitations and terms of service of the OpenWeatherMap API.

## Prerequisites
Before running the code, ensure that you have the following requirements installed:

Python (3.7 or higher)
Required Python packages, which you can install using pip:
 - requests
 - streamlit
 - streamlit-extras
 - datetime

## Setup and Execution
1. Clone or download the code to your local machine.
2. Open a terminal or command prompt and navigate to the directory where the code is located.
3. Run the following command to execute the Streamlit application:
```bash
  streamlit run main.py
```
4. The Streamlit application will open in your web browser.
5. Enter the name of the city for which you want to fetch weather data.
6. Select the temperature unit (Celsius or Fahrenheit) from the dropdown.
7. Click the "Find" button to retrieve and display the weather information for the specified city.

## Code Structure
 - get_weather(city, unit): Function to fetch current weather data using the OpenWeatherMap API. It returns information such as general weather conditions, temperature, description, weather icon URL, "feels like" temperature, wind speed, and humidity.
 - get_predictive_data(unit, lon, lat): Function to fetch future weather data for the specified location using the OpenWeatherMap API. It provides temperature data for the next 7 hours, "feels like" temperature, wind speed, and humidity.
 - handle_weather_search(city, unit): Main function for handling the weather data retrieval and display in the Streamlit app. It fetches current and predictive weather data and displays it, along with custom styles.
 - apply_custom_styles(): Function to apply custom CSS styles to the Streamlit app to control its appearance.
 - main(): The main function that sets up the Streamlit app, allowing users to input the city and temperature unit. It also calls the function to apply custom styles.

## Custom Styles
The application uses custom CSS styles to enhance the visual appearance of the Streamlit app. The styles include background colors, font sizes, and box shadows to create an aesthetically pleasing user interface.
