import requests
import streamlit as st
from streamlit_extras.stylable_container import stylable_container
from weatherdataerror import WeatherDataError
import datetime

# Function to fetch main weather data
def get_weather(city, unit):
    """
    Retrieve weather data for a given city.

    Args:
        city (str): The name of the city to fetch weather data for.
        unit (str): The temperature unit ('Celsius' or 'Fahrenheit').

    Returns:
        tuple: A tuple containing general weather information, temperature, description, weather icon URL, 
        "feels like" temperature, and humidity.
        
    Raises:
        WeatherDataError: If there's an error fetching weather data.
    """
    # Determine the temperature unit for the API request
    if unit == 'Celsius':
        display_unit = 'metric'
    else:
        display_unit = 'imperial'
    api_key = '06a900d695b7ad2724d885503951e322'
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units={display_unit}'

    response = requests.get(url)
    
    # Check the status code to ensure the request was successful (status code 200)
    if response.status_code == 200:
        weather_data = response.json()  # Convert response data into a Python dictionary

        #st.json(weather_data)

        general = weather_data['weather'][0]['main']
        desc = weather_data['weather'][0]['description']
        temperature  = weather_data['main']['temp']
        icon_id = weather_data['weather'][0]['icon']
        icon = f'https://openweathermap.org/img/wn/{icon_id}@2x.png'
        feels_like = weather_data['main']['feels_like']
        wind = weather_data['wind']['speed']
        humidity = weather_data['main']['humidity']

        lon = weather_data["coord"]["lon"]
        lat = weather_data["coord"]["lat"]
    else:
        raise WeatherDataError('Error fetching weather data')

    return general, int(temperature), desc, icon, feels_like, wind, humidity, lon, lat

# Function to fetch temperatures future weather data
def get_predictive_data(unit, lon, lat):
    """
    Retrieve future weather data based on location.

    Args:
        unit (str): The temperature unit ('Celsius' or 'Fahrenheit').
        lon (float): The longitude of the location.
        lat (float): The latitude of the location.

    Returns:
        tuple: A tuple containing temperature, "feels like" temperature, wind speed, and humidity.
    """
    # Determine the temperature unit for the API request
    if unit == 'Celsius':
        display_unit = 'metric'
    else:
        display_unit = 'imperial'
    api_key2 =  "9b833c0ea6426b70902aa7a4b1da285c"
    ex = "current,minutely,daily,alerts"
    url2 = f'https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&exclude={ex}&appid={api_key2}&units={display_unit}'
    
    response2 = requests.get(url2)
    weather_data2 = response2.json()
    #st.json(weather_data2)

    current_time = datetime.datetime.now()
    #current_hour = current_time.hour + 2 #current hour plus two hours incase it is at the end of the hour too
    current_hour = current_time.hour

    temperature_list = [] #This is all the temperatures in the next 6 hours
    for i in range(6):
        temp_hour = current_hour + i
        temp = int(weather_data2["hourly"][temp_hour]['temp'])
        temperature_list.append(temp)

    temperature  = weather_data2["hourly"][current_hour]['temp']
    feels_like = weather_data2["hourly"][current_hour]['feels_like']
    wind = weather_data2["hourly"][current_hour]['wind_speed']
    humidity = weather_data2["hourly"][current_hour]['humidity']

    return temperature, temperature_list, feels_like, wind, humidity

