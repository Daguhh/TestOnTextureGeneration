import matplotlib
from numpy import *


class GetColorFromMap() :
    def __init__(self, voronoi_size) :

        self.map = generate_map_shape()
        self.cmap = matplotlib.cm.get_cmap('terrain')
        self.norm_color = matplotlib.colors.Normalize(vmin=amin(self.map), \
                                                vmax=amax(self.map))
        self.norm_pos = self.map.shape[0]/voronoi_size

    def get_color(self, pos) :
        arg = round(pos*self.norm_pos)
        ind_color = self.map(arg)
        color = self.cmap(ind_color)
        return color
       
        










































