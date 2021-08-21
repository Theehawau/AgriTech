import pandas as pd
import json
import requests
import sys
import csv

class get_bounds_region:
    """ """
    def __init__(self,filepath:str):
        self.regions_path = filepath
        self.data = []
    def get_region_to_location(self) -> None:
        """ 
        This functions creates a list of dict in the format:
        [{'region':'','location':''},...]
        """
        print('Getting location to region names...')
        with open (self.regions_path, encoding="utf-8") as f:
            f.readline()
            for line in f:
                filename = line.replace('\n','')
                location = f'https://s3-us-west-2.amazonaws.com/usgs-lidar-public/{filename}ept.json'
                dic = {'region':filename,'location':location}
                self.data.append(dic)
        print('Successful')
            
    def get_region_bounds(self) -> None:
        """ 
        This functions updates the list of dict to:
        [{'region':'','location':'','bounds':''},...]
        """
        print('Getting bounds to region names')
        for dic in self.data:
            try:
                json_file = requests.get(dic['location']).json()
                bound = json_file['bounds']
                dic['bounds'] = bound
            except Exception:
                print(f"Error occured couldn't find bounds for {dic['region']}")
                continue
        print('Successful')
        
    def save_data(self, filename:str = 'metadata.csv') -> None:
        """
        This function saves the dict as a csv file
        Parameters
        ----------
        filename:str :
             (Default value = 'metadata.csv')
             
        Returns
        -------
        None
        """
        print('Saving file to metadata.csv ...')
        with open(filename, 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=['region','location','bounds'])
            writer.writeheader()
            writer.writerows(self.data)
        print('File saved successfully')    

        
if __init__ == '__main__':
    get = get_bounds_region('filename.txt')
    get.get_region_to_location()
    get.get_region_bounds()
    get.save_data()
    
