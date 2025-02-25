from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import random
import requests

class ActionMotivationalQuote(Action):
    def name(self):
        return "action_motivational_quote"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: dict):
        quotes = [
            "Believe you can and you're halfway there.",
            "Act as if what you do makes a difference. It does.",
            "Success is not how high you have climbed, but how you make a positive difference to the world.",
        ]
        quote = random.choice(quotes)
        dispatcher.utter_message(text=quote)
        return []

class ActionGetWeather(Action):
    def name(self):
        return "action_get_weather"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: dict):

        location = next(tracker.get_latest_entity_values("location"), None)
        if not location:
            dispatcher.utter_message(text="Sorry, I didn't catch the location. Could you please specify?")
            return []
        
        api_key = "062198cd8bf941c89f5203741252402"
        base_url = "http://api.weatherapi.com/v1"
        complete_url = f"{base_url}/current.json?key={api_key}&q={location}&aqi=no"
        response = requests.get(complete_url)

        if response.status_code == 200:
            data = response.json()
            main = data['main']
            weather_description = data['weather'][0]['description']
            temperature = main['temp']

            weather_report = f"The weather in {location} is currently {weather_description} with a temperature of {temperature}°C."
            dispatcher.utter_message(text=weather_report)
        else:
            dispatcher.utter_message(text="Sorry, I couldn't fetch the weather data. Please try again.")

        return []

    
       