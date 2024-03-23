import requests
from flask import Flask, request, jsonify, render_template
from pprint import pprint

app = Flask(__name__)

# OpenWeatherMap API key
key = "f0eb22dfee8c13e389e81a552c707e76"

# Predefined disaster conditions
disaster_conditions = ["Tropical Depression", "Extreme temperature", "Extremely heavy rain", "Cold wave", "Storm", "Low temperature", "Convective storm", "Strong wind", "Continuous rain", "Gust wind", "Tropical storm", "Rain damage", "Typhoon", "Heavy rain", "Drought", "Hail Rain damage"]

@app.route('/')
def index():
    return '''
<style>
body {
    font-family: Arial, sans-serif;
    margin: 0; /* Remove default margin */
    padding: 0; /* Remove default padding */  
}

.main-container {
    background-image: url('https://t4.ftcdn.net/jpg/02/66/38/15/360_F_266381525_alVrbw15u5EjhIpoqqa1eI5ghSf7hpz7.jpg');
    width: 100%;
    min-height: 100vh;
    background-size: cover;
    opacity: 0.8; /* Set opacity to 0.8 to reduce the background image's intensity */
    display: flex;
    flex-direction: column;
    justify-content: center; /* Vertically center the content within the container */
    align-items: center;
}

h1 {
    text-align: center;
    color: white;
}
  
.form-container {
    display: flex;
    flex-direction: column;
    margin: 20px auto;
    width: 300px;
    align-items: center;
}
  
.form-container label {
    margin-bottom: 5px;
    display: block;
    font-weight: 800;
    font-size: 25px;
    color: white;
}
  
.weather option {
    background: transparent;
}
  
.select, input[type="text"] {
    width: 100%;
    padding: 10px;
    border: 1px solid #ccc;
    border-radius: 4px;
    margin-bottom: 15px;
}
  
.button {
    background-color: #329436; 
    border: none;
    color: white;
    padding: 10px 20px;
    text-align: center;
    text-decoration: none;
    display: inline-block;
    font-size: 16px;
    margin-top: 10px;
    cursor: pointer;
    border-radius: 50px;
    margin-left: 70px;
}
.button:hover {
    background: transparent;
    border: solid;
    border-color: white;
}
</style>

<div class='main-container'>
    <h1>Crop Insurance Claim Filing</h1>
    
    <form action="/get_weather" method="get">
        <div class="form-container">
            <label for="weather">Weather Condition:</label>
            <select class= "select" name="weather" id="weather">
                <option value="">Select Weather</option>
                <option value="Tropical Depression">Tropical Depression</option>
                <option value="Extreme temperature">Extreme temperature</option>
                <option value="Extremely heavy rain">Extremely heavy rain</option>
                <option value="Cold wave">Cold wave</option>
                <option value="Storm">Storm</option>
                <option value="Low temperature">Low temperature</option>
                <option value="Convective storm">Convective storm</option>
                <option value="Strong wind">Strong wind</option>
                <option value="Moderate rain">Moderate rain</option>
                <option value="Gust wind">Gust wind</option>
                <option value="Tropical storm">Tropical storm</option>
                <option value="Rain damage">Rain damage</option>
                <option value="Typhoon">Typhoon</option>
                <option value="Heavy rain">Heavy rain</option>
                <option value="Drought">Drought</option>
                <option value="Hail Rain damage">Hail Rain damage</option>
            </select>

            <label for="city">Location:</label>
            <input type="text" id="city" name="city" placeholder="Enter your farm location"/>
        </div>
        <button class="button" type="submit">Submit Claim</button>
    </form>
</div>


    '''

@app.route('/get_weather', methods=['GET'])
def get_weather():
   
    city = request.args.get('city')
    weather_condition = request.args.get('weather')

    # Construct the API endpoint for finding the city coordinates
    geo_link = f"https://api.openweathermap.org/geo/1.0/direct?q={city}&limit=5&appid={key}"

    #request to the Geo API endpoint
    geo_response = requests.get(url=geo_link)
    geo_data = geo_response.json()

    token = "c3ed76b2371288"
    link = f"https://ipinfo.io?token={token}"


    response = requests.get(url=link)
    data = response.json()

    # city information
    user_city = data.get('city')

    if user_city and user_city.lower() == city.lower(): 
        if geo_data:
           
            lat = geo_data[0]['lat']
            lon = geo_data[0]['lon']

         
            weather_link = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={key}"

           
            weather_response = requests.get(url=weather_link)
            weather_data = weather_response.json()

            if 'weather' in weather_data:
                
                description = weather_data['weather'][0]['description']
                # Check if the weather condition matches any predefined disaster conditions
                insurance_granted = weather_condition.lower() == description.lower()

                return jsonify({'Weather': description, 'Insurance Granted': insurance_granted, 'User registering from': user_city})
            else:
                return jsonify({'error': 'Weather data not found'})
        else:
            return jsonify({'error': 'City not found'})
    else:
        return jsonify({'error': 'Insurance not granted as user is fabricating location'})

'''
        if 'weather' in weather_data:
            # Extract description from weather data
            description = weather_data['weather'][0]['description']

            # Check if the weather condition matches any predefined disaster conditions
            if weather_condition.lower() in map(str.lower, disaster_conditions):
                insurance_granted = True
            else:
                insurance_granted = False

            return jsonify({'Weather': description, 'Insurance Granted': insurance_granted})
        else:
            return jsonify({'error': 'Weather data not found'})
    else:
        return jsonify({'error': 'City not found'})
'''     

if __name__ == '__main__':
    app.run(debug=True)
