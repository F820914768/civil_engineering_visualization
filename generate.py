# -*- coding: utf-8 -*-

import structure as stu
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d import proj3d
import matplotlib.pyplot as plt
import matplotlib as mpl


ls = [6,6,6,6,6]
bs = [6,3,6]
hs = [3,3,3,3,3,3,3]




if __name__ == '__main__':
    frame = stu.Frame(stu.axe)   
    support = stu.SymmetricSupport(stu.axe)     
    for h in hs:
        frame.add_storey_from_list(ls, bs, h)
        
    
    
    skewCol1 = stu.Column(stu.axe, (0, 0, 0), (0, 6, 3))
    skewCol2 = stu.Column(stu.axe, (0, 9, 3), (0, 15, 0))
    skewCol3 = skewCol1.copy_translate((sum(ls), 0, 0))
    skewCol4 = skewCol2.copy_translate((sum(ls), 0, 0))

    support.add_templates([skewCol1, skewCol2, skewCol3, skewCol4])
    for h in hs:
        support.add_storey(3)
     
    support.plot_range((0,40), (0, 40), (0, 40))
    support.plot()
    
    


