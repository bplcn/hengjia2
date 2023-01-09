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

# ! 思考问题：对于大规模计算，定义类的数组还是数组的类更为合适？
#节点
class point(object):
    def __init__(self,array):
        self.x=array[0]
        self.y=array[1]
        self.number=int(array[2])
# ! 节点、杆单元信息处理为字典更合适
points=np.genfromtxt('point.txt',delimiter=',')

# prepare_point = locals()
# for i in points:
#     point_='point'+str(int(i[2]))
#     prepare_point[point_]=point(i)

# ! 荷载和约束部分无编号之必要
#约束
class yueshu(object):
    def __init__(self,array):
        self.point=int(array[0])
        self.x=int(array[1])
        self.y=int(array[2])
        self.number=int(array[3])
yueshus=np.genfromtxt('yueshu.txt',delimiter=',')

#荷载
class load(object):
    def __init__(self,array):
        self.point=int(array[0])
        self.x=int(array[1])
        self.y=int(array[2])
loads=np.genfromtxt('load.txt',delimiter=',')
        
#杆
# ! 类不必太过复杂
class pole(object):
    def __init__(self,array,coord1,coord2):
        self.point1=int(array[0])
        self.point2=int(array[1])
        # ! 元编程并不必要
        # self.x=(eval('point'+str(self.point1)).x,eval('point'+str(self.point2)).x)
        # self.y=(eval('point'+str(self.point1)).y,eval('point'+str(self.point2)).y)
        self.x = np.array([coord1[0],coord2[0]])
        self.y = np.array([coord1[1],coord2[1]])
        self.xlength=self.x[1]-self.x[0]
        self.ylength=self.y[1]-self.y[0]
        self.length=np.sqrt(self.xlength**2+self.ylength**2)
        self.sin=self.ylength/self.length
        self.cos=self.xlength/self.length
        self.number=int(array[2])
poles=np.genfromtxt('pole.txt',delimiter=',')

#求解
n=len(poles)+len(yueshus)
Kmat=np.zeros((n,n))
loa=np.zeros((n,1))

pole_Vec = []
for elem in poles:
    elemid = int(elem[2])
    nodeid1 = int(elem[0])
    nodeid2 = int(elem[1])
    coord1 = [points[nodeid1][0],points[nodeid1][1]]
    coord2 = [points[nodeid2][0],points[nodeid2][1]]

    pole_=pole(elem,coord1,coord2)
    # ! 注意保存计算结果
    pole_Vec.append(pole_)        

if 2*len(points)<n:
    print('欠定')
elif 2*len(points)>n:
    print('超正定')
elif 2*len(points)==n:
    for pole_ in pole_Vec:
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

# ! for-if loop 速度较慢
#可视化
fig,ax=plt.subplots()
colors = cm.jet(x)
for pole_ in pole_Vec:
    # po=pole(i)
    F=x[pole_.number]
    ax.plot(pole_.x,pole_.y,color=colors[pole_.number])
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.legend()
plt.show()
"""       
#可视化
fig,ax=plt.subplots()
for po in pole_Vec:

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
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.legend()
plt.show()
"""


# ! 尝试利用taichi加速https://zhuanlan.zhihu.com/p/547123604
# ! 尝试利用numba加速 https://zhuanlan.zhihu.com/p/78882641