import numpy as np
import xarray as xr
from affine import Affine
from rasterio import features
from pyproj import Geod

import logging

logger = logging.getLogger()


def transform_from_latlon(lat, lon):
    lat = np.asarray(lat)
    lon = np.asarray(lon)
    trans = Affine.translation(lon[0], lat[0])
    scale = Affine.scale(lon[1] - lon[0], lat[1] - lat[0])
    return trans * scale


def rasterize(
    shapes, coords, latitude="latitude", longitude="longitude", fill=np.nan, **kwargs
):
    """Rasterize a list of (geometry, fill_value) tuples onto the given
    xray coordinates. This only works for 1d latitude and longitude
    arrays.
    """
    transform = transform_from_latlon(coords[latitude], coords[longitude])
    out_shape = (len(coords[latitude]), len(coords[longitude]))
    raster = features.rasterize(
        shapes,
        out_shape=out_shape,
        fill=fill,
        transform=transform,
        dtype=float,
        **kwargs,
    )
    spatial_coords = {latitude: coords[latitude], longitude: coords[longitude]}
    return xr.DataArray(raster, coords=spatial_coords, dims=(latitude, longitude))


def sort_dict(my_dict):
    # Sort secondary keys in each sub-dictionary
    for key in my_dict:
        my_dict[key] = dict(sorted(my_dict[key].items(), key=lambda x: x[1]))

    # Sort primary keys by the sum of secondary key values
    my_dict = dict(sorted(my_dict.items(), key=lambda x: sum(x[1].values())))

    return my_dict


def getArea(shape):
    """
    calculate the area of a geometry in square meters based on a WGS84 ellipsoid

    Args:
        shape (shapely.geometry): The geometry to reproject.

    Returns:
        float: The area of the geometry in square meters.
    """
    geod = Geod(ellps="WGS84")

    return abs(geod.geometry_area_perimeter(shape)[0])
