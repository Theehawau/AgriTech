# AgriTech
Obtain Land Elevation Data Using USGS LIDAR

AgriTech is a python module that domain experts and data scientists can use to fetch, visualise, and transform publicly available satellite and LIDAR data. 
It uses PDAL, GDAL, OGR

### Runtime 
Python 3
### Installation
```cli
git clone https://github.com/Theehawau/AgriTech
cd AgriTech
pip -r requirements.txt
```
### Features
* [Get Bounds]()
> This script contains a class that can obtain the bounds to a region, link to the region point cloud data from a file of region names.
* [Read]()
> This script contains a class with attributes to check given region validity, generate pipeline from give data, run pipeline to obtain tiff file,shape file and geojson file
* [Visualize]()
> This script contains functions for visualizing the data

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
Other Usage samples can be found in this [notebook]()
#### Read
```python
import read
##Initialize module with bounds, region
rpd = Read_Point_Data('[-15730544, 10937407, -19027, -15691854, 10976097, 19663]','AK_Coastal_2009')

```
Other Usage samples can be found in this [notebook]()
#### Visualize
```python
## Import all functions in module
from visualize import *
##Plot heatmap from shape file with elevation as legend
heatmap('shp/iowa.shp')
```
Other Usage samples can be found in this [notebook]()


