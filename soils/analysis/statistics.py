from datetime import datetime
import _pickle as pickle

import numpy as np
import pandas as pd
from shapely.geometry import Polygon
from xhistogram.xarray import histogram

import logging


from soils.analysis.serializers import serialize_general_stats
from soils.analysis.utils import rasterize, sort_dict, getArea
from soils.analysis.parameters import HistParams, LandCoverData


logger = logging.getLogger()

SCENARIOS = [
    "crop_I",
    "crop_MG",
    "crop_MGI",
    "grass_part",
    "grass_full",
    "rewilding",
    "degradation_ForestToGrass",
    "degradation_ForestToCrop",
    "degradation_NoDeforestation",
]

PIX_HA = 6.25


class SoilStatistics:
    """
    Class for computing soil statistics based on the given dataset, variable, years, depth, and geometry.

    Args:
        request (dict): The request containing the dataset, variable, years, depth, and geometry.

    Attributes:
        dataset (str): The dataset name.
        variable (str): The variable name.
        years (list): The years range.
        depth (float): The depth value.
        geometry (dict): The geometry coordinates.
        hist_params (HistParams): The histogram parameters.
        ds (xarray.Dataset): The dataset loaded from pickle.
    """

    def __init__(self, request: dict):
        self.dataset = request["dataset"]
        self.variable = request["variable"]
        self.years = request["years"]
        self.depth = request["depth"]
        self.geometry = request["geometry"]
        self.hist_params = HistParams(self.dataset, self.variable)
        self.polygon = Polygon(
            self.geometry["features"][0]["geometry"]["coordinates"][0]
        )
        self.ds = None

    def read_dataset(self):
        """
        Read the dataset from a pickle file.
        """
        with open(f"./soils/data/{self.dataset}_{self.variable}.pkl", "rb") as input:
            self.ds = pickle.load(input)

    def filter_dataset(self):
        """
        Filter the dataset based on the provided geometry.
        """

        xmin, ymin, xmax, ymax = self.polygon.bounds
        if self.ds:
            self.ds = self.ds.sel(lon=slice(xmin, xmax), lat=slice(ymax, ymin))
            shapes = zip([self.polygon], range(1))
            da_mask = rasterize(
                shapes, self.ds.coords, longitude="lon", latitude="lat"
            ).rename("mask")
            self.ds["mask"] = da_mask
        else:
            logger.error("Dataset is not loaded")
            raise Exception("Dataset is not loaded")

    def compute_statistics(self):
        """
        Compute the soil statistics.

        Returns:
            dict: The serialized general statistics.
        """
        if not self.ds:
            logger.error("Dataset is not loaded")
            raise Exception("Dataset is not loaded")

        if self.dataset == "historic":
            start_date = self.years[0]
            end_date = self.years[1]
        else:
            start_date = np.datetime64(
                datetime.strptime(f"{self.years[0]}-12-31", "%Y-%m-%d")
            )
            end_date = np.datetime64(
                datetime.strptime(f"{self.years[1]}-12-31", "%Y-%m-%d")
            )

        ds_index = self.ds.where(self.ds["mask"].isin(0.0)).sel(
            depth=self.depth, time=slice(start_date, end_date)
        )

        diff = ds_index.loc[dict(time=end_date)] - ds_index.loc[dict(time=start_date)]

        if (self.dataset == "experimental") and (self.variable == "stocks"):
            diff = diff[self.variable] / 10.0
        else:
            diff = diff[self.variable]

        n_bins = self.hist_params.n_binds()
        bin_ranges = self.hist_params.bind_ranges()

        bins = np.linspace(bin_ranges[0], bin_ranges[1], n_bins + 1)
        h = histogram(diff, bins=[bins], dim=["lat", "lon"], block_size=1)

        counts = h.values
        mean_diff = diff.mean(skipna=True).values

        if (self.dataset == "experimental") and (self.variable == "stocks"):
            mean_values = ds_index[self.variable].mean(["lon", "lat"]).values / 10.0
        else:
            mean_values = ds_index[self.variable].mean(["lon", "lat"]).values

        if self.dataset == "historic":
            mean_years = self.ds.coords.get("time").values
        else:
            mean_years = [
                int(str(x).split("-")[0]) for x in ds_index.coords.get("time").values
            ]

        if np.isnan(mean_diff):
            mean_diff = None

        mean_values = [None if np.isnan(x) else x for x in mean_values]

        return serialize_general_stats(counts, bins, mean_diff, mean_years, mean_values)

    def get_statistics(self) -> dict:
        """
        Get the soil statistics.

        Returns:
            dict: The serialized general statistics with area.
        """
        self.read_dataset()
        self.filter_dataset()
        data = self.compute_statistics()
        data.update({"area_ha": getArea(self.polygon) / 1e4})

        return data


