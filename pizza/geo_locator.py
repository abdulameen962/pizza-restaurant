from django.conf import settings
import requests
def automate_locator(ip):
   api_key = settings.GEO_LOCATOR_API_KEY

   api_url = 'https://ipgeolocation.abstractapi.com/v1/?api_key=' + api_key

   response = requests.get(api_url + "&ip_address=" + ip)

   return response.content


def get_location(ip):
    response = requests.get(f'https://ipapi.co/{ip}/json/').json()
    location_data = {
        "ip": ip,
        "city": response.get("city"),
        "region": response.get("region"),
        "country": response.get("country_name")
    }
    return location_data


#get location places to send links of websites
import pandas as pd
import json

links = []

def restaurant_locator(location):
   url = f"https://maps.googleapis.com/maps/api/place/findplacefromtext/json?input=restaurant&inputtype=textquery&locationbias=circle%3A2000%4047.6918452%2C-122.2226413&locationbias=circle%3A1500%4047.6918452%2C-122.2226413&fields=formatted_address%2Cname%2Crating%2Copening_hours%2Cwebsite&key={settings.GOOGLE_API_KEY}"

   payload={}
   headers = {}

   response = requests.request("GET", url, headers=headers, data=payload)

   if len(response.candidates) > 0:
      for web in response.candidates:
           if web.website and len(web.website) > 0:
              links.append(web.website)

   return links