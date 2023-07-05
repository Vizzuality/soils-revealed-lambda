from dataclasses import dataclass


@dataclass
class HistParams:
    dataset: str
    variable: str

    def n_binds(self):
        return {
        "experimental": {'stocks': 80, 'concentration': 20},
        "historic": {'stocks': 40},
        "recent": {'stocks': 10},
        "crop_I": {'stocks': 30},
        "crop_MG": {'stocks': 30},
        "crop_MGI": {'stocks': 30},
        "grass_part": {'stocks': 30},
        "grass_full": {'stocks': 30},
        "rewilding": {'stocks': 60},
        "degradation_ForestToGrass": {'stocks': 51},
        "degradation_ForestToCrop": {'stocks': 51},
        "degradation_NoDeforestation": {'stocks': 51}
        }[self.dataset][self.variable]

    def bind_ranges(self):
        return {
        "experimental": {'stocks': [-50, 50], 'concentration': [-10, 10]},
        "historic": {'stocks': [-40,40]},
        "recent": {'stocks': [-50,50]},
        "crop_I": {'stocks': [0,30]},
        "crop_MG": {'stocks': [0,30]},
        "crop_MGI": {'stocks': [0,30]},
        "grass_part": {'stocks': [0,30]},
        "grass_full": {'stocks': [0,30]},
        "rewilding": {'stocks': [-30,30]},
        "degradation_ForestToGrass": {'stocks': [-50,1]},
        "degradation_ForestToCrop": {'stocks': [-50,1]},
        "degradation_NoDeforestation": {'stocks': [-50,1]}
        }[self.dataset][self.variable]



@dataclass
class LandCoverData:
    def child_parent(self):
        return {"0": "0",
                "10": "1",
                "11": "1",
                "12": "2",
                "20": "1",
                "30": "1",
                "40": "1",
                "50": "2",
                "60": "2",
                "61": "2",
                "62": "2",
                "70": "2",
                "71": "2",
                "72": "2",
                "80": "2",
                "81": "2",
                "82": "2",
                "90": "2",
                "100": "2",
                "110": "3",
                "120": "3",
                "121": "3",
                "122": "3",
                "130": "3",
                "140": "3",
                "150": "3",
                "151": "3",
                "152": "3",
                "153": "3",
                "160": "4",
                "170": "5",
                "180": "4",
                "190": "6",
                "200": "7",
                "201": "7",
                "202": "7",
                "210": "8",
                "220": "9"}
