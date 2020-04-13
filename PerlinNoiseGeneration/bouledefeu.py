from numpy import *
from numpy import matlib

from matplotlib import pyplot as plt
from PIL import Image
from scipy import misc
from scipy.interpolate import interp2d
plt.ion()

##if __name__ == "__main__":
##
##    main()


####mat=empty([100,100])
##periode = 2**arange(1,9,1)
##freq=1/periode
##
##for i in x
##    xlim0 = i//periode * periode
##    xlim1 = xlim0 + periode
##    for j in y
##        ylim0 = j//periode * periode
##        ylim1 = ylim0 + periode
##
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

