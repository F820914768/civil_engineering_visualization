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
        self.Bu = Bu
        self.Bl = Bl
        self.tu, self.tl, self.tm = tu, tl, tm

    def plot(self, range=((-500, 500), (500, 500))):
        super().plot()
        self.ax.add_patch(patches.Rectangle((0,0), 
                                        self.Bl, 
                                        self.tl))
        self.ax.add_patch(patches.Rectangle(((self.Bl-self.Bu)/2,
                                        self.H-self.tu), 
                                        self.Bu, 
                                        self.tu))
        self.ax.add_patch(patches.Rectangle(((self.Bl-self.tm)/2,
                                        self.tl), 
                                        self.tm, 
                                        (self.H-self.tu-self.tl)))
        self.ax.set(xlim=(-200, 499), ylim=(0, 500))
        plt.show()

    def compute_area(self):
        return self.Bu*self.tu + self.Bl*self.tl + (self.H - self.tu - self.tl)*self.tm
    
    def compute_Ix(self):
        pass

    def compute_Iy(self):
        pass

    def get_coordinates(self):
        pass


class TSection(Section):
    def __init__(self, B, H, tu, tm):
        super().__init__(B, H)
        self.tu, self.tm = tu, tm

    def plot(self):
        super().plot()
        self.ax.add_patch(patches.Rectangle((0,
                                        self.H-self.tu), 
                                        self.B, 
                                        self.tu))
        self.ax.add_patch(patches.Rectangle(((self.B-self.tm)/2,
                                        0), 
                                        self.tm, 
                                        (self.H-self.tu)))
        self.ax.set(xlim=(-200, 499), ylim=(0, 500))
        plt.show()
        
if __name__ == '__main__':
    h_test = HSection(400, 300, 200, 18, 12, 8)
    h_test.plot()
    
    print(h_test.compute_area())

    T_test = TSection(400, 400, 12, 18)
    T_test.plot()

