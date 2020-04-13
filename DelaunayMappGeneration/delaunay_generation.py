from numpy import *
from matplotlib import pyplot as plt
import time

plt.ion()
show_plot = 1
show_plot_cercle = 0
##############################################################################"
def main_delaunay_generation(size_grid = 100, density = 1, grid_step = 1) :
    tic = time.time()
    # main function, return delaunay triangles and their circonscrit circle center
    delaunay = DeLaunayList()
    print("GRID_SIZE = " + str(size_grid))
    if show_plot :
        plt.figure()
    rand_pts = random_density_grid(size_grid, density, grid_step)

    delaunay.rand_pts = rand_pts
    zone_step = floor(size_grid/(3/density))
    zones = zonage(rand_pts, size_grid, density, zone_step)

    l=0; k=0
    for i in arange(len(zones)) :
        for j in arange(len(zones[i])) :
            P_zone = zones[i][j]
            Q_zone = empty(0)
            if i==(len(zones)-1) :
                for a in zones[i] :
                    Q_zone = hstack((Q_zone,a)).astype(dtype='uint32')
                for b in zones[i-1] :
                    Q_zone = hstack((Q_zone,b)).astype(dtype='uint32')
            else :
                for a in arange(-1,2) :
                    for b in arange(-1,2) :
                        try :
                            if (i+a)>=0 and (j+b)>=0 and (i+a)<len(zones) and (j+b)<len(zones[i]):
                                Q_zone =  hstack((Q_zone,zones[i+a][j+b])).astype(dtype='uint32')
                        except :
                            pass
##                            print(len(zones))
##                            print(len(zones[i]))
##                            print('out of range')
##                            print("i = %d, a = %d, j = %d, b = %d " %(i, a, j, b))


##            plt.plot(rand_pts[Q_zone,0],rand_pts[Q_zone,1],linewidth = 20)
##            plt.show()
##            plt.pause(0.001)



            for P in P_zone :
                delaun_point = find_voisin(rand_pts, Q_zone, P, delaunay)
                delaunay.Liste = delaun_point
                l=l+1; k=k+1
                if k>100 :
                    k=0
                    s = l*100/rand_pts.shape[0]
                    toc = time.time()
                    temps = (toc-tic)
                    temps = temps*100/s-temps
                    print('=======  %d.4 %%  =====  time left : %d.4 sec =====' %(s, temps))
##                    plt.show()
##                    plt.pause(0.001)
    temps = toc-tic
    print('elapsed time : %d.4' %temps)
    if show_plot :
        plt.show()
    return delaunay


##############################################################################"
def random_density_grid(size_grid, density, grid_step) :

    # genere des points dans chaque case de la grille en fonction de la densité
    x_grid = arange(0,size_grid,grid_step)
    y_grid = arange(0,size_grid,grid_step)
    x0=y0=0
    xend=yend=size_grid
    x_pt=empty((0,1))
    y_pt=empty((0,1))
    pt_list=list()
    k=0
    for i in x_grid :
        for j in y_grid :
            test=random.rand()
            if density >= test :
                k=k+1
                x_tp = random.rand()*grid_step + (i)
                y_tp = random.rand()*grid_step + (j)
                x_pt = vstack((x_pt,x_tp))
                y_pt = vstack((y_pt,y_tp))
    pt_array=hstack((x_pt,y_pt))

    # add border point
    x_low = empty((size_grid,2))
    x_up = empty((size_grid,2))
    y_left = empty((size_grid,2))
    y_right = empty((size_grid,2))
    x_low[:,0] = arange(0,size_grid,1)+1
    x_up[:,0] = arange(0,size_grid,1)
    y_left[:,1] = arange(0,size_grid,1)
    y_right[:,1] = arange(0,size_grid,1)+1
    x_low[:,1] = -(x_low[:,0]-size_grid/2)**2/size_grid**3
    x_up[:,1] = size_grid  + (x_low[:,0]-size_grid/2)**2/size_grid**3
    y_left[:,0] = -(x_low[:,0]-size_grid/2)**2/size_grid**3
    y_right[:,0] = size_grid +(x_low[:,0]-size_grid/2)**2/size_grid**3
    pt_array = vstack((pt_array,x_low,x_up,y_right,y_left))

    if show_plot :
        plt.plot(pt_array[:,0],pt_array[:,1],'.')
        plt.pause(0.001)
    return pt_array


