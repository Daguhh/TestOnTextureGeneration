from numpy import *
from numpy import matlib

from matplotlib import pyplot as plt
from PIL import Image
from scipy import misc
from scipy.interpolate import interp2d
from matplotlib import cm
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

import math
from matplotlib.pyplot import *
from numpy import *
from matplotlib.path import Path
import matplotlib.patches as patches


plt.ion()

################################################################################
class CreateColorMap() :
    def __init__(self) :
        self.Brown()

    def Brown(self) :
        cdict1 = {'red':  ((0.0, 0/255,   0/255),
                           (1.0, 190/255, 190/255)),
                 'green': ((0.0, 0/255,   0/255),
                           (1.0, 62/255,  62/255)),
                 'blue':  ((0.0, 0/255,   0/255),
                           (1.0, 62/255,  62/255))}
        self.brown = LinearSegmentedColormap('brown', cdict1)


################################################################################
def gen_perlin_noise(self, \
             size_image = 100, \
             size_turbulance = 300, \
             nb_octaves = 7, \
             persistance = 0.5, \
             show_perlin_noise = 1):

    # init
    mat0 = random.rand(size_turb,size_turb)
    x0 = arange(size_turb)
    y0 = arange(size_turb)
    octaves=[]

    # interpolation de la matrice générée aléatoirement
    f = interp2d(x0, y0, mat0)
    # calcul de 2 à 2^nboctave
    for j in arange(nboctaves) :
        octave=2**j
        # nouvelle base d'interpolation
        x1=arange(0,size_turbulance,octave)
        y1=arange(0,size_turbulance,octave)
        #interpolation
        temp_oct=f(x1,y1)
        # liste des bruits aux différentes octaves
        octaves.append(temp_oct)

    # matrice contenant le bruit de perlin
    perlin_noise = empty((size_turb,size_turb))

    for octave in octaves :
        # mise a echelle des différentes octaves
        mat=misc.imresize(octave,(size_turb,size_turb))
        # persistance de l'octace
        per=per/persistence
        # somme des bruits
        perlin_noise = perlin_noise + octave*per

    # normalisation
    perlin_noise = perlin_noise/amax(perlin_noise)

    # plot
    if show_perlin_noise :
        plt.figure(1)
        plt.imshow(perlin_cut,cmap='autumn')
        plt.show()
        plt.pause(0.001)

    # redimensionnement au format de l'image
    perlin_noise = misc.imresize(perlin_noise,(size_image,size_image))
    perlin_noise = perlin_noise/amax(perlin_noise)

    return perlin_noise


################################################################################
def woodtexturegeneration(size_image = 1000, \
                          size_turb_x1 = 1000, \
                          lambda_x1 = 3, \
                          size_turb_x2 = 300, \
                          lambda_x2 = 40, \
                          x2_power = 160, \
                          plot_show = 0) :
    # init
    size_image = 1000
    plot_show = 0

    # turbulance en x
    size_turb_x1 = 1000
    lambda_x1 = 3
    x1_power = 25
    turb_x1 = generate(size_image, size_turb_x1)

    # turbulance en y
    size_turb_x2 = 300
    lambda_x2 = 40
    x2_power = 160
    turb_x2 = generate(size_image, size_turb_x2)

    # base de taille size_image, centrée en zero
    x0 = arange(-floor(size/2),floor(size/2),1)
    y0 = arange(-floor(size/2),floor(size/2),1)
    X,Y=meshgrid(x0,y0)

    # application des turbulances à sin(x) à 2fréquences différentes
    wood_texture = sin((X + turb_x1 * x1_power)/lambda_x1) +  \
             0.1 * sin((X + turb_x2 * x2_power)/lambda_x2)

    # plot
    if plot_show == 1 :
        plt.figure()
        Colmap = CreateColorMap()
        plt.imshow(mat0,cmap=Colmap.brown)


##################################################################################
class ArbreClass() :
    def __init__(self, Axes, Strate) :

        # Strate = nbpt, rayon, couleur, contour, courbure
        self.nbpt = Strate.nbpt #[10,8,8,8,8,8]
        self.rayon = Strate.rayon #[2,1.5,0.9,0.5,0.3,0.1]
        self.courbure = Strate.courbure #0.5
        self.couleur = Strate.couleur #[205,200,195,190,185,180]
        self.contour = Strate.contour #(0,150/255,0)
        self.size = 10
        self.pos_x = 0
        self.pos_y = 0
        self.Axes = Axes
        self.strates = list()
