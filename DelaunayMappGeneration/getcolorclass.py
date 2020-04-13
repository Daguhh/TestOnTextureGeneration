import matplotlib
from numpy import *
from numpy import *
from numpy import matlib
from matplotlib import pyplot as plt
from PIL import Image
from scipy import misc
from scipy.interpolate import interp2d
#from pathfinding_algo import find_ocean
plt.ion()


###################################################################################
def main_standalone() :
    generate_map_shape(size = 300, \
                       size_turb = 110, \
                       xpower = 100, \
                       ypower = 110, \
                       water_level = 0.60)




###################################################################################
class GetColorFromMap() :
    def __init__(self, voronoi_size) :

        self.map = generate_map_shape(size = 300, size_turb = 80, xpower = 90, ypower = 120, water_level = 0.60)
        self.cmap = matplotlib.cm.get_cmap('terrain')
        self.norm_color = matplotlib.colors.Normalize(vmin=amin(self.map), \
                                                vmax=amax(self.map))
        self.norm_pos = self.map.shape[0]/(voronoi_size+1)
        self.water_level = 0.60
#        self.water_map = find_ocean(self.map, self.water_level)

        self.water_map = self.cmap(0.01)
        self.cmap_ocean = self.cmap(0)
        self.cmap_lake = self.cmap(0.2)
        self.cmap_sand = self.cmap(0.5)
        self.cmap_forest = self.cmap(0.65)
        self.cmap_rock = self.cmap(0.8)
        self.cmap_snow = self.cmap(0.999)


    def get_color(self, pos) :
        arg = floor(pos*self.norm_pos).astype(dtype='uint32')
        ind_color = self.map[arg[0],arg[1]]
        color = self.cmap(ind_color)
        return color


    def iswater(self, pos) :
        arg = floor(pos*self.norm_pos).astype(dtype='uint32')
        water = self.water_map[arg[0],arg[1]]
        return water

    def get_color2(self, point) :
        mean_altitude = 0
##        mean_moisture = 0
##        mean_water = 0
        for bary in point.Bary :
            mean_altitude = mean_altitude + bary.altitude
##            mean_moisture = mean_moisture + bary.moisture
##            mean_water = mean_water + bary.water
        mean_altitude = mean_altitude/len(point.Bary)
##        mean_moisture = mean_moisture/len(point.Bary)
##        mean_water = mean_water/len(point.Bary)
        if point.water == 2 :
##            self.cmap(altitude)
            if mean_altitude > 0.60 :
                color = self.cmap_snow(self.moisture)
            elif mean_altitude > 0.5 :
                color = self.cmap_rock(self.moisture)
            elif mean_altitude > 0.4 :
                color = self.cmap_forest(self.moisture)
            else : # mean_altitude > 0.9 :
                color = self.cmap_sand(self.moisture)
        elif point.water == 1 :
            color = self.cmap_lake
        elif point.water == 0 :
            color = self.cmap_ocean
        else :
            color = zeros(3)
        return color



        print('pos=' + str(pos))
        arg = floor(pos*self.norm_pos).astype(dtype='uint32')
        ind_color = self.map[arg[0],arg[1]]
        color = self.cmap(ind_color)
        return color



##        arg = floor(pos*self.norm_pos).astype(dtype='uint32')
##        ind_color = self.map[arg[0],arg[1]]
##        if ind_color<0.60 :
##            color = WATER # water entre 0 et 0.06
##        return color






###################################################################################
##class name2color() :
##    def __init__(self)
##        self.water=[0,0.04] # water entre 0 et 20
##        self.sable # entre 40 et 60
##        montagne # >80
##
##


###################################################################################
def generate_map_shape(size = 100, size_turb = 50, xpower = 50, ypower = 50, water_level = 0.65) :
    continuer = 1
    plt.figure()
    while continuer :
##        size=100 #1000
##        size_turb=50 #300
        lambdax = 1
        lambday = 1
##        xpower = 50 #600
##        ypower = 50 #600

        param1 = 3 #7
        param2 = 0.7
##        water_level = 0.65
        water_brigtness = 15 # more = darker
        a=0
        l=0
##        plt.figure()
        while l<2 :


            mat0=random.rand(size_turb,size_turb)
            x0=arange(size_turb)
            y0=arange(size_turb)
            grids=[]

            pts=vstack((x0,y0))
            for j in arange(1,param1,1) :
                i=2**j
                x1=arange(0,size_turb,i)
                y1=arange(0,size_turb,i)
                f = interp2d(x0, y0, mat0)
                grid_z1=f(x1,y1)
                grids.append(grid_z1)


            per=1
            perlin_mat=empty((size_turb,size_turb))
            for mat in grids :
                mat=misc.imresize(mat,(size_turb,size_turb))
                per=per/param2
                perlin_mat = perlin_mat + mat*per

            perlin_mat=perlin_mat/amax(perlin_mat)
            perlin_cut=perlin_mat.copy()
##            plt.imshow(perlin_cut,cmap='terrain')
##            plt.show()
##            plt.pause(0.001)
            l=l+1

            perlin_cut=misc.imresize(perlin_cut,(size,size))
            perlin_cut=perlin_cut/amax(perlin_cut)
            if a == 0 :
                turb_x0=perlin_cut-amax(perlin_cut)/2
                a=1
            else :
                turb_y0=perlin_cut-amax(perlin_cut)/2

        x0=arange(size)-size/2
        y0=arange(size)-size/2
        X,Y=meshgrid(x0,y0)
        R=sqrt((X+turb_x0*xpower)**2/lambdax+(Y+turb_y0*ypower)**2/lambday)
        R=R/amax(R)
        mat0 = 1-R
        print(amax(mat0))
        mat0[(mat0<water_level)]=mat0[(mat0<water_level)]/water_brigtness
        plt.imshow(mat0,cmap='terrain')
        plt.pause(0.001)
##        wait = input('Y pour valider, N pour changer de map\n ...   ')
##        if wait == 'Y' :
        if 1 :
            continuer = 0

    return mat0



###################################################################################
if __name__ == '__main__' :
    mat = main_standalone()
##def distance_from_ocean :
##    pass








































