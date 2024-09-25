# TravelRecommender

# Overview
This is a web scrapping project that gathers the tourist attractions for different cities in India from this [website](https://www.travelogyindia.com/blog/most-visited-tourist-places-in-india/). It also provides the corresponding weather data for the cities and gives a recommendation to go out or not depending on the UV index and the Visibility index of that city. 

# What does it do?

It scrapes the city/place names that are presented in the website. It then fetches the text under the city name that has the list Travel Attractions. Once we have the city names and the travel attractions, an API call using `weatherstack` is made which gives the weather details for that city. Once the weather data is retrieved, a `reccommended` variable is created that says whethe it is recommended to go out to that city given the combination of the UV and the Visibility index at that place. Once the data is retrived, simple data cleaning is done and it is written to a CSV file. 

# How to run?
- Clone this repository and navigate to the directory to run this code. 

- Get an API key for the `weatherstack` API- follow this [link](https://weatherstack.com/). 

- Run this command `pip install -r requirements.txt` on the terminal to install the required packages and finally,

- Execute `main.py` script using `python main.py` in the terminal and give the weather stack API key when prompted for it. 

And wait for the project to create a dataset for you. 

# Limitations

1. The project only scrapes data for cities in India that are covered in the website which has limited number of cities. Hence, the dataset has limited information source resulting a small dataset. 

2. Data retrieving using the API call may be slow because of the rate limits and if too many requests are made in a short time, further requests maybe blocked by the API resulting in incomplete/incorrect data. 