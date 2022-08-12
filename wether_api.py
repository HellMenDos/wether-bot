import requests

wether_token = '89e80577932c72c6aa1ba520e19b6f92'

url = lambda lat,lon: f"https://api.openweathermap.org/data/2.5/weather?lat={lat[1]}&lon={lon[1]}&appid={wether_token}&lang=RU"

def get(lat:int, lon:int):
    data = requests.get(url(lat,lon))
    return data.json()

def set_user(user_id: int) -> None:
    data = requests.post("http://62.113.110.28/api/main/wether/",data={"user_id": user_id})
