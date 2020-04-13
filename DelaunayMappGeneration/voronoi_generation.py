from numpy import *
from matplotlib import pyplot as plt
from delaunay_generation import main_delaunay_generation as delaunay_gen
import pickle
from matplotlib.path import Path
import matplotlib.patches as patches
from getcolorclass import *

#####################################################################################
####    delaunay structure :                        #################################
####        delaunay.Liste                          #################################
####        delaunay.rand_pts                       #################################
####                                                #################################
####        delaunay.Liste[i].indice                #################################
####        delaunay.Liste[i].Tri[j]                #################################
####        delaunay.Liste[i].Bary[j]               #################################
####                                                #################################
####        delaunay.Liste[i].water                 #################################
####        delaunay.Liste[i].moisture              #################################
####        delaunay.Liste[i].altitude              #################################
####                                                #################################
####        delaunay.Liste[i].Bary[j].pos           #################################
####        delaunay.Liste[i].Bary[j].water         #################################
####        delaunay.Liste[i].Bary[j].altitude      #################################
####        delaunay.Liste[i].Bary[j].moisture      #################################
####        delaunay.Liste[i].Bary[j].tri           #################################
#####################################################################################

def main_voronoi() :

    size_grid = 15
    density = 1
    grid_step = 1
    affichage = 'Polygone'

    delaunay = delaunay_gen(size_grid, density, grid_step)
##    return delaunay

    ##    gcfm = GetColorFromMap(size_grid)
##    if affichage == 'Polygone' or affichage == 'Polygone2':
    gcfm = GetColorFromMap(size_grid)

    ####plt.figure()
    fig = plt.figure()
    ax = fig.add_subplot(111)
    if 1 :
        for delau_point in delaunay.Liste :
            if affichage == 'Point' :
                print("point")
                x = empty(0)
                y = empty(0)
                for bary in delau_point.Bary :
                    x = hstack((x,bary.Pos[0][0]))
                    y = hstack((y,bary.Pos[0][1]))
                try :
                    x = hstack((x,x[0]))
                    y = hstack((y,y[0]))
                    ax.plot(x,y)
                except :
                    print('x = %s, y = %s' %(x,y))



            elif affichage == 'Polygone' :
                nverts = len(delau_point.Bary)+1
                verts = empty((0,2))
                for bary in delau_point.Bary :
                    verts = vstack((verts,bary.Pos))
                try :
##                if 1 :
                    verts = vstack((verts,verts[0,:]))
                    verts[verts[:,0]<=0,0] = 0
                    verts[verts[:,1]<=0,1] = 0
                    verts[verts[:,0]>size_grid,0] = size_grid
                    verts[verts[:,1]>size_grid,1] = size_grid
                    codes = ones(nverts, int) * Path.LINETO
                    codes[0] = Path.MOVETO
                    codes[nverts-1] = Path.CLOSEPOLY
                    path = Path(verts, codes)
                    ind = delau_point.indice
                    arg_color = delaunay.rand_pts[ind]
                    if arg_color[0]<0 : arg_color[0] = 0
                    if arg_color[1]<0 : arg_color[1] = 0
                    color = gcfm.get_color(arg_color)
                    patch = patches.PathPatch(path, facecolor=color, edgecolor='none')
                    ax.add_patch(patch)
                except :
                    print('!!!!!!!!!!    attention   !!!!!!!!!!! \n poly_position= %s' %verts)




    elif affichage == 'Polygone2' :

        point_water_array = empty((0,2))
        for point in delaunay.Liste :
            arg_color = delaunay.rand_pts[point.indice]
            if arg_color[0]<0 :
                arg_color[0] = 0
            if arg_color[1]<0 :
                arg_color[1] = 0

            # define water of point
            point.water = gcfm.iswater(arg_color)
##            print('water : ' + str(point.water))
            if point.water == 0 :
                point_water_array = vstack((point_water_array,arg_color))

        for point in delaunay.Liste :
            for bary in point.Bary :
                if bary.pos[0][0] < 0 : bary.pos[0][0] = 0
                if bary.pos[0][1] < 0 : bary.pos[0][1] = 0
                if bary.pos[0][0] > size_grid : bary.pos[0][0] = size_grid
                if bary.pos[0][1] > size_grid : bary.pos[0][1] = size_grid

                dist_from_ocean = sqrt(amin((point_water_array[:,0]-bary.pos[0][0])**2 + \
                                       (point_water_array[:,1]-bary.pos[0][1])**2))
                bary.altitude = dist_from_ocean


        delaunay, max_altitude = norm_altitude(delaunay)
        show_polygones(delaunay, size_grid, gcfm)

    plt.xlim([0,size_grid])
    plt.ylim([0,size_grid])
    plt.show()

    plt.pause(60)
    fichier_nom = ("fichier_delaunay%sx%s.txt" %(size_grid, size_grid))
    mon_fichier = open(fichier_nom, "w")
    with open('donnees', 'wb') as fichier:
        mon_pickler = pickle.Pickler(fichier)
        mon_pickler.dump(delaunay)

    ##
    ##with open('donnees', 'rb') as fichier:
    ##    mon_depickler = pickle.Unpickler(fichier)
    ##    data = mon_depickler.load()




def show_polygones(delaunay, size_grid, gcfm) :

    fig = plt.figure()
    ax = fig.add_subplot(111)
    for point in delaunay.Liste :
            nverts = len(point.Bary)+1
            verts = empty((0,2))
            for bary in point.Bary :
                verts = vstack((verts,bary.pos))
            try :
##            if 1 :
                verts = vstack((verts,verts[0,:]))

                # modifie point hors zone
                verts[verts[:,0]<=0,0] = 0
                verts[verts[:,1]<=0,1] = 0
                verts[verts[:,0]>size_grid,0] = size_grid
                verts[verts[:,1]>size_grid,1] = size_grid

                # definition du polygone
                codes = ones(nverts, int) * Path.LINETO
                codes[0] = Path.MOVETO
                codes[nverts-1] = Path.CLOSEPOLY
                path = Path(verts, codes)

                couleur = gcfm.get_color2(point)

                # plot
                patch = patches.PathPatch(path, facecolor=couleur, edgecolor='none')
                ax.add_patch(patch)
            except :
                print('!!!!!!!!!!    attention   !!!!!!!!!!! \n poly_position= %s' %verts)
    plt.show()


def norm_altitude(delaunay) :
    max_altitude = 0
    for point in delaunay.Liste :
        for bary in point.Bary :
            if bary.altitude > max_altitude :
                max_altitude = bary.altitude
    for point in delaunay.Liste :
        for bary in point.Bary :
            bary.altitude = bary.altitude/(max_altitude)
##            print(bary.altitude)
    return delaunay, max_altitude



if __name__ == '__main__' :
    delaunay = main_voronoi()

















