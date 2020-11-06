def binds(dataset,variable):
    binds_dic = {
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
    }

    return binds_dic[dataset][variable]

def ranges(dataset,variable):
    ranges_dic = {
        "experimental": {'stocks': [-50, 50], 'concentration': [-10, 10]},
        "historic": {'stocks': [-40,40]},
        "recent": {'stocks': [-5,5]},
        "crop_I": {'stocks': [0,30]}, 
        "crop_MG": {'stocks': [0,30]}, 
        "crop_MGI": {'stocks': [0,30]}, 
        "grass_part": {'stocks': [0,30]}, 
        "grass_full": {'stocks': [0,30]}, 
        "rewilding": {'stocks': [-30,30]}, 
        "degradation_ForestToGrass": {'stocks': [-50,1]}, 
        "degradation_ForestToCrop": {'stocks': [-50,1]}, 
        "degradation_NoDeforestation": {'stocks': [-50,1]}        

    }

    return ranges_dic[dataset][variable]
