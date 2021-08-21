import json
import pdal
import traceback
import geopandas as gpd
from osgeo import gdal,ogr
import sys 
import os

def create_pipeline(pipeline_path:str ,bounds:str,location:str) -> dict:
    """

    Parameters
    ----------
    pipeline_path:str :path to pipeline json file
        
    bounds:str :bounds to region
        
    location:str : url to download point cloud data
        

    Returns
    -------
    pipeline as a dict
    """
        try:
            pipeline_json = json.load(open(pipeline_path))
            pipeline_json['pipeline'][0]['bounds'] = bounds
            pipeline_json['pipeline'][0]['filename'] = location
            return pipeline_json
        except Exception:
            print("Error Occured")
            traceback.print_exc()
            
def read_data(pipeline) -> None:
    """
    This function executes the pipeline
    Parameters
    ----------
    pipeline : pipeline json data as a dict

    """
        try:
            print('feeding pipeline to pdal...')
            pipeline = pdal.Pipeline(json.dumps(pipeline))
            print('Executing pipeline...')
            pipeline.execute()
            print('Execution Complete!')
        except Exception:
            print("Error Occured")
            traceback.print_exc()
            
def convert_tif_to_shp(src_tif:str , output:str):
    """
    This function can create a shape file from a tif file

    Parameters
    ----------
    src_tif:str :tif file path
        
    output:str :shp file path

    """
        # mapping between gdal type and ogr field type
        type_mapping = { gdal.GDT_Byte: ogr.OFTInteger,
                        gdal.GDT_UInt16: ogr.OFTInteger,   
                        gdal.GDT_Int16: ogr.OFTInteger,    
                        gdal.GDT_UInt32: ogr.OFTInteger,
                        gdal.GDT_Int32: ogr.OFTInteger,
                        gdal.GDT_Float32: ogr.OFTReal,
                        gdal.GDT_Float64: ogr.OFTReal,
                        gdal.GDT_CInt16: ogr.OFTInteger,
                        gdal.GDT_CInt32: ogr.OFTInteger,
                        gdal.GDT_CFloat32: ogr.OFTReal,
                        gdal.GDT_CFloat64: ogr.OFTReal}

        # this allows GDAL to throw Python Exceptions
        gdal.UseExceptions()
        print("reading tif file...")
        
        try:
            ds = gdal.Open(src_tif)
        except RuntimeError as e:
            print('Unable to open file')
            print(e)
            sys.exit(1)

        try:
            srcband = ds.GetRasterBand(1)
        except RuntimeError as e:
            # for example, try GetRasterBand(10)
            print('Band ( %i ) not found' % 1)
            print(e)
            sys.exit(1)

        # create shapefile datasource from geotiff file
        print("creating shapefile...")
        dst_layername = "Shape"
        drv = ogr.GetDriverByName("ESRI Shapefile")
        dst_ds = drv.CreateDataSource(output)
        dst_layer = dst_ds.CreateLayer(dst_layername, srs = None )
        raster_field = ogr.FieldDefn('elevation', type_mapping[srcband.DataType])
        dst_layer.CreateField(raster_field)
        gdal.Polygonize( srcband, None, dst_layer, 0, [], callback=None)
        print(f'Transformation Completed..\nfile saved here {output}')
        
def get_dimensions(shp_file:str) -> gpd.GeoDataFrame:  
    """
    gets dimensions from a shape file
    Parameters
    ----------
    shp_file:str :shp file path
        

    Returns
    -------
    data as geopandas data frame
    """
        geo_df = gpd.read_file(shp_file)
#         change geometry to point
        geo_df['geometry'] = geo_df.geometry.centroid
        return geo_df
    
