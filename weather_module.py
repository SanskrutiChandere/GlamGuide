# import requests

# api_key = '92e7e7127e7188d4e0d4256522face23'

# user_input = input("Enter City:")

# weather_data = requests.get(
#     f"http://api.openweathermap.org/data/2.5/weather?q={user_input}&appid={api_key}&units=metric")
# # print(weather_data.json())

# if weather_data.json()['cod']=='404':
#     print("No City Found")
# else:
#     weather = weather_data.json()['weather'][0]['main']
#     temp = round(weather_data.json()['main']['temp'])
    
#     print(f"The weather in {user_input} is: {weather}")
#     print(f"The temperature in {user_input} is: {temp}°C")

import requests

def get_weather(location):
    api_key = '92e7e7127e7188d4e0d4256522face23'
    
    # Make API request to OpenWeatherMap
    weather_data = requests.get(
        f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}&units=metric")
    
    # Check if the city exists
    if weather_data.json()['cod'] == '404':
        return "No City Found", None
    else:
        # Extract weather and temperature information
        weather = weather_data.json()['weather'][0]['main']
        temp = round(weather_data.json()['main']['temp'])
        return weather, temp
