import openseespy.opensees as ops



class MaterialManager:
    def __init__(self):
        self.matTag = 0
        self.dict = {}
        
    def __repr__(self):
        return '{}'.format(self.dict)
    
    def addMaterial(self, matType, **matKargs):
        ops.uniaxialMaterial(matType, self.matTag, **matKargs)
        self.dict[self.matTag] = {'matType':matType, **matKargs}
        self.matTag += 1
        
    def __getitem__(self, matTag):
        if not self.__exist(matTag):
            raise IndexError('{} not found'.format(matTag))
        return self.dict[matTag]        
    
    def __exist(self, matTag):
        if matTag in self.dict:
            return True
        return False
    


if __name__ == '__main__':
    materials = MaterialManager()
    materials.addMaterial('FRPConfinedConcrete', fpc1 = 1000, fpc2 = 20000)
    
    
    