from datetime import datetime
import _pickle as pickle
import logging
import os

import numpy as np
import xarray as xr
from rasterio import features
from shapely.geometry import Polygon
from xhistogram.xarray import histogram
import pyproj
import shapely.ops as ops
from functools import partial

from soils.analysis.serializers import serialize_general_stats
from soils.analysis.utils import transform_from_latlon
from soils.analysis.parameters import HistParams

logger = logging.getLogger()
logger.setLevel(logging.INFO)


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


def compute_values(ds, geometry, dataset, variable, years, depth):
    hist_params = HistParams(dataset, variable)
    if dataset == 'historic':
        start_date = years[0]
        end_date = years[1]
    else:
        start_date = np.datetime64(datetime.strptime(f'{years[0]}-12-31', "%Y-%m-%d"))
        end_date = np.datetime64(datetime.strptime(f'{years[1]}-12-31', "%Y-%m-%d"))

    xmin, ymax, xmax, ymin = geometry.bounds
    ds_index = ds.where(ds['mask'].isin(0.0)).sel(depth=depth, lon=slice(xmin, xmax), lat=slice(ymin, ymax), time=slice(start_date, end_date))

    # Get difference between two dates
    diff = ds_index.loc[dict(time=end_date)] - ds_index.loc[dict(time=start_date)]

    # Get counts and binds of the histogram
    if (dataset == 'experimental') and (variable == 'stocks'):
        diff = diff[variable] / 10.
    else:
        diff = diff[variable]

    nBinds = hist_params.n_binds()
    bindsRange = hist_params.bind_ranges()

    bins = np.linspace(bindsRange[0], bindsRange[1], nBinds + 1)
    h = histogram(diff, bins=[bins], dim=['lat', 'lon'], block_size=1)

    counts = h.values
    mean_diff = diff.mean(skipna=True).values
    if (dataset == 'experimental') and (variable == 'stocks'):
        mean_values = ds_index[variable].mean(['lon', 'lat']).values / 10.
    else:
        mean_values = ds_index[variable].mean(['lon', 'lat']).values

    if dataset == 'historic':
        mean_years = ds.coords.get('time').values
    else:
        mean_years = [int(str(x).split('-')[0]) for x in ds_index.coords.get('time').values]

    # Replace NaNs with ""
    if np.isnan(mean_diff):
        mean_diff = None

    mean_values = [None if np.isnan(x) else x for x in mean_values]

    return counts, bins, mean_diff, mean_years, mean_values


def statistics(request):
    # Read xarray.Dataset from pkl
    dataset = request['dataset']
    variable = request['variable']

    parent = os.getcwd()

    # Read xarray.Dataset from pkl
    with open(f'./soils/data/{dataset}_{variable}.pkl', 'rb') as input:
        ds = pickle.load(input)

    # Create the data mask by rasterizing the geometry
    geometry = Polygon(request['geometry'].get('features')[0].get('geometry').get('coordinates')[0])

    # Get area
    geom_area = ops.transform(
        partial(
            pyproj.transform,
            pyproj.Proj(init='EPSG:4326'),
            pyproj.Proj(
                proj='aea',
                lat_1=geometry.bounds[1],
                lat_2=geometry.bounds[3])),
        geometry)
    area = geom_area.area/ 1e+4

    # Get bbox and filter
    xmin, ymax, xmax, ymin = geometry.bounds
    ds = ds.sel(lon=slice(xmin, xmax), lat=slice(ymin, ymax))

    # Rasterize geometry
    shapes = zip([geometry], range(1))
    da_mask = rasterize(shapes, ds.coords, longitude='lon', latitude='lat').rename('mask')
    ds['mask'] = da_mask

    # Compute output values
    counts, bins, mean_diff, mean_years, mean_values = compute_values(ds, geometry, request['dataset'], request['variable'], request['years'], request['depth'])

    return serialize_general_stats(counts, bins, mean_diff, mean_years, mean_values, area)
