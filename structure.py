import matplotlib.pyplot as plt
import matplotlib as mpl
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d import proj3d
import numpy as np

fig = plt.figure(figsize=(10,10))
axe = Axes3D(fig)
GLOBAL_NAME = 0

class NodeManager:
    '''
    To manage id and coordinate of nodes
    
    methods:
        self.get(coordinate): get a nodeId by coordinate
        self.anti_get(nodeId): get coordinate by nodeId
        self.get_all(): get all nodeId, coordinate
    '''
    def __init__(self):
        self.dict = {}
        self.anti_dict = {}
        self.i = 0

    def __repr__(self):
        return '{}'.format(self.dict)
    
    def __getitem__(self, nodeId):
        return self.anti_dict[nodeId]
    
    def __type_checking(self, coordinate):
        if not isinstance(coordinate, tuple):
            coordinate = tuple(coordinate)
        return coordinate
    
    def __iter__(self):
        nodes = self.get_all()
        for node in nodes:
            yield node
            
    def __len__(self):
        return self.i
        
    def get(self, coordinate):
        '''
        get nodeId by coordinate
        
        Examples
        --------
        >>> node_manager.get((4,3,1))
        0
        '''
        coordinate = self.__type_checking(coordinate)
        return self.dict[coordinate]
        
    def anti_get(self, node_id):
        return self.anti_dict[node_id]
    
    def add(self, coordinate):
        coordinate = self.__type_checking(coordinate)
        if coordinate in self.dict:
            return True
        
        self.dict[coordinate] = self.i
        self.anti_dict[self.i] = coordinate
        self.i += 1
    
    def exist(self, coordinate):
        coordinate = self.__type_checking(coordinate)
        if coordinate in self.dict:
            return True
        else:
            return False
    
    def delete(self, coordinate):
        if self.exist(coordinate):
            key = self.get(coordinate)
            self.dict.pop(coordinate)
            self.anti_dict.pop(key)
    
    def get_all(self):
        output = []
        for key in self.dict:
            output.append([self.get(key), *key])
        return output
    

    
node_manager = NodeManager() 

    
    
    
class Column:
    def __init__(self, axe, point1, point2, color = 'blue', type_='column'):
        global GLOBAL_NAME
        self.X = np.array([point1[0], point2[0]])
        self.Y = np.array([point1[1], point2[1]])
        self.Z = np.array([point1[2], point2[2]])
        self.axe = axe
        self.height = self.Z[1] - self.Z[0]
        self.point1 = point1
        self.point2 = point2
        self.__type = type_
        
        self.axe.plot(self.X, self.Y, self.Z, color = color)
        
        node_manager.add(point1)
        node_manager.add(point2)
        self.name = GLOBAL_NAME
        GLOBAL_NAME += 1
        
    def __getitem__(self, pos):
        if pos == 0:
            return self.point1
        elif pos == 1:
            return self.point2
    
    def __repr__(self):
        presentation = 'a {0} between point{1} and point{2} with id {3}'.format(self.__type,
                                                  self.point1, self.point2, self.name)
        return presentation.format(self.__type)
    
    def copy_translate(self, shift = (0, 0, 3)):
        delta_x, delta_y, delta_z = shift
        
        X_new = self.X + delta_x
        Y_new = self.Y + delta_y
        Z_new = self.Z + delta_z
        
        point1 = [X_new[0], Y_new[0], Z_new[0]]
        point2 = [X_new[1], Y_new[1], Z_new[1]]
        
        return Column(self.axe, point1, point2)
        
    def plot(self , axe):
        axe.plot(self , self.point1, self.point2 , "blue")
        

    
    
class Beam(Column):
    def __init__(self, axe, point1, point2):
        super().__init__(axe, point1, point2, type_ = 'beam')   
        self.height = point1[2]
        

class Structure:
    def __init__(self, axe):
        self.columns = []
        self.beams_L = []
        self.beams_B = []
        self.axe = axe
    
    def plot_range(self, x_range , y_range , z_range):
        self.x_range = x_range
        self.y_range = y_range
        self.z_range = z_range
        
    def plot(self , scale_x = 0.5 , scale_y = 0.5 , scale_z = 1 ):
        def short_proj():  
          return np.dot(Axes3D.get_proj(self.axe), scale)
    
        self.axe.set_xlim(self.x_range[0], self.x_range[1])
        self.axe.set_ylim(self.y_range[0], self.y_range[1])
        self.axe.set_zlim(self.z_range[0], self.z_range[1])  
        
        scale = np.diag([scale_x, scale_y, scale_z, 1.0])

        self.axe.get_proj = short_proj
  
        plt.show(self.axe)



        
class Support(Structure):
    def __init__(self, axe):
        super().__init__(axe)
        self.level = 0
        self.H = 0
        self.template = []
        self.members = []
        
    def set_H(self, h):
        self.H = h
        
    def to_members(self):
        output = []
        for member in self.members:
            name = member.name
            pointId1 = node_manager.get(member.point1)
            pointId2 = node_manager.get(member.point2)
            output.append([name, pointId1, pointId2])
        return output

