import os
import requests
from dotenv import load_dotenv
import datetime
load_dotenv(dotenv_path='.venv/.env')

# Sheety to narzędzie, które zarządza arkuszem google.
# Arkusz google: My Workouts

GENDER = 'male'
WEIGHT_KG = 70
HEIGHT_CM = 179
AGE = 22

datetime_ = datetime.datetime.now()
date = datetime_.strftime("%d/%m/%Y")
time = datetime_.strftime("%H:%M:%S")

APP_ID = os.getenv("API_ID")
APP_KEY = os.getenv("API_KEY")
SHEET_TOKEN = os.getenv("SHEET_TOKEN")

exercise_text = input("Tell me which exercises you did: ")

nutritionix_endpoint = 'https://trackapi.nutritionix.com/v2/natural/exercise'
sheety_endpoint = 'https://api.sheety.co/0b6f646cb7546c186e4309643a92d3ac/workoutTracking/workouts'

exercise_headers = {
    "X-APP-ID": APP_ID,
    "X-APP-KEY": APP_KEY,
}
exercise_parameters = {
    "query": exercise_text,
    "gender": GENDER,
    "weight_kg": WEIGHT_KG,
    "height_cm": HEIGHT_CM,
    "age": AGE
}

exercise_response = requests.post(url=nutritionix_endpoint, headers=exercise_headers, json=exercise_parameters)
exercise_response.raise_for_status()

exercises = exercise_response.json()['exercises']

data = {
    "workout": {
        "date": date,
        "time": time,
        "exercise": False,
        "duration": 0,
        "calories": 0,
    }
}
sheet_headers = {
    "Authorization": f"Bearer {SHEET_TOKEN}"
}

for exercise in exercises:
    data['workout']['exercise'] = exercise['name'].title()
    data['workout']['duration'] = exercise['duration_min']
    data['workout']['calories'] = exercise['nf_calories']
    sheet_response = requests.post(sheety_endpoint, json=data, headers=sheet_headers)
    sheet_response.raise_for_status()