##############################################################################"
def find_voisin(rand_pts, Q_zone, P, delaunay) :

    # creation d'un point
    delau_point = DeLaunayPoint()
    delau_point.indice = P

    # changement de base
    pts = rand_pts
    ptsQ=empty((Q_zone.shape[0],2))
    ptsQ = rand_pts[Q_zone,:]
    P = int(argwhere(P==Q_zone))

    # P = reference du point central
    p = ptsQ[P,:]

    # find Q (closest point)
    temp=1000*ones(ptsQ.shape[0])
    for i in arange(ptsQ.shape[0]) :
        q=ptsQ[i,:]
        if (i!=P) :
            temp[i]=(dot(q-p,q-p))
    Q = argmin(temp)
    q = ptsQ[Q,:]
    R = array([Q])
    r = q

    # find R (next point on the right)
    continuer = 1; k = 1; TRI = list()
    while continuer  :

        # creation d'un point barycentre
        delau_bary = DeLaunayBary()

        PRQ = empty((ptsQ.shape[0],1)) # angle a maximiser
        q = r # pt de départ
        Q = R[k-1]
        cmpt = 0 # décompte des points "inatégnables"
        for i in arange(ptsQ.shape[0]) :
            r = ptsQ[i,:]
            # cherche point a droite de Q et != de P
            if i == P  or cross(q-p,r-p)>=0 :
                PRQ[i] = -1 # point au bord de la grille
                cmpt = cmpt + 1 # => fin de la recherche lorque cmpt = nbpt
                continue
            else :
                QR = sqrt(   (q[0]-r[0])**2 + (q[1]-r[1])**2   )
                PR = sqrt(   (p[0]-r[0])**2 + (p[1]-r[1])**2   )
                PRQ[i] = arccos( dot(p-r,q-r) / (QR*PR) ) # calcul de l'angle à maximiser

        # enregistrement pts ou fin de recherche
        if cmpt > ptsQ.shape[0]-1 : # aucun point ne convient
            break
        else :
            R = vstack((R,argmax( PRQ ))) # on enregiste les indices des triangles
            r = hstack((ptsQ[R[k],0],ptsQ[R[k],1])) # combine coordonées x et y
            tri = vstack((p,q,r,p)) # trace triangles
            if show_plot :
                plt.plot(tri[:,0],tri[:,1])
##                plt.show()
##                plt.pause(0.1)

            # save triangle and its barycenter
            #print("Q_zone = " + str(Q_zone))
            #print("Q_zoneP = " + str(Q_zone[P]))
            #print("Q_zoneQ = " + str(Q_zone[Q]))
            #print("Rk = " + str(R[k][0]))
            #print("Q_zoneRk = " + str(Q_zone[R[k][0]]))
            #print("bary = " + str(delaunay.Liste))
            temp = [Q_zone[P],int(Q_zone[Q]),Q_zone[R[k][0]]]
            #print(temp)
            temp = sort(temp)
            #print(temp)
            temp = ','.join('{:03X}'.format(a) for a in temp)
            delau_bary.Tri = temp
            test, pos = list_comp(delaunay, temp)
            if test :
                delau_bary.Pos = pos
##                print('save =' + str(save))
            else :
                delau_bary.Pos = barycentre(tri)
##                print('temp =' + str(temp))


##            delau.Tri = vstack((Q_zone[P],Q_zone[Q],Q_zone[R[k]]))
##            delau.Bary = barycentre(tri)
        delau_point.Bary = delau_bary
        # si on a fait un tour complet
        if (R[k]==R[0]) :
            break
        k=k+1

    return delau_point


