#%matplotlib inline
from scipy import linalg as la
from scipy import optimize
import matplotlib as mpl
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.axes3d import Axes3D
import numpy as np
import sympy
from matplotlib import cm
sympy.init_printing()

#节点
class point(object):
    def __init__(self,array):
        self.x=array[0]
        self.y=array[1]
        self.number=int(array[2])

points=np.genfromtxt('arc\point.txt',delimiter=',')

prepare_point = locals()
for i in points:
    point_='point'+str(int(i[2]))
    prepare_point[point_]=point(i)

#约束
class yueshu(object):
    def __init__(self,array):
        self.point=int(array[0])
        self.x=int(array[1])
        self.y=int(array[2])
        self.number=int(array[3])
yueshus=np.genfromtxt('arc\yueshu.txt',delimiter=',')

#荷载
class load(object):
    def __init__(self,array):
        self.point=int(array[0])
        self.x=int(array[1])
        self.y=int(array[2])
loads=np.genfromtxt('arc\load.txt',delimiter=',')
        
#杆
class pole(object):
    def __init__(self,array):
        self.point1=int(array[0])
        self.point2=int(array[1])
        self.x=(eval('point'+str(self.point1)).x,eval('point'+str(self.point2)).x)
        self.y=(eval('point'+str(self.point1)).y,eval('point'+str(self.point2)).y)
        self.xlength=self.x[1]-self.x[0]
        self.ylength=self.y[1]-self.y[0]
        self.length=np.sqrt(self.xlength**2+self.ylength**2)
        self.sin=self.ylength/self.length
        self.cos=self.xlength/self.length
        self.number=int(array[2])
poles=np.genfromtxt('arc\pole.txt',delimiter=',')

#求解
n=len(poles)+len(yueshus)
Kmat=np.zeros((n,n))
loa=np.zeros((n,1))
if 2*len(points)<n:
    print('欠定')
if 2*len(points)>n:
    print('超正定')
if 2*len(points)==n:
    for i in poles:
        pole_=pole(i)
        Kmat[pole_.point1][pole_.number]=pole_.cos
        Kmat[-1-pole_.point1][pole_.number]=pole_.sin
        Kmat[pole_.point2][pole_.number]=-pole_.cos
        Kmat[-1-pole_.point2][pole_.number]=-pole_.sin
    for i in yueshus:
        yueshu_=yueshu(i)
        Kmat[yueshu_.point][-1-yueshu_.number]=yueshu_.x
        Kmat[-1-yueshu_.point][-1-yueshu_.number]=yueshu_.y
    for i in loads:
        load_=load(i)
        loa[load_.point]=load_.x
        loa[-1-load_.point]=load_.y
    x=la.solve(Kmat,loa)
    print('上至下为对应编号杆受力，正为压力，负为拉力;下往上为对应编号约束力')
    print(x)
    
#可视化
fig,ax=plt.subplots()
for i in poles:
    po=pole(i)
    F=x[po.number]
    if F<0:
        my_color=cm.Oranges(-0.1*F)
        ax.plot(po.x,po.y,color=my_color)
    if F>0:
        my_color=cm.GnBu(0.1*F)
        ax.plot(po.x,po.y,color=my_color)
    if F==0:
        my_color='g'
        ax.plot(po.x,po.y,color=my_color)
ax.plot(0,0,color=cm.Oranges(0.5),label="pull")
ax.plot(0,0,color=cm.GnBu(0.5),label="pressure")
ax.plot(0,0,color='g',label="zero")
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.legend()
plt.show()

