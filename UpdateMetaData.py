import ast
from shapely.geometry import Polygon
import pandas as pd
# Run this file to get clean meta data as data.csv
db = pd.read_csv('metadata.csv')

def get_polygon(bounds:list):
    if len(bounds) == 6:
        MINX, MINY, MAXX, MAXY = [bounds[0],bounds[1],bounds[3],bounds[4]]
    polygon = Polygon(((MINX, MINY), (MINX, MAXY), (MAXX, MAXY), (MAXX, MINY), (MINX, MINY)))
    return polygon
# Uses ast to get change the list from string datatype
db['bounds'] = db[['bounds']].applymap(lambda x: ast.literal_eval(x), na_action='ignore')

db['polygon'] = db[['bounds']].applymap(lambda x: get_polygon(x), na_action='ignore')

db['region'] = db[['region']].applymap(lambda x: x.replace('/',''), na_action='ignore' )

db.rename(columns={'location':'url'}, inplace=True)

#save data to data.csv
db.to_csv('data.csv',index=False)