##############################################################################"
# calcul barycentre des triangles
def barycentre(triangle) :
    p = triangle[0,:]
    q = triangle[1,:]
    r = triangle[2,:]

    x1=q[0]
    y1=q[1]
    x2=r[0]
    y2=r[1]
    x3=p[0]
    y3=p[1]

    try :
        equ1 = (x3**2-x2**2+y3**2-y2**2)/(2*(y3-y2))
        equ2 = (x2**2-x1**2+y2**2-y1**2)/(2*(y2-y1))
        equ3 = (x2-x1)/(y2-y1)-(x3-x2)/(y3-y2)
        X = -(equ1-equ2)/equ3
    except :
        print('erreur : ', erreure)
        print('echec calcul X : x1=%s y1=%s x2=%s y2=%s x3=%s y3=%s' %(x1,y1,x2,y2,x3,y3))

    try :
        equ4 = -(x2-x1)/(y2-y1)*X
        equ5 = (x2**2-x1**2+y2**2-y1**2) / (2*(y2-y1))
        Y = equ4 + equ5
    except :
        print('erreur : ', erreure)
        print('echec calcul Y : x1=%s y1=%s x2=%s y2=%s x3=%s y3=%s' %(x1,y1,x2,y2,x3,y3))

    centre=array([X,Y])
    if show_plot_cercle :
        plt.plot(centre[0],centre[1],'.')

    # trace cercles
    if show_plot_cercle :
        rayon = sqrt(dot(p-centre,p-centre))
        theta = linspace(0,2*pi,40)
        x_cercle = rayon*cos(theta)+centre[0]
        y_cercle = rayon*sin(theta)+centre[1]
        plt.plot(x_cercle,y_cercle)

    return centre

##############################################################################"
class DeLaunayList :
    def __init__(self) :
        self.liste = list()
        self.rand_pts = 0

    def _set_Liste(self, point) :
        self.liste.append(point)
    def _get_Liste(self) :
        return self.liste
    Liste = property(_get_Liste, _set_Liste)


##############################################################################"
class DeLaunayPoint :
    def __init__(self) :
        self.indice = int()
        self.bary = list()

    # stocke les barycentres des triangles "Tri"
    def _set_Bary(self, bary) :
        self.bary.append(bary)
    def _get_Bary(self) :
        return self.bary
    Bary = property(_get_Bary, _set_Bary)
##        self.color = empty(0)
##        self.pos=[]
##        self.water=[]
##        self.altitude=[]
##        self.moisture=[]

class DeLaunayBary :
    def __init__(self) :
        self.triangle = []
        self.pos = []
        self.water = 0
        self.altitude = 0
        self.moisture = 0

    def _set_Tri(self, triangle) :
        self.triangle.append(triangle)
    def _get_Tri(self) :
        return self.triangle

    def _set_Pos(self, pos) :
        self.pos.append(pos)
    def _get_Pos(self) :
        return self.pos

    Pos = property(_get_Pos, _set_Pos)
    Tri = property(_get_Tri, _set_Tri)

class BaryPoint :
    def __init__(self) :
        self.pos=[]
        self.water=[]
        self.altitude=[]
        self.moisture=[]

##    def color(self) :


def list_comp(delaunay, value):
    test = False
    pos = []
    for delau_point in delaunay.Liste :
##        print(delau_point.Bary[0].Pos)
        for bary in delau_point.Bary :
#            print("bary.tru = " + str(bary.Tri))
            if bary.Tri==value :
                test = True
                pos = bary.Pos
                break
    return test , pos


###############################################################################
 # divise la grille en plus petites parties
def zonage(rand_pts, size_grid, density, zone_step) :

    arg = argsort(rand_pts[:,0])
    step = floor(size_grid/zone_step*size_grid*density)
    X = arange(0, arg.shape[0], step)
    X = hstack((X,arg.shape[0]))
    X = X.astype(dtype='uint32')
    zonei=list()

    for i in arange(X.shape[0]-1) :
        indice = arg[arange(X[i],X[i+1],1)]
        arg2 = argsort(rand_pts[indice,1])
        step2 = floor(density*X[1]/zone_step)
        Y = arange(0,arg2.shape[0], step2)
        Y = hstack((Y,arg2.shape[0]))
        Y = Y.astype(dtype='uint32')
        zonej=list()
        for j in arange(Y.shape[0]-1) :
            indice2 = arg2[arange(Y[j],Y[j+1],1)]
            zonelist=list()
            zone = indice[indice2]
            zonelist=list(zone)
            pts = rand_pts[zone,:]
##            plt.plot(pts[:,0],pts[:,1],linewidth = 0.3)
##            plt.show()
##            plt.pause(0.001)
            zonej.append(zonelist)
        zonei.append(zonej)
    return zonei



### exectution du programme


if __name__ == '__main__' :
    show_plot = 1
    delaunay = main_delaunay_generation(size_grid = 20, density = 1, grid_step = 1)













