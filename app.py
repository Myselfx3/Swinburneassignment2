import requests
from dotenv import load_dotenv
import os
from dataclasses import dataclass
from chatterbot import ChatBot 
from chatterbot.trainers import ListTrainer
from flask import Flask, render_template, request



load_dotenv()
api_key = os.getenv('API_KEY')

@dataclass
class WeatherData:
    main: str
    description: str
    icon: str
    temperature: str
    humidity: str

location_data = {
    "Lake District National Park": (54.4609, -3.0886),
    "Corfe Castle" : (50.6395, -2.0566),
    "The Cotswolds" : (51.8330, -1.8433),
    "Cambridge" : (52.2053, 0.1218),
    "Bristol" : (51.4545, -2.5879),
    "Oxford" : (51.7520, -1.2577),
    "Norwich" : (52.6309, 1.2974),
    "Stonehenge": (51.1789, -1.8262),
    "Watergate Bay": (50.4429, -5.0553),
    "Birmingham": (52.4862, 1.8904)}

def get_current_weather(lat,lon,API_key):
    resp = requests.get (f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_key}&units=metric').json()
    data = WeatherData (
        main=resp.get('weather') [0].get('main'),
        description=resp.get('weather') [0].get('description'),
        icon=resp.get('weather') [0].get('icon'),
        temperature=resp.get('main').get('temp'),
        humidity=resp.get('main').get('humidity')
        )
    return data   
 

def get_weather_data():
    weather = {}
    for location in location_data.keys():
        lat, lon = location_data[location]
        weather[location] = get_current_weather(lat,lon, api_key)
    return weather

bot = ChatBot(
    'Weatherbot',
    storage_adapter='chatterbot.storage.SQLStorageAdapter',
    logic_adapters=[
        {
            'import_path': 'chatterbot.logic.BestMatch',
        }
    ]
)



for location in location_data.keys():
    conversation = [
        f"What is the weather like in {location}?",
        f"Tell me the weather in {location}.",
        f"Can you provide weather information for {location}?",
        f"Give me the current weather in {location}.",
        f"How's the weather in {location}?",
        f"Describe the weather in {location}.",
        f"Is it raining in {location}?",
        f"What's the temperature in {location}?",
        f"{location} weather",
        f"{location} current conditions",
        f"{location}",
        f"{location} {location}",
        f"{location} {location}{location}",
        f"{location} {location} {location} {location}",
        f"{location} {location} {location} {location} {location}",
        f"{location} {location} {location} {location} {location} {location}",
        f"{location} {location} {location} {location} {location} {location} {location} {location}",
        f"{location} {location} {location} {location} {location} {location} {location} {location} {location}",
        f"{location} and {location} weather",
    ]

trainer = ListTrainer(bot)

trainer.train(conversation)


response = bot.get_response(f'{location}')
print(response)


app = Flask(__name__)
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_response', methods=['POST'])
def get_response():
    user_input = request.form['user_input']
    response = bot.get_response(f'{location}')

    locations = [loc.strip() for loc in response("in")[1:]]
    
    if locations:
        weather_responses = get_weather_data(locations)
        response += '\n' + '\n'.join(weather_responses)

    return response

if __name__ == '__main__':
    app.run(debug=True)
