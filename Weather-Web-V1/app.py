import requests
from flask import Flask, render_template, request

app = Flask(__name__)

# Enter your OpenWeatherMap API key here
api_key = "8c0d46fb7fe7e71d5d0b2d3179f3f992"

# Dictionary mapping city names to symbols
city_symbols = {
    "Paris": "🗼",
    "New York": "🗽",
    "London": "🏰",
    "San Francisco": "🌉",
    "Washington": "🏛️",
    "Miami Beach": "🏖️",
    "Tokyo": "🏙️",
}

# Define a function to retrieve the weather data and recommendations
def get_weather(city):
    # API endpoint URL for current weather data
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"

    # Send a GET request to the API endpoint and get the response
    response = requests.get(url)

    # Get the JSON data from the response
    data = response.json()

    # Get the current temperature, wind speed, and weather description from the data
    temp = data["main"]["temp"]
    wind_speed = data["wind"]["speed"]
    weather_description = data["weather"][0]["description"].title()

    # Check if the temperature is comfortable for going outside
    if temp >= 30:
        recommendation = "It's hot outside. Wear light clothing and stay hydrated."
    elif temp >= 20:
        recommendation = "It's a nice day, you can go outside!"
    else:
        recommendation = "It's cold outside. Wear warm clothing and stay indoors if possible."

    # Check if it's windy outside
    if wind_speed >= 10:
        warning = "It's windy outside. Be careful when walking or cycling."
    else:
        warning = "The wind speed is moderate, it should not affect your outdoor activities."

    # Get the symbol for the city, defaulting to a globe symbol if the city is not in the dictionary
    symbol = city_symbols.get(city, "🌍")

    # Return a dictionary containing the weather data and recommendations
    return {"temp": temp, "wind_speed": wind_speed, "weather_description": weather_description, "recommendation": recommendation, "warning": warning, "symbol": symbol}

# Define a route for the homepage
@app.route("/")
def index():
    return render_template("index.html")

# Define a route for the weather report page
@app.route("/weather", methods=["POST"])
def weather():
    # Get the city name entered by the user
    city = request.form["city"]

    # Get the weather data and recommendations for the city
    weather_data = get_weather(city)

    # Render the weather report page with the weather data and recommendations
    return render_template("weather.html", city=city, temp=weather_data["temp"], wind_speed=weather_data["wind_speed"], weather_description=weather_data["weather_description"], recommendation=weather_data["recommendation"], warning=weather_data["warning"], symbol=weather_data["symbol"])

if __name__ == "__main__":
    app.run(debug=True)