from structure import node_manager, Frame, SymmeticFrame, Column, Beam
from structure import axe, fig
#import opensees as ops

if __name__ == '__main__':
    

    frame = SymmeticFrame(axe, 3, 3, 3, 6, 3, 10)
    frame.plot_range((0,20) , (0,20) , (0,60))
    frame.plot()
    
    for node in node_manager:
        print(node)
        
    frame.to_beamB()