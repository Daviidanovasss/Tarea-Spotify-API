from dotenv import load_dotenv
load_dotenv()
import os
import requests


def get_user_data(user_id: str):
    API_KEY_Public = os.getenv("client_Public_Key")
    API_KEY_Secret = os.getenv("client_Secret_Key")

    
    url_API_Spotify = 'https://accounts.spotify.com/api/token'
    header_Spotify = {"Content-Type": "application/x-www-form-urlencoded"}
    data_Spotify = {
                "grant_type": "client_credentials",
                "client_id": API_KEY_Public,
                "client_secret": API_KEY_Secret
                }
    auth_response = requests.post(url_API_Spotify, headers = header_Spotify, data = data_Spotify)
    access_token = auth_response.json()['access_token']
    print(access_token)
    headers = {"Authorization": f"Bearer {access_token}"}
    url = f"https://api.spotify.com/v1/users/{user_id}"
    response = requests.get(url, headers=headers)
    user_data = response.json()
    if response.status_code != 200:
        return{"error": "User not found"}
    return user_data