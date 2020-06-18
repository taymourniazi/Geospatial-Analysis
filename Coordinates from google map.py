# -*- coding: utf-8 -*-
"""
Created on Tue March 29 10:28:23 2020

@author: Taymour Niazi
"""

import requests, json, time
import pandas as pd
pd.set_option("display.precision", 10)
from pandas.io.json import json_normalize

Save_Path = '<File Path>'
File_Name = 'Gas Station V1'


class GooglePlaces(object):
    def __init__(self, apiKey):
        super(GooglePlaces, self).__init__()
        self.apiKey = apiKey

    def search_places_by_coordinate(self, location, radius, types):
        endpoint_url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
        places = []
        params = {
            'location': location,
            'radius': radius,
            'types': types,
            'key': self.apiKey
        }
        res = requests.get(endpoint_url, params = params)
        results =  json.loads(res.content)
        places.extend(results['results'])
        time.sleep(2)
        while "next_page_token" in results:
            params['pagetoken'] = results['next_page_token'],
            res = requests.get(endpoint_url, params = params)
            results = json.loads(res.content)
            places.extend(results['results'])
            time.sleep(2)
        return places

    def get_place_details(self, place_id, fields):
        endpoint_url = "https://maps.googleapis.com/maps/api/place/details/json"
        params = {
            'placeid': place_id,
            'fields': ",".join(fields),
            'key': self.apiKey
        }
        res = requests.get(endpoint_url, params = params)
        place_details =  json.loads(res.content)
        return place_details

api = GooglePlaces("<Your API Key>")

Dammam_places = api.search_places_by_coordinate("26.193785, 50.136511", "50000", "gas_station")
Dammam_places1 = api.search_places_by_coordinate("26.114558, 50.113582", "50000", "gas_station")
Dammam_places2 = api.search_places_by_coordinate("26.215913, 50.043116", "50000", "gas_station")

Petrol_Dammam = pd.DataFrame(Dammam_places)
Petrol_Dammam1 = pd.DataFrame(Dammam_places1)
Petrol_Dammam2 = pd.DataFrame(Dammam_places2)

Data_R = pd.concat([Petrol_Dammam, Petrol_Dammam1, Petrol_Dammam2])

Data_R['Location_City'] = 'Dammam'
drop_Dup = Data_R.drop_duplicates(subset=['place_id'], keep='first')
data_location = json_normalize(drop_Dup['geometry'])
drop_Dup = pd.concat([drop_Dup.reset_index(drop=True),data_location.reset_index(drop=True)], axis=1)
drop_Dup.to_excel(Save_Path+File_Name+'.xlsx')
