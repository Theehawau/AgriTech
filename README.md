# AgriTech

[![Issues][issues-shield]][issues-url]

![workflow](https://github.com/Theehawau/AgriTech/actions/workflows/cml.yml/badge.svg)

<p>Obtain Land Elevation data using USGS LIDAR.
AgriTech is a python module that domain experts and data scientists can use to fetch, visualise, and transform publicly available satellite and LIDAR data.</p>
  
###  Built With

Resoures that used in this project are :
* PDAL
* GDAL
* OGR
* Shapely
... amongst others

### Installation
```cli
git clone https://github.com/Theehawau/AgriTech
cd AgriTech
pip -r requirements.txt
```
### Features
* [filename.txt](../main/filename.txt) : list of regions available in amazon bucket
* [data.csv](../main/data.csv) : table of region name, url to data on amazon bucket, region bounds, region polygon.
* [metadata.csv](../main/metadata.csv) : table  of region name, url to data on amazon bucket, bounds.
* [read_file.json](../main/read_file.json) :pipeline skeleton json file
* [GetBounds](../main/GetBounds.py)
  <p> This script contains a class that can obtain the bounds to a region, link to the region point cloud data from a file of region names.</p>

* [ReadData](ReadData.py)
  <p>This script contains functions to  generate pipeline from give data, run pipeline to obtain tiff file,generate shape file and  generate dimensions geopandas     dataframe </p>
  
* [UpdateMetaData](ReadData.py)
  <p> This script contains functions to  generate pipeline from give data, run pipeline to obtain tiff file,generate shape file and  generate dimensions geopandas     dataframe </p>
  
* [GetDimensions](../blob/main/GetDimension.py)
  <p> This script contains a class with attributes to validate bounds, create and run pipeline, generate shape file and dimension geopandas. </p>
  <p> The attributes need to be followed step wise. <a href="https://github.com/Theehawau/AgriTech/blob/main/notebooks/GetDimension.ipynb">See example.</a></p>
  
* [Visualize](https://github.com/Theehawau/AgriTech/blob/main/Visualize.py)
  <p> This script contains functions for visualizing the data </p>

### Usage
#### Get Bounds
```python
##Import module
import GetBounds
##Initialize module with file containing regions name
getbounds = GetBounds.get_bounds_region('filename.txt')
##To get link to point cloud data for regions in filename.txt
getbounds.get_region_to_location()
##To get valid bounds to regions in filename.txt from link
getbounds.get_region_bounds()
##To save list of dictionary with region, bound, location in metadata.csv
getbounds.save_data('metadata.csv')
```
#### Visualize
```python
## Import all functions in module
from visualize import *
##Plot heatmap from shape file with elevation as legend
heatmap('shp/iowa.shp')
```
Other Usage samples and examples can be found in [notebooks](../main/notebooks)



[issues-shield]: https://img.shields.io/github/issues/Theehawau/AgriTech.svg?style=for-the-badge
[issues-url]: https://github.com/Theehawau/AgriTech/issues