class SymmetricSupport(Support):
    def add_templates(self, members):
        self.template.extend(members)
        
    def add_template(self, member):
        self.template.append(member)
        
    def add_storey(self, h):
        for member in self.template:
            self.members.append(member.copy_translate((0, 0, self.H)))
        self.H += h
    

class Frame(Structure):
    def __init__(self, axe):
        super().__init__(axe)
        self.columns = []
        self.beams_L = []
        self.beams_B = []
        self.H = 0
        self.level = 0
        
    def add_storey_with_shift(self, l, b, h, span_L, span_B, shift=(0,0)):
        x, y = shift
        H_next = self.H + h
        columns = [[Column(axe, (i*l+x, j*b+y, self.H), (i*l+x, j*b+y, H_next)) 
                        for i in range(span_L+1)] 
                        for j in range(span_B+1)]
        self.H = H_next
        beams_L = [[Beam(axe, (i*l+x, j*b+y, self.H), ((i+1)*l+x, j*b+y, self.H)) 
                        for i in range(span_L)] 
                        for j in range(span_B+1)]
        beams_B = [[Beam(axe, (i*l+x, j*b+y, self.H), ((i)*l+x, (j+1)*b+y, self.H)) 
                        for i in range(span_L+1)] 
                        for j in range(span_B)]
        
        self.columns.append(columns)
        self.beams_L.append(beams_L)
        self.beams_B.append(beams_B)
        
        self.level += 1

    
    def add_storey(self, l, b, h, span_L, span_B, shift=(0,0)):
        self.add_storey_with_shift(l, b, h, span_L, span_B)


    def set_H(self, h):
        self.H = h


    def __to_elementArgs(self, l):
        output = []
        for i in range(len(l)):
            for j in range(len(l[i])):
                for k in range(len(l[i][j])):
                    member = l[i][j][k]   
                    memberName = member.name
                    pointId1 = node_manager.get(member.point1)
                    pointId2 = node_manager.get(member.point2)
                    output.append([memberName, pointId1, pointId2])
        return output

    def __to_elementArgsNth(self, l, n):
        output = []
        for j in range(len(l[n])):
            for k in range(len(l[n][j])):
                member = l[n][j][k]   
                memberName = member.name
                pointId1 = node_manager.get(member.point1)
                pointId2 = node_manager.get(member.point2)
                output.append([memberName, pointId1, pointId2])
        return output      
    
    def to_columns_nth(self, n):
        return  self.__to_elementArgsNth(self.columns, n)

    def to_beamL_nth(self, n):
        return  self.__to_elementArgsNth(self.beams_L, n)
    
    def to_beamB_nth(self, n):
        return self.__to_elementArgsNth(self.beams_B, n)
    
    def to_columns(self):
        element_columns = self.__to_elementArgs(self.columns)
        return element_columns  
    
    def to_beamL(self):
        element_beams_L = self.__to_elementArgs(self.beams_L)
        return element_beams_L  
        
    def to_beamB(self):
        element_beams_B = self.__to_elementArgs(self.beams_B)
        return element_beams_B  




class SymmeticFrame(Frame):
    def __init__(self, axe, l, b, h, span_L, span_B, level_H):
        super().__init__(axe)
        self.l, self.b, self.h = l, b, h
        self.span_L, self.span_B, self.level_H = span_L, span_B, level_H
        
        for i in range(level_H):
            self.add_storey(l, b, h, span_L, span_B)
    
    
    
    
if __name__ == '__main__':
        
    l, b, h = 6, 8, 3.3
    span_L, span_B, level_H = 6, 3, 14
    
    frame = Frame(axe)
    frame.add_storey(l, b, h, 6, 3)
    for i in range(5):
        frame.add_storey(l, b, 5, 6, 3)
    for i in range(5):
        frame.add_storey_with_shift(l, b, 3, 3, 1, (12, 8))
    frame.plot_range((0,50) , (0,50) , (0,60))
    

    frame2 = Frame(axe)
    frame2.set_H(28.3)
    frame2.add_storey_with_shift(3, 3, 3, 1, 1, (30, 20))
    frame.plot()
    

    
    
    
    fig2 = plt.figure(figsize=(10,10))
    axe2 = Axes3D(fig2)
    
    skewColumn1 = Column(axe2, point1=(0,0,0), point2=(6,0,3.3))
    skewColumn2 = Column(axe2, point1=(12,0,0), point2=(6,0,3.3))  
    
    support = SymmetricSupport(axe2)
    support.add_templates([skewColumn1, skewColumn2])
    support.set_H(5)
    support.add_storey(3.3)
    support.add_storey(3.3)
    support.add_storey(3.3)
    support.add_storey(3.3)
    
    support.plot_range((0, 20), (0, 20), (0, 20))
    support.plot()
    
    









            
            
    