def handle_weather_search(city,unit):
    """
    Handle weather data retrieval and display in a Streamlit app.

    This function retrieves current and predictive weather data for a specified city
    and temperature unit. It then displays the weather information, including
    temperature, feels like, wind, humidity, and deltas, in a Streamlit app.

    Args:
        city (str): The name of the city for which weather data is requested.
        unit (str): The temperature unit, either 'Celsius' or 'Fahrenheit'.

    Returns:
        None
    """
    try:
        # Fetching current and future weather data
        general, temperature, description, icon, feels_like, wind, humidity, lon, lat = get_weather(city, unit)
        temperature2, temperature_list, feels_like2, wind2, humidity2 = get_predictive_data(unit, lon, lat)
    except WeatherDataError as e:
        st.error(f"{e} - City not found")
        st.stop()

    st.write(general)
    st.image(icon)
    st.write(f'Description: {description}')

    delta_temperature = round(temperature - temperature2, 1) #this variable is not used anywhere
    delta_feels_like = round(feels_like - feels_like2, 1)
    delta_wind = round(wind - wind2, 1)
    delta_humidity = round(humidity - humidity2, 1)

    # Display temperatures for the next 6 hours
    try:
        with stylable_container(
            key = "temperatures",
            css_styles = """
                [data-testid="stVerticalBlock"]{
                background: linear-gradient(195deg, #FCB1A6, #FC6376);
                color: #5d2a42;
                text-align: center;
                padding: 20px 0px 20px 0px;
                padding: 5% 5% 5%, 5%;
                border-radius: 30px;
                box-shadow: #FC6376 -15px 10px 30px;
            }
            """
        ):
            columns = st.columns(6)
            for i in range(6):
                if unit == 'Celsius':
                    columns[i].metric("Temperature", f"{temperature_list[i]} °C")
                else:
                    columns[i].metric("Temperature", f"{temperature_list[i]} °F")
    except:
        with st.container():
            columns = st.columns(6)
            for i in range(6):
                if unit == 'Celsius':
                    columns[i].metric("Temperature", f"{temperature_list[i]} °C")
                else:
                    columns[i].metric("Temperature", f"{temperature_list[i]} °F")
        st.markdown(
            """<style>
            [data-testid="stVerticalBlock"] > [style*="flex-direction: column;"] > [data-testid="stVerticalBlock"] {
                background: linear-gradient(195deg, #FCB1A6, #FC6376);
                color: #5d2a42;
                text-align: center;
                padding: 20px 0px 20px 0px;
                padding: 5% 5% 5%, 5%;
                border-radius: 30px;
                box-shadow: #FC6376 -15px 10px 30px;
            }
            </style>""",
            unsafe_allow_html=True,
        )

    # Display "Feels like", humidity, and wind information with deltas
    col11, col22, col33 = st.columns(3)
    if unit == 'Celsius':
        col11.metric("Feels like", f"{feels_like} °C", delta=f"{delta_feels_like} °C")
    else:
        col11.metric("Feels like", f"{feels_like} °F", delta=f"{delta_feels_like} °F")
    col22.metric("Humidity:", f"{humidity} %", delta = f"{delta_humidity} %")
    col33.metric("Wind", f"{wind}mph", delta = delta_wind)

def apply_custom_styles():
    """
    Apply custom CSS styles to a Streamlit app.

    This function adds custom CSS styles to different elements of a Streamlit app
    to control their appearance.

    Args:
        None

    Returns:
        None
    """
    st.markdown(
        """
        <style>
            [data-testid="stAppViewContainer"],
            [data-testid="stHeader"] {
            background: linear-gradient(195deg, #FFDCCC, #FC6376)
            }

            [data-testid="StyledLinkIconContainer"] {
            background-color: #FCB1A6;
            color: #5d2a42;
            text-align: center;
            padding: 20px 90px 20px 20px;
            padding: 5% 5% 5%, 5%;
            border-radius: 30px;
            box-shadow: #FC6376 0px 5px 16px;
            }

            [data-testid="stWidgetLabel"] {
            color: #5d2a42;
            font-size: 20px !important;
            }

            [data-testid="textInputRootElement"] {
            background-color: #FFF9EC;
            color: #5d2a42;
            border: 1px solid #5d2a42;
            box-shadow: #FC6376 0px 3px 10px;
            }

            div[data-baseweb="base-input"] {
            background-color: #FFF9EC;
            }

            .stSelectbox > div[data-baseweb="select"] > div {
            background-color: #FFF9EC;
            color: #5d2a42;
            border: 1px solid #5d2a42;
            box-shadow: #FC6376 0px 3px 10px;
            }

            [data-testid="baseButton-secondary"] {
            background-color: #FFF9EC;
            color: #5d2a42;
            border: 1px solid #5d2a42;
            box-shadow: #FC6376 0px 3px 10px;
            }

            [data-testid="stMarkdownContainer"] {
            color: #5d2a42;
            font-size: 20px !important;
            }

            [data-testid="stMetricValue] {
            color: #5d2a42;
            }

        </style>
        """,
        unsafe_allow_html=True,
    )

# Main function to display weather information
def main():
    """
    Main function to display weather information in a Streamlit app.

    This function sets up a Streamlit app to allow users to find weather information
    for a specified city and temperature unit.

    Args:
        None

    Returns:
        None
    """
    st.set_page_config(page_title="Kyla's Weather App")
    st.header("Find the Weather for today")
    st.markdown("---")
    city = st.text_input("Enter the City").lower()
    unit = st.selectbox("Select Temperature Unit ",["Celsius","Fahrenheit"])

    if st.button("Find"):
        handle_weather_search(city, unit)

    # Call the function to apply the styles
    apply_custom_styles()

if __name__ == "__main__":
    main()