class LandCoverStatistics:
    def __init__(self, request: dict, group_type: str):
        """
        Initialize the LandCoverStatistics class.

        Args:
            request: The request containing the geometry and other parameters.
            group_type: The type of group for which statistics are computed ('recent' or 'future').
        """
        self.geometry = request["geometry"]
        self.group_type = group_type
        self.scenarios = SCENARIOS
        self.lc_params = LandCoverData()
        self.ds = None
        self.data = {}  # type: dict #TODO improve typing
        self.polygon = Polygon(
            self.geometry["features"][0]["geometry"]["coordinates"][0]
        )

    def read_dataset(self):
        """
        Read the land cover dataset from a pickle file.
        """
        with open(f"./soils/data/land_cover_{self.group_type}.pkl", "rb") as input:
            self.ds = pickle.load(input)

    def filter_dataset(self):
        """
        Filter the land cover dataset based on the provided geometry.
        """
        if not self.ds:
            logger.error("Dataset is not loaded")
            raise Exception("Dataset is not loaded")
        # Get bbox and filter
        xmin, ymin, xmax, ymax = self.polygon.bounds
        self.ds = self.ds.sel(x=slice(xmin, xmax), y=slice(ymax, ymin))
        # Create the data mask by rasterizing the geometry
        shapes = zip([self.polygon], range(1))
        da_mask = rasterize(shapes, self.ds.coords, longitude="x", latitude="y").rename(
            "mask"
        )
        self.ds["mask"] = da_mask
        # Filter by mask
        self.ds = self.ds.where(self.ds["mask"].isin(0.0))

    def compute_recent_statistics(self):
        """
        Compute recent land cover change statistics.

        Returns:
            A dictionary containing the computed statistics.
        """
        if not self.ds:
            logger.error("Dataset is not loaded")
            raise Exception("Dataset is not loaded")
        # Filter dataset
        df = pd.concat(
            [
                self.ds.isel(time=0)
                .to_dataframe()
                .reset_index()
                .drop(columns=["x", "y", "time"])
                .rename(
                    columns={"stocks": "stocks_2000", "land-cover": "land_cover_2000"}
                ),
                self.ds.isel(time=1)
                .to_dataframe()
                .reset_index()
                .drop(columns=["x", "y", "time", "mask"])
                .rename(
                    columns={"stocks": "stocks_2018", "land-cover": "land_cover_2018"}
                ),
            ],
            axis=1,
        )
        # Filter rows where columns A and B have equal values
        df = df[df["land_cover_2000"] != df["land_cover_2018"]]
        df["stocks_change"] = df["stocks_2018"] - df["stocks_2000"]
        # Remove rows where mask is null
        df = df[~df["mask"].isnull()]
        # Remove rows with 0 change
        df = df[df["stocks_change"].notnull() & (df["stocks_change"] != 0.0)]
        # Add category names
        df = df[["land_cover_2018", "land_cover_2000", "stocks_change"]]
        df["land_cover_2000"] = df["land_cover_2000"].astype(int).astype(str)
        df["land_cover_2018"] = df["land_cover_2018"].astype(int).astype(str)
        df = df.assign(
            land_cover_group_2000=df["land_cover_2000"].map(
                self.lc_params.child_parent()
            ),
            land_cover_group_2018=df["land_cover_2018"].map(
                self.lc_params.child_parent()
            ),
        )

        # Create final data
        indicators = {
            "land_cover_groups": ["land_cover_group_2000", "land_cover_group_2018"],
            "land_cover": ["land_cover_2000", "land_cover_2018"],
            "land_cover_group_2018": ["land_cover_2000", "land_cover_group_2018"],
        }

        for name, indicator in indicators.items():
            # Grouping the DataFrame by land cover 2000 and 2018, and applying the aggregation function to 'stocks_change'
            grouped_df = df.groupby(indicator)["stocks_change"].sum().reset_index()
            grouped_2018_df = (
                grouped_df.groupby([indicator[1]])["stocks_change"].sum().reset_index()
            )

            data_tmp = {}
            for category in grouped_2018_df.sort_values("stocks_change")[indicator[1]]:
                records = grouped_df[grouped_df[indicator[1]] == category].sort_values(
                    "stocks_change"
                )
                records = dict(zip(records[indicator[0]], records["stocks_change"]*PIX_HA))
                data_tmp[category] = records

            self.data[name] = data_tmp

        # Reorganize land cover data
        children = list(self.data["land_cover"].keys())
        parent = [self.lc_params.child_parent()[child] for child in children]
        child_dict = dict(zip(children, parent))

        land_cover_dict = {}
        for parent_id in list(self.data["land_cover_groups"].keys()):
            child_ids = [key for key, value in child_dict.items() if value == parent_id]
            land_cover_dict[parent_id] = {
                id: self.data["land_cover"][id] for id in child_ids
            }

        self.data["land_cover"] = land_cover_dict

        return self.data

    def compute_future_statistics(self):
        """
        Compute future land cover change statistics.

        Returns:
            A dictionary containing the computed statistics.
        """
        if not self.ds:
            logger.error("Dataset is not loaded")
            raise Exception("Dataset is not loaded")
        # Filter dataset
        df = (
            self.ds.isel(time=0)
            .to_dataframe()
            .reset_index()
            .drop(columns=["x", "y", "time"])
        )
        # Remove rows where mask is null
        df = df[~df["mask"].isnull()]
        ## Add category names
        df = df[["land-cover"] + self.scenarios].rename(
            columns={"land-cover": "land_cover"}
        )
        df["land_cover"] = df["land_cover"].astype(int).astype(str)
        df["land_cover_groups"] = df["land_cover"].map(self.lc_params.child_parent())

        # Create final data
        indicators = {
            "land_cover": ["land_cover_groups", "land_cover"],
            "land_cover_groups": ["land_cover_groups"],
        }

        for name, indicator in indicators.items():
            data_tmp = {}
            for scenario in self.scenarios:
                df_sum = df.groupby(indicator)[scenario].sum().reset_index()

                records = dict(zip(df_sum[name], df_sum[scenario]*PIX_HA))

                data_tmp[scenario] = records

                # Reorder dictionary
            # sorted_keys = sorted(data_tmp.keys(), key=lambda x: sum(data_tmp[x].values()))
            # data_tmp = {key: data_tmp[key] for key in sorted_keys}
            data_tmp = sort_dict(data_tmp)

            self.data[name] = data_tmp

        return self.data

    def get_statistics(self):
        """
        Get land cover change statistics.

        Returns:
            A dictionary containing the computed statistics.
        """
        self.read_dataset()
        self.filter_dataset()
        # Get land cover statistics
        if self.group_type == "recent":
            self.data = self.compute_recent_statistics()
        elif self.group_type == "future":
            self.data = self.compute_future_statistics()

        return self.data
