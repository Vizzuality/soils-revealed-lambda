import numpy as np
import pandas as pd
import xarray as xr
import dask.array as da
from dask.diagnostics import ProgressBar
import zarr
import s3fs
from affine import Affine
from rasterio import features
from shapely.geometry import Polygon
import os
from dotenv import load_dotenv
from pathlib import Path
import json

load_dotenv()
env_path = Path('.') / '.env'

class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        else:
            return super(NpEncoder, self).default(obj)
        
def transform_from_latlon(lat, lon):
    lat = np.asarray(lat)
    lon = np.asarray(lon)
    trans = Affine.translation(lon[0], lat[0])
    scale = Affine.scale(lon[1] - lon[0], lat[1] - lat[0])
    return trans * scale

def rasterize(shapes, coords, latitude='latitude', longitude='longitude',
              fill=np.nan, **kwargs):
    """Rasterize a list of (geometry, fill_value) tuples onto the given
    xray coordinates. This only works for 1d latitude and longitude
    arrays.
    """
    transform = transform_from_latlon(coords[latitude], coords[longitude])
    out_shape = (len(coords[latitude]), len(coords[longitude]))
    raster = features.rasterize(shapes, out_shape=out_shape,
                                fill=fill, transform=transform,
                                dtype=float, **kwargs)
    spatial_coords = {latitude: coords[latitude], longitude: coords[longitude]}
    return xr.DataArray(raster, coords=spatial_coords, dims=(latitude, longitude))

def read_dataset(dataset_type, group, access_key_id, secret_accsess_key):
    # AWS S3 path
    s3_path = f's3://soils-revealed/{dataset_type}.zarr'
    # Initilize the S3 file system
    s3 = s3fs.S3FileSystem(key=access_key_id, secret=secret_accsess_key)
    store = s3fs.S3Map(root=s3_path, s3=s3, check=False)
    # Read Zarr file
    ds = xr.open_zarr(store=store, group=group, consolidated=True)
    
    # Change coordinates names
    ds = ds.rename({'x': 'lon', 'y': 'lat'})
    
    # Change depth coord from 0 to 1 dimensional array
    depths = ds.coords.get('depth').values
    if depths.ndim == 0: 
        ds = ds.squeeze().drop("depth")
        ds = ds.assign_coords({"depth": np.array([depths])})
        
    return ds 

def compute_values(ds, geometry, years, depth, variable, dataset_type, group, nBinds, bindsRange):
    
    if dataset_type == 'global-dataset' and group == 'historic':
        start_date = years[0]
        end_date = years[1]
        mean_years = ds.coords.get('time').values
    else:
        start_date = np.datetime64(pd.DatetimeIndex([f'{years[0]}-12-31'])[0])
        end_date = np.datetime64(pd.DatetimeIndex([f'{years[1]}-12-31'])[0])
        mean_years = list(pd.DatetimeIndex(ds.coords.get('time').values).year)
    
    xmin, ymax, xmax, ymin = geometry.bounds
    ds_index = ds.where(ds['mask'].isin(0.0)).sel(depth='0-30', lon=slice(xmin, xmax), lat=slice(ymin, ymax))

    # Get difference between two dates
    diff = ds_index.loc[dict(time=end_date)] - ds_index.loc[dict(time=start_date)]
                    
    # Get counts and binds of the histogram
    if dataset_type == 'experimental-dataset' and variable == 'concentration':
        diff = diff[variable]/10.
    else:
        diff = diff[variable]
        
    h, bins = da.histogram(diff, bins=nBinds, range=bindsRange)
    
    with ProgressBar():
        counts = h.compute()
        mean_diff = diff.mean(skipna=True).values 
        mean_values = ds_index[variable].mean(['lon', 'lat']).values
        
    return counts, bins, mean_diff, mean_years, mean_values

def serializer(counts, bins, mean_diff, mean_years, mean_values):

    return {
        'counts': counts,
        'bins': bins,
        'mean_diff': mean_diff,
        'mean_years': mean_years,
        'mean_values':mean_values
    }

def analysis(request):
    request = request.get_json()
    
    # Read xarray.Dataset from Zarr in Amazon S3 bucket
    ds = read_dataset(request['dataset_type'], request['group'], access_key_id = os.getenv("S3_ACCESS_KEY_ID"), 
                      secret_accsess_key = os.getenv("S3_SECRET_ACCESS_KEY"))
    
    # Create the data mask by rasterizing the vector data
    geometry = Polygon(request['geometry'].get('features')[0].get('geometry').get('coordinates')[0])
    
    shapes = zip([geometry], range(1))
    da_mask = rasterize(shapes, ds.coords, longitude='lon', latitude='lat').rename('mask')
    ds['mask'] = da_mask   
    
    # Compute output values
    counts, bins, mean_diff, mean_years, mean_values = compute_values(ds, geometry, request['years'], request['depth'], 
                                                                      request['variable'], request['dataset_type'], 
                                                                      request['group'], request['nBinds'], 
                                                                      request['bindsRange'])
    
    return json.dumps(serializer(counts, bins, mean_diff, mean_years, mean_values), cls=NpEncoder)
