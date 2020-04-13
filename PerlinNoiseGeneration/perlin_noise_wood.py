from numpy import *
from numpy import matlib

from matplotlib import pyplot as plt
from PIL import Image
from scipy import misc
from scipy.interpolate import interp2d
plt.ion()



size=1000
size_turbx=1000
size_turby=300
lambdax = 3
lambday = 40
xpower = 25
ypower = 160
nb_smooth = 7
persistence = 0.5
a=0
b=0
l=0
plt.figure()

while l<2 :
    if b == 0 :
        size_turb=size_turbx
        b=1
    else :
        size_turb=size_turby

    mat0=random.rand(size_turb,size_turb)
##    mat0[250:350:,250:350:]=random.rand(100,100)/2+0.5
    x0=arange(size_turb)
    y0=arange(size_turb)
    grids=[]

    pts=vstack((x0,y0))
    for j in arange(1,nb_smooth,1) :
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
        per=per/persistence
        perlin_mat = perlin_mat + mat*per

    perlin_mat=perlin_mat/amax(perlin_mat)
    perlin_cut=perlin_mat.copy()
##    perlin_cut[0,0]=1.6
    plt.imshow(perlin_cut,cmap='autumn')
    plt.show()
    plt.pause(0.001)
    l=l+1

    perlin_cut=misc.imresize(perlin_cut,(size,size))
    perlin_cut=perlin_cut/amax(perlin_cut)
    if a == 0 :
        turb_x0=perlin_cut
        a=1
    else :
        turb_y0=perlin_cut
##misc.imread
##misc.imsave
##interp1


##    mat0[250:350:,250:350:]=random.rand(100,100)
x0=arange(-floor(size/2),floor(size/2),1)
y0=arange(-floor(size/2),floor(size/2),1)
X,Y=meshgrid(x0,y0)
##mat0=sin(sqrt(((X+turb_x0*xpower)**2)/lambdax+((Y+turb_y0*ypower)**2)/lambday))
mat0=sin((X+turb_x0*xpower)/lambdax)+0.1*sin((X+turb_y0*ypower)/lambday)
plt.imshow(mat0,cmap='gray')
plt.figure()


import math
from matplotlib.pyplot import *
from numpy import *



c0=empty((50,1))
c1=empty((50,1))
c2=empty((50,1))
brown=[165,42,42]
c0[:,0]=linspace(0,165,50)
c1[:,0]=linspace(0,42,50)
c2[:,0]=linspace(0,42,50)
b_cmap = hstack((c0,c1,c2))

mat_temp=random.rand(100,100)

from matplotlib import cm
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

cdict1 = {'red':   ((0.0, 0/255, 0/255),
                    (1.0, 190/255, 190/255)),

         'green': ((0.0, 0/255, 0/255),
                   (1.0, 62/255, 62/255)),

         'blue':  ((0.0, 0/255, 0/255),
                   (1.0, 62/255, 62/255))
         }

blue_red1 = LinearSegmentedColormap('BlueRed1', cdict1)
plt.imshow(mat0,interpolation='nearest',  cmap=blue_red1, aspect='auto')
plt.colorbar()
plt.show()

fig = figure(5)
ax = fig.add_subplot(111)
mat2=mat0[:,200:600]
ax.imshow(mat2,cmap=blue_red1)
##plt.show()



ion()
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



def R(phi) :
    Rot = array([[cos(phi), -sin(phi)],[sin(phi),cos(phi)]])
    return Rot



nbpt_=[10,8,8,8]
Ray_ = [2,1.5,0.9,0.5]
couleur_ = [205,200,195,190]
##fig = figure()
##ax = fig.add_subplot(111)
for k in arange(1) :
    plt.pause(2)
    C = empty((0,2))
    nbpt = nbpt_[k]
    phi = linspace(0,1,nbpt)*2*pi
    phi=phi+random.rand(phi.shape[0])*pi/6-pi/12
    phi=hstack((phi,phi[0]))
    ##
    Ray = Ray_[k]
    figure(2)
    for i in arange(phi.shape[0]-1) :
        B=empty((4,2))
        B[0,:] = [Ray * cos(phi[i]), Ray*sin(phi[i])]
        B[3,:] = [Ray * cos(phi[i+1]), Ray*sin(phi[i+1])]

        coef = B[3,:]-B[0,:]
        B[1,:] = B[0,:]+[coef[1]*0.5,-coef[0]*0.5]
        B[2,:] = B[3,:]+[coef[1]*0.5,-coef[0]*0.5]
        C = vstack((C,B[:3:,:]))

    ##    plot(B[:,0],B[:,1])
        plot(B[0,0],B[0,1],'o')
        plot(B[3,0],B[3,1],'o')
    show()
    i=0
    ##phi = 0
    figure(figsize=(8,8))
    verts=empty((0,2))
    while i+3 < C.shape[0] :
    ##    C=B
    ##    C=dot(B,R(phi))
        P0 = C[i,:] + random.rand(2)*0.1
        if i+1 > C.shape[0] :
            break
        P1 = C[i+1,:]+ random.rand(2)*0.1
        if i+2 > C.shape[0] :
            break
        P2 = C[i+2,:]+ random.rand(2)*0.1
        if i+3 > C.shape[0] :
            break
        P3 = C[i+3,:]+ random.rand(2)*0.1
        i=i+3


        print('ahaha')
        a=0
        if a==1 :
            points = courbe_bezier_3([P0,P1,P2,P3],50)
            for temp in points :
                verts = vstack((verts,temp))
            a=0

        elif a==0 :
            points = courbe_bezier_3([P0,P1,P2,P3],50)
            for temp in points :
                verts = vstack((verts,temp))
            a=1


        plot_points(points,style='r-')
        print('ahaha')
        points = courbe_bezier_3([P0,P1,P2,P3],50)
        plot_points(points,style='r-')#
    grid()

    verts = vstack((verts,verts[0,:]))
    from matplotlib.path import Path
    import matplotlib.patches as patches


    verts=(verts)*300+[200,-200]
    codes = ones(verts.shape[0], int) * Path.LINETO
    codes[0] = Path.MOVETO
    codes[verts.shape[0]-1] = Path.CLOSEPOLY

    path = Path(verts, codes)
    couleur = (0,couleur_[k]/255,0)
    patch = patches.PathPatch(path, facecolor=couleur, edgecolor='none')
    ax.add_patch(patch)

    couleur = (0,150/255,0)
    plt.pause(2)
    ax.plot(verts[:,0],verts[:,1],color=couleur,linewidth = 5)
show()



