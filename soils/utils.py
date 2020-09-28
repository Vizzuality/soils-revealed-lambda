def binds(dataset,variable):
    binds_dic = {
        "experimental": {'stocks': 80, 'concentration': 80},
        "historic": {'stocks': 40},
        "recent": {'stocks': 10}
    }

    return binds_dic[dataset][variable]

def ranges(dataset,variable):
    ranges_dic = {
        "experimental": {'stocks': [-50, 50], 'concentration': [-10, 10]},
        "historic": {'stocks': [-40,40]},
        "recent": {'stocks': [-5,5]}
    }

    return ranges_dic[dataset][variable]
