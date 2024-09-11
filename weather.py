
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import requests
import time

app = Flask(__name__)
CORS(app)

@app.route('/')
@app.route('/home')
def home():
    return render_template('index.html')

@app.route('/getWeather', methods=['POST'])
def getWeather():
    data = request.get_json()
    city = data['city']
    api = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid=4542341c0498bbc020c321bdc6b07acb"
    json_data = requests.get(api).json()
    
    if json_data.get('cod') != 200:
        return jsonify({"error": "City not found"})
    
    condition = json_data['weather'][0]['main']
    temp = int(json_data['main']['temp'] - 273.15)
    min_temp = int(json_data['main']['temp_min'] - 273.15)
    max_temp = int(json_data['main']['temp_max'] - 273.15)
    pressure = json_data['main']['pressure']
    humidity = json_data['main']['humidity']
    wind = json_data['wind']['speed']
    sunrise = time.strftime("%H:%M:%S", time.gmtime(json_data['sys']['sunrise'] + 7200))
    sunset = time.strftime("%H:%M:%S", time.gmtime(json_data['sys']['sunset'] + 7200))

    weather_info = {
        "condition": condition,
        "temp": temp,
        "min_temp": min_temp,
        "max_temp": max_temp,
        "pressure": pressure,
        "humidity": humidity,
        "wind": wind,
        "sunrise": sunrise,
        "sunset": sunset
    }

    return jsonify(weather_info)

if __name__ == '__main__':
    app.run(debug=True)