import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd
from scipy.interpolate import griddata
import numpy as np
def heatmap(shpfile:str, nodata_value:int = -9999)-> None:
    """
    creates a heatmap of the region and its elevation
    Parameters
    ----------
    shpfile : str :path to shapefile
        
    nodata_value:int :
         (Default value = -9999)
    
    """
#     read shape file 
    geo_df = gpd.read_file(shpfile)
    
#     remove no data values from data
    df = geo_df[geo_df['elevation_'] > nodata_value]
    
    plt.rcParams["figure.figsize"] = (20,10)
    fig, ax = plt.subplots(1, 1)
    df.plot(column='elevation_', cmap='OrRd', ax=ax, legend=True, legend_kwds={'label': "Elevation by point"})
    ax.legend(fontsize=15)
    
def map3d(shpfile:str, nodata_value:int = -9999)-> None:
    """
    creates a 3d map of the region latitude, longitude and elevation

    Parameters
    ----------
    shpfile : str :path to shapefile
        
    nodata_value:int :
         (Default value = -9999)

    """
    #     read shape file 
    geo_df = gpd.read_file(shpfile)
    
#     remove no data values from data
    geo_df = geo_df[geo_df['elevation_'] > nodata_value]
    geo_df['geometry'] = geo_df.geometry.centroid
    
    xyz = zip(geo_df.geometry.x,geo_df.geometry.y,geo_df['elevation_'])
    data = pd.DataFrame(xyz)
    x = data[0].values
    y = data[1].values
    z = data[2].values
    xi = np.linspace(x.min(),x.max(),100)
    yi = np.linspace(y.min(),y.max(),100)
    zi = griddata((x, y), z, (xi[None,:], yi[:,None]), method='nearest')
    xig, yig = np.meshgrid(xi, yi)
    
    plt.rcParams["figure.figsize"] = (20,10)
    fig = plt.figure()
    ax = fig.add_subplot(1,2,1, projection='3d')
    my_plot = ax.plot_surface(xig, yig, zi,rstride=1, cstride=1, cmap='OrRd', linewidth=0, antialiased=True)
    ax.set_xlabel("Longitude")
    ax.set_ylabel("Latitude")
    ax.set_zlabel("Elevation")
    ax.set_title('Surface Elevation Plot')
    plt.show()
