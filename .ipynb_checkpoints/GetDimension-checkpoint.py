import ast
import traceback
from shapely.geometry import Polygon
import pandas as pd
import json
import pdal
from osgeo import gdal,ogr
import geopandas as gpd

class GetDimensionFromBounds:
    """
    This class contains all the functions required
    to read point data and get dimension.
    """
    def __init__(self, bounds:tuple):
        self.bounds=bounds
    def get_polygon(self, bounds:list):
        """
        This function is used to obtain polygon from bounds.
        It is useful for determining if the specified bound
        is in a regions.
        Parameters
        ----------
        bounds:list :The region bounds as a list e.g [-15730544, 10937407, -19027, -15691854, 10976097, 19663]
        Returns
        -------
        polygon of the bounds

        """
        if len(bounds) == 6:
            minx, miny, maxx, maxy = [bounds[0],bounds[1],bounds[3],bounds[4]]
            polygon = Polygon(((minx, miny), (minx, maxy), (maxx, maxy), (maxx, miny), (minx, miny)))
        return polygon

    def validate_bound(self,data:str) -> tuple:
        """
        This function checks if a specified bound is accurate.

        Parameters
        ----------
        data:str :The csv file containing available regions and there bounds.

        Returns
        -------
        tuple : (True, region, url for point cloud data)
        """
        print('Validating bounds:')
        b = self.bounds
        MINX, MINY, MAXX, MAXY = [b[0][0],b[1][0],b[0][1],b[1][1]]
        polygon = Polygon(((MINX, MINY), (MINX, MAXY), (MAXX, MAXY), (MAXX, MINY), (MINX, MINY)))
        db = pd.read_csv(data)
        db['bounds'] = db[['bounds']].applymap(lambda x: ast.literal_eval(x), na_action='ignore')
        db['polygon'] = db[['bounds']].applymap(lambda x: self.get_polygon(x), na_action='ignore')
        try:
            for i,r,u,p in db[['region','url','polygon']].itertuples():
                if p.contains(polygon):
                    self.run,self.region,self.url = (True,r,u) 
                    return(True,r,u,b) 
            return(False,'bound specified not in any known region')
        except Exception:
            print("Error Occured for")
            traceback.print_exc()
            
    def create_pipeline(self, pipelinejson:str = 'read_file.json') -> dict:
        """
        This function is used to generate the pipeline for specified bounds
        Parameters
        ----------
        pipelinejson:str :
             (Default value = 'read_file.json')

        Returns
        -------
        pipeline as a dictionary

        """
        print('Creating Pipeline:')
        if self.run == True:
            try:
                pipeline_json = json.load(open(pipelinejson))
                pipeline_json['pipeline'][0]['bounds'] = str(self.bounds)
                pipeline_json['pipeline'][0]['filename'] = self.url
                pipeline_json['pipeline'][5]['filename'] = f'{self.region}.laz'
                pipeline_json['pipeline'][6]['filename'] = f'{self.region}.tif'
                self.pipeline_json = pipeline_json
                return(pipeline_json)
            except Exception:
                print("Error Occured")
                traceback.print_exc()
        else:
            print('Create Pipeline failed. Invalid bound')
        
    def execute_pipeline(self) -> str:
        """ 
        Executes pipeline
        """
        print('Executing pipeline:')
        try:
            print('Feeding pipeline to pdal...')
            pipeline = pdal.Pipeline(json.dumps(self.pipeline_json))
            print('Executing pipeline...')
            pipeline.execute()
            return(f'Execution Successful,\npoint cloud data saved as:/n{self.region}.laz /n{self.region}.tif')
        except Exception:
            print("Error Occured")
            traceback.print_exc()
            
    def create_shp(self) -> str:
        """ 
        Creates shp file from tiff file
        """
        print('Creating Shape file:')
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
        print("Reading tif file...")
        
        try:
            ds = gdal.Open(f'{self.region}.tif')
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
        dst_ds = drv.CreateDataSource(f'{self.region}.shp')
        dst_layer = dst_ds.CreateLayer(dst_layername, srs = None )
        raster_field = ogr.FieldDefn('elevation', type_mapping[srcband.DataType])
        dst_layer.CreateField(raster_field)
        gdal.Polygonize( srcband, None, dst_layer, 0, [], callback=None)
        print(f'Shapefile Created..\nfile saved here {self.region}.shp')
        
    
    def get_dimensions(self) -> gpd.GeoDataFrame:  
        """ 
        This function returns the dimension from the shapefile.
        """
        print('Reading shape file...')
        geo_df = gpd.read_file(f'{self.region}.shp')
#         change geometry from polygon to point
        geo_df['geometry'] = geo_df.geometry.centroid
        return geo_df  
    

