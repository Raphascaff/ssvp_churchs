import re
import requests

def decode_unicode_escapes(text):
    return re.sub(r'\\u[0-9a-fA-F]{4}', lambda match: chr(int(match.group(0)[2:], 16)), text)

def extract_lat_long(text):
    a, b, c = text.find('!3d'), text.find('!4d'), text.find('!16')
    lat = text[a:b].replace('!3d', '')
    lon = text[b:c].replace('!4d', '')
    return [float(lat), float(lon)]

def get_latitude_longitude(address:str, mapbox_key='pk.eyJ1IjoicmFwaGFlbHNjYWZmIiwiYSI6ImNtMjI3YW1leTAzeXAybXBwa3EyNndoZjkifQ.kX4V45OzubMncdDvEnM-3w') -> str:

    if not mapbox_key:
        raise ValueError("Mapbox key must be provided.")
    
    url = f"https://api.mapbox.com/search/geocode/v6/forward?q={address}&access_token={mapbox_key}"
    try:

        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        coordinates = data['features'][0]['geometry']['coordinates']
        latitude, longitude = coordinates[1], coordinates[0]
        return (latitude, longitude)
    
    except (IndexError, KeyError):

        print("Error: Coordinates not found for the given address.")
        return (None, None)
    
    except requests.RequestException as e:

        print(f"Request error: {e}")
        return (None, None)