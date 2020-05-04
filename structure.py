# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import matplotlib.pyplot as plt
import matplotlib as mpl
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d import proj3d
import numpy as np



class Column:
    def __init__(self, axe, point1, point2, color = 'blue'):
        self.X = np.array([point1[0], point2[0]])
        self.Y = np.array([point1[1], point2[1]])
        self.Z = np.array([point1[2], point2[2]])
        self.axe = axe
        self.height = self.Z[1] - self.Z[0]
        self.point1 = point1
        self.point2 = point2
        
        self.axe.plot(self.X, self.Y, self.Z, color = color)

    def copy_translate(self, shift = (0, 0, 3)):
        delta_x, delta_y, delta_z = shift
        
        X_new = self.X + delta_x
        Y_new = self.Y + delta_y
        Z_new = self.Z + delta_z
        
        point1 = [X_new[0], Y_new[0], Z_new[0]]
        point2 = [X_new[1], Y_new[1], Z_new[1]]
        
        return Column(self.axe, point1, point2)
        

    
    
class Beam(Column):
    def __init__(self, axe, point1, point2):
        super().__init__(axe, point1, point2)   
        self.height = point1[2]
        

class Structure:
    def __init__(self, axe):
        self.columns = []
        self.beams_L = []
        self.beams_B = []
        self.axe = axe
        
    def plot(self):
        plt.show(self.axe)
        
    def get_all_points(self):
        points = []
        for i in range(len(self.columns)):
            for j in range(len(self.columns[i])):
                for k in range(len(self.columns[i][j])):
                    column = self.columns[i][j][k]
                    points.append(column.point1)
                    if k == len(self.columns[i][j]) - 1:
                        points.append(column.point2)
                    
        return points
    
        
class Frame(Structure):
    def __init__(self, axe, l, b, h, L, B, H):
        super().__init__(axe)
        self.l, self.b, self.h = l, b, h
        self.L, self.B, self.H = L, B, H
        
        self.columns = [[[Column(axe, (i*l, j*b, k*h), (i*l, j*b, (k+1)*h)) 
                        for i in range(L)] 
                        for j in range(B)]
                        for k in range(H)]
        self.beams_L = [[[Beam(axe, (i*l, j*b, k*h), ((i+1)*l, j*b, k*h)) 
                        for i in range(L-1)] 
                        for j in range(B)]
                        for k in range(H+1)]
        self.beams_B = [[[Beam(axe, (i*l, j*b, k*h), ((i)*l, (j+1)*b, k*h)) 
                        for i in range(L)] 
                        for j in range(B-1)]
                        for k in range(H+1)]
        
    

    
if __name__ == '__main__':
    fig = plt.figure()
    axe = Axes3D(fig)
    
    
    l, b, h = 3, 3, 3
    L, B, H = 6, 3, 10
    
    frame = Frame(axe, l, b, h, L, B, H)
    frame.plot()

    points = frame.get_all_points()











            
            
    