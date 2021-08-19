import pandas as pd
import json
import requests
import sys

class get_bounds_region:
    def __init__(self,filepath:str):
        self.regions_path = filepath
        self.region_to_location={}
        self.region_to_bounds={}
    
    def get_region_to_location(self):
        region_to_location = {}
        print('Getting location to region names...')
        with open (self.regions_path, encoding="utf-8") as f:
            f.readline()
            for line in f:
                filename = line.replace('\n','')
                location = f'https://s3-us-west-2.amazonaws.com/usgs-lidar-public/{filename}ept.json'
                region_to_location[filename] = location
            self.region_to_location = region_to_location
        print('Successful')
            
    def get_region_bounds(self):
        file_to_bounds = {}
        print('Getting bounds to region names')
        for file,location in self.region_to_location.items():
            try:
                json_file = requests.get(location).json()
                file_to_bounds[file] = json_file['bounds']
            except Exception:
                print(f"Error occured couldn't find bounds for {file}")
                continue
        self.region_to_bounds = file_to_bounds
        print('Successful')
    
    def get_dataframe(self):
        print('get data for dataframe...')
        for region,bounds in self.region_to_bounds.items():
            regions = []
            bounds = []
            locations=[]
            regions.append(region)
            bounds.append(bounds)
            locations.append(self.region_to_location[file])
        self.data = pd.DataFrame({'region':regions,'bounds':bounds,'location':locations})
        print('Successful')
    def save_data(self):
        self.data.to_csv('metadata.csv')
        print('File saved successfully')