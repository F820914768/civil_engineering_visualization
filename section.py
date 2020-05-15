import matplotlib.pyplot as plt 
import matplotlib.patches as patches

class Section:
    def __init__(self, H, B):
        self.H = H
        self.B = B

    def plot(self):
        
        
        self.ax = plt.subplot(111)



class HSection(Section):
    def __init__(self, Bu, Bl, H, tu, tl, tm):
        super().__init__(H, max(Bu, Bl))
        self.top_flange_width = Bu
        self.low_flange_width = Bl
        self.top_flange_thickness = tu
        self.low_flange_thickness = tl
        self.height = H
        self.web_thickness = tm
        self.low_flange_main_point_1 = [-Bl/2 , -H/2]
        self.low_flange_main_point_2 = [Bl/2 , -H/2 + tl]
        self.top_flange_main_point_1 = [-Bu/2 , H/2 - tu]
        self.top_flange_main_point_2 = [Bu/2 , H/2]
        self.web_main_point_1 = [-tm/2 , -H/2 + tl]
        self.web_main_point_2 = [tm/2 , H/2- tl]
    def plot(self):
        super().plot()
        self.ax.add_patch(patches.Rectangle(self.low_flange_main_point_1 , 
                                            self.low_flange_width, 
                                            self.low_flange_thickness , color='r'))
        self.ax.add_patch(patches.Rectangle(self.top_flange_main_point_1, 
                                            self.top_flange_width, 
                                            self.top_flange_thickness, color='r'))
        self.ax.add_patch(patches.Rectangle(self.web_main_point_1, 
                                            self.web_thickness, 
                                            (self.height-self.top_flange_thickness-
                                             self.low_flange_thickness), color='r'))
        self.ax.set(xlim=(-500, 500), ylim=(-500, 500))
        plt.axis('equal')
        plt.grid()
        plt.show()

    def compute_area(self):
        self.area = (self.top_flange_width * self.top_flange_thickness 
                     + self.low_flange_width * self.low_flange_thickness 
                     + (self.height - self.top_flange_thickness - self.low_flange_thickness)
                     *self.web_thickness)
        return self.area
    
    def compute_Ix(self):
        pass

    def compute_Iy(self):
        pass



if __name__ == '__main__':
    lvl_01_05_col = HSection(600, 600, 600, 30, 30, 30)
    
    lvl_06_10_col = HSection(550, 550, 550, 24, 24, 24)
    
    lvl_11_14_col = HSection(500, 500, 500, 20, 20, 20)
    
    lvl_all_beam = HSection(500, 500, 300, 12, 12, 24)
    
#    h_test = HSection(600, 600, 600, 30, 30, 30)
#    h_test.plot()
#    print(h_test.low_flange_main_point_1)
#    print(h_test.low_flange_main_point_2)
#    print(h_test.top_flange_main_point_1)
#    print(h_test.top_flange_main_point_2)
#    print(h_test.web_main_point_1)
#    print(h_test.web_main_point_2)
#    print(h_test.compute_area())

