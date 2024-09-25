import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import csv

def get_weather_UV_data(API_key, city):
    url = f"https://api.weatherstack.com/current?access_key={API_key}"
    querystring = {"query":city}
    response = requests.get(url, params=querystring)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed with {response.status_code} ")
        return []


def get_places(web_url):
    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36'
    }
    response = requests.get(web_url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        city_tags = soup.find_all('h2') # get all the info under the h2 attribute

        city_and_attractions = []
        for city in city_tags:
            city_name = city.get_text() # get the city names
            city_text = city.find_next('p') 
            
            # the tourist attractions are in second 'p' tag. so,
            tourist_places = city_text.find_next('p').get_text() #if city_text.find_next('p') else 'No attractions listed'
    
            city_and_attractions.append({'City': city_name, 'Attractions': tourist_places})
        return city_and_attractions
    else:
        print(f"Data Load Fail with {response.status_code}")    
        return None    

def writing_to_CSV(data, filename):
    
    # CSV headers
    headers = ['City/Place', 'Attractions', 'Temperature', 'UV Index', 'Recommended to go out?']
    
    with open(filename, mode='w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        
        writer.writerow(headers)
        for row in data:
            writer.writerow(row) 
    print("Done writing to the CSV.")


def main(API_key, web_url):
    city_and_attractions = get_places(web_url)

    data_for_CSV = []

    for city_info in city_and_attractions:
        city = city_info['City']
        attractions = city_info['Attractions']

        if ':' not in attractions:
            continue  # Skip the iteration if there are no recommendation for that place

        weather_data_for_city = get_weather_UV_data(API_key, city)

        if weather_data_for_city:
            temperature = weather_data_for_city['current']['temperature'] #get the temperature fo that place
            uv_index = weather_data_for_city['current']['uv_index'] #get the uv index for that place
            visibility = weather_data_for_city['current']['visibility'] 
            if uv_index > 5 and visibility < 2: # uv index is greater than 5 and visibility is less than 2, recommend not to go out
                recommended = 'No'
            else:
                recommended = 'Yes'
        else:
            temperature = 'NA'
            uv_index = 'NA'
            recommended = 'NA'
        
        data_for_CSV.append([city, attractions, temperature, uv_index, recommended])
        time.sleep(1)
    
    # cleaning
    for row in data_for_CSV:
        row[0] = row[0].lstrip('0123456789. ').strip() # removing the trailing number/./whitespace

        row[1] = row[1].split(':', 1)[-1].strip()  # Split at the first colon and take the part after it
        attractions_list = row[1].split(',')
        row[1] = '\n'.join([attraction.strip() for attraction in attractions_list])
    
    writing_to_CSV(data_for_CSV, 'Travel_recommendations.csv')

web_url = 'https://www.travelogyindia.com/blog/most-visited-tourist-places-in-india/'
API_key = input("Enter the API key: ")
main(API_key, web_url)
