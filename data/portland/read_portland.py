# -*- coding: utf-8 -*-
"""
To read Portland's bicycle network.
"""

import geopandas as gpd
import folium

if __name__ == "__main__":
    net = gpd.read_file("Bicycle_Network.geojson")
    PORTLAND_COORD = [45.5428,-122.6544]
    m = folium.Map(location = PORTLAND_COORD, zoom_start = 12) 
    list_status = ["RECOMM", "ACTIVE", "RETIRED", "PLANNED"]
    color_dict = dict(RECOMM = "blue", ACTIVE = "green", 
                      RETIRED = "black", PLANNED = "red")
    size = dict()
    for stat in list_status :
        new_layer = folium.FeatureGroup(stat, show = False)
        batch_size = 0
        for ind in net[net["Status"] == stat].index:
            pos = []
            for val in list(net["geometry"][ind].coords[:]):
                pos.append(list(reversed(val)))
            folium.PolyLine(locations = pos,
                            color = color_dict[stat],
                            popup = "Length = {} \n Name = {}".format(
                                net["LengthMiles"][ind], 
                                net["SegmentName"][ind])
                            ).add_to(new_layer)
            if net["LengthMiles"][ind] > 0 :
                batch_size +=  net["LengthMiles"][ind]
        new_layer.add_to(m)
        size[stat] = batch_size
    folium.LayerControl().add_to(m)  
    m.save("./Portland_map.html")