##    def create_arbre(self) :

##        for i in arange(nb_strates) :
        nbpt = self.nbpt
        rayon = self.rayon
        couleur = self.couleur
        contour = self.contour
        courbure = self.courbure
        self.strates = self.FeuillageClass(nbpt, rayon, couleur, contour, courbure, self)

    def modify_arbre(self, strate, nbpt, rayon, couleur, contour, courbure) :
        self.strates = self.FeuillageClass(nbpt, rayon, couleur, contour, courbure, self)

    def plot_arbre(self) :
        self.strates.plot_feuillage(self.Axes)

    class FeuillageClass() :
        def __init__(self, nbpt, rayon, couleur, contour, courbure, Outclass) :
            self.nbpt = nbpt
            self.couleur = (0, couleur/256, 0)
            self.contour = (0, contour/256, 0)
            self.rayon = rayon
            self.pos_x = Outclass.pos_x
            self.pos_y = Outclass.pos_y
            self.size = Outclass.size
            self.courbure = courbure
            self.Calculate()


        def plot_feuillage(self, Axes) :
            ax = Axes

            new_verts=(self.verts)*self.size + [self.pos_x, self.pos_y]
            path = Path(new_verts, self.codes)

            ax.plot(new_verts[:,0], new_verts[:,1],color=self.contour,linewidth = 5)
            patch = patches.PathPatch(path, facecolor=self.couleur, edgecolor='none')
            ax.add_patch(patch)

        def Calculate(self) :
         # stocke les points définissants le polygone
            verts=empty((0,2))
            C = empty((0,2))

            # calcul des points aléatoires répartis sur un cercle de rayon Ray
            # génération des angles
            nbpt = self.nbpt
            phi = linspace(0,1,nbpt)*2*pi
            phi=phi+random.rand(phi.shape[0])*pi/6-pi/12
            phi=hstack((phi,phi[0]))
            Ray = self.rayon

            # calcul de 4 points définissants la courbe de Bezier a partir de 2 point du cercle
            for i in arange(phi.shape[0]-1) :
                B=empty((4,2))
                # deux point du cercles
                B[0,:] = [Ray * cos(phi[i]), Ray*sin(phi[i])]
                B[3,:] = [Ray * cos(phi[i+1]), Ray*sin(phi[i+1])]

                # calculs des deux points définnissants la courbure de l'arc
                coef = B[3,:]-B[0,:]
                B[1,:] = B[0,:]+[coef[1]*0.5,-coef[0]*self.courbure] # perpendiculaire a B0B3
                B[2,:] = B[3,:]+[coef[1]*0.5,-coef[0]*self.courbure]
                C = vstack((C,B[:3:,:]))

                # calcul de la courbe de bezier et enregistrement des points
                points = courbe_bezier_3([B[0,:], B[1,:], B[2,:], B[3,:]],50)
                for temp in points :
                    verts = vstack((verts,temp))

            # on boucle la boucle
            verts = vstack((verts,verts[0,:]))

            # création du polygone

            codes = ones(verts.shape[0], int) * Path.LINETO
            codes[0] = Path.MOVETO
            codes[verts.shape[0]-1] = Path.CLOSEPOLY

            self.codes = codes
            self.verts = verts


######################################################################################
def combinaison_lineaire(A,B,u,v):
    return [A[0]*u+B[0]*v,A[1]*u+B[1]*v]
def interpolation_lineaire(A,B,t):
    return combinaison_lineaire(A,B,t,1-t)
def point_bezier_3(points_control,t):
    x=(1-t)**2
    y=t*t
    A = combinaison_lineaire(points_control[0],points_control[1],(1-t)*x,3*t*x)
    B = combinaison_lineaire(points_control[2],points_control[3],3*y*(1-t),y*t)
    return [A[0]+B[0],A[1]+B[1]]
def courbe_bezier_3(points_control,N):
    if len(points_control) != 4:
        raise SystemExit("4 points de controle")
    dt = 1.0/N
    t = dt
    points_courbe = [points_control[0]]
    while t < 1.0:
        points_courbe.append(point_bezier_3(points_control,t))
        t += dt
    points_courbe.append(points_control[3])
    return points_courbe
def plot_points(points_courbe,style='-'):
    x = []
    y = []
    for p in points_courbe:
        x.append(p[0])
        y.append(p[1])
    plot(x,y,style)


