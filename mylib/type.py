import numpy as np
import math

class Point: # 节点
    id = 0
    # coordinate
    x = 0
    y = 0
    # load
    px = 0
    py = 0
    # axial displacement
    u = 0
    # deflection
    w = 0
    # rotation
    theta = 0

    def __init__(self, data:list[float]):
        (self.id, self.x, self.y) = data

    def __str__(self):
        return f"Node {self.id}: ({self.x}, {self.y})"
    
    def __repr__(self):
        return self.__str__()

class Material: # 材料
    id = 0
    E = 0

    def __init__(self, data: list[float]) -> None:
        (self.id, self.E) = data

    def __str__(self) -> str:
        return f"<id:{self.id}, E:{self.E}>"

    def __repr__(self) -> str:
        return self.__str__()

class Plane: # 截面
    id = 0
    # area
    A = 0
    # moment of inertia
    I = 0

    def __init__(self,  data: list[float]) -> None:
        (self.id, self.A, self.I) = data

    def __str__(self) -> str:
        return f"<id:{self.id}, A:{self.A}, I:{self.I}>"

    def __repr__(self) -> str:
        return self.__str__()

class Unit: # 单元
    #region parameters
    id = 0
    # node id
    i = 0
    j = 0
    # material
    material: Material = None
    # plane
    plane: Plane = None
    # length
    L = 0
    # angle
    theta = 0
    # axial stiffness
    EA = 0
    # flexural stiffness
    EI = 0
    # shear stiffness
    GA = 0
    # element stiffness matrix
    k = np.zeros((6, 6))
    # element transformation matrix
    T = np.zeros((6, 6))
    # endregion

    def __init__(self, data:list[float]):
        (self.id, self.i, self.j, self.material, self.plane) = data
        # calculate length
        dx = self.j.x - self.i.x
        dy = self.j.y - self.i.y
        self.L = np.hypot(dx, dy)
        # calculate angle
        dx = self.j.x - self.i.x
        dy = self.j.y - self.i.y
        self.theta = np.arctan2(dy, dx)
        # calculate axial stiffness
        self.EA = self.material.E * self.plane.A
        # calculate flexural stiffness
        self.EI = self.material.E * self.plane.I
        # calculate shear stiffness
        self.GA = self.material.E * self.plane.A / 3
        
    def __str__(self):
        return f"Element {self.id}: ({self.i}, {self.j})"

    def __repr__(self):
        return self.__str__()
    
    def calculateKe_without_shear(self) -> np.ndarray:
        # calculate element stiffness matrix
        c = np.cos(self.theta)
        s = np.sin(self.theta)
        # without shear deformation
        Ke = np.array([[self.EA/self.L, 0, 0, -self.EA/self.L, 0, 0],
                      [0, 12*self.EI/self.L**3, 6*self.EI/self.L**2, 0, -12*self.EI/self.L**3, 6*self.EI/self.L**2],
                      [0, 6*self.EI/self.L**2, 4*self.EI/self.L, 0, -6*self.EI/self.L**2, 2*self.EI/self.L],
                      [-self.EA/self.L, 0, 0, self.EA/self.L, 0, 0],
                      [0, -12*self.EI/self.L**3, -6*self.EI/self.L**2, 0, 12*self.EI/self.L**3, -6*self.EI/self.L**2],
                      [0, 6*self.EI/self.L**2, 2*self.EI/self.L, 0, -6*self.EI/self.L**2, 4*self.EI/self.L]])
        return Ke
    
    def calculateKe_with_shear(self) -> np.ndarray:
        # calculate element stiffness matrix
        c = np.cos(self.theta)
        s = np.sin(self.theta)
        # with shear deformation
        

class Payload: # 荷载
    point: Point = None
    px = 0
    py = 0

    def __init__(self, data: list) -> None:
        (self.point, self.px, self.py) = data

    def __str__(self) -> str:
        return f"<point:{self.point.id}, px:{self.px}, py:{self.py}>"

    def __repr__(self) -> str:
        return self.__str__()

class Constraint: # 约束
    point: Point = None
    axis = 1 # 1: x, 2: y, 3: theta
    value = 0

    def __init__(self, data: list) -> None:
        (self.point, self.axis, self.value) = data

    def __str__(self) -> str:
        return f"<point:{self.point.id}, axis:{self.axis}, value:{self.value}>"

    def __repr__(self) -> str:
        return self.__str__()