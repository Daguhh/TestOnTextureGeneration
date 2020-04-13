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



