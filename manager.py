
class Manager:
    def __init__(self, key_type_ = tuple):
        self.dict = {}
        self.anti_dict = {}
        self.key_attributes = {}
        self.id_attributes = {}
        self.i = 1 
        self.key_type_ = tuple       

    def __type_checking(self, key):
        if not isinstance(key, self.key_type_):
            key = self.key_type_(key)
        return key

    def __getitem__(self, ID):
        return self.anti_dict[ID]

    def __iter__(self):
        elements = self.get_all()
        for element in elements:
            yield element

    def __repr__(self):
        return '{}'.format(self.dict)

    def __len__(self):
        return self.i

    def exist(self, coordinate):
        coordinate = self.__type_checking(coordinate)
        if coordinate in self.dict:
            return True
        else:
            return False

    def get(self, key):
        key = self.__type_checking(key)
        return self.dict[key]

    def anti_get(self, id):
        return self.anti_dict[id]

    def get_all(self):
        output = []
        for key in self.dict:
            output.append([self.get(key), *key])
        return output

    def get_all_id(self):
        return self.anti_dict.keys()

    def delete(self, key):
        if self.exist(key):
            key = self.get(key)
            self.dict.pop(key)
            self.anti_dict.pop(key)

    def add(self, key, **kwargs):
        key = self.__type_checking(key)
        if self.exist(key):
            return True
        
        self.dict[key] = self.i
        self.anti_dict[self.i] = key
        self.i += 1

        if not kwargs:
            self.key_attributes[key] = kwargs
            self.id_attributes = kwargs

    def get(self, key):
        key = self.__type_checking(key)
        return self.dict[key]

    def has_attribute(self, key):
        key = self.__type_checking(key)
        if key in self.key_attributes and key in self.dict:
            return True
        return False

    def has_attribute_by_id(self, id):
        if id in self.id_attributes and id in self.anti_dict:
            return True
        return False

    def get_attribute(self, key):
        key = self.__type_checking(key)
        return self.key_attributes[key]

    def get_attribute_by_id(self, id):
        return self.id_attributes[id]

    def add_attribute(self, key, **kwargs):
        key = self.__type_checking(key)
        id = self.get(key)
        #print(kwargs)
        if kwargs:
            if not self.has_attribute(key):
                self.key_attributes[key] = {}
            self.key_attributes[key].update(kwargs)

            if not self.has_attribute_by_id(id):
                self.id_attributes[id] = {}
            self.id_attributes[id].update(kwargs)

    def add_attribute_by_id(self, id, **kwargs):
        key = self.anti_get(id) #; print(kwargs)
        self.add_attribute(key, **kwargs)
                
    def get_all_with_attr(self, attr_name, attr_value):
        ids = self.id_attributes.keys()
        special_ids = []
        for id in ids:
            attr = self.get_attribute_by_id(id)
          
          
            if attr.get(attr_name) == attr_value:
                special_ids.append(id)
        return special_ids

    def get_all_with_attrs(self, **kwargs):
        output = []
        for attr_name, attr_value in kwargs.items():
            output.append(set(self.get_all_with_attr(attr_name, attr_value)))
        output_ids = output[0]
        for ids in output:
            output_ids = output_ids.intersection(ids)
        return list(output_ids)

class NodeManager(Manager):
    '''
    To manage id and coordinate of nodes
    
    methods:
        self.get(coordinate): get a nodeId by coordinate
        self.anti_get(nodeId): get coordinate by nodeId
        self.get_all(): get all nodeId, coordinate
    '''

    def get(self, coordinate, **kwargs):
        '''
        get nodeId by coordinate
        
        Examples
        --------
        >>> node_manager.get((4,3,1))
        0
        '''
        return super().get(coordinate, **kwargs)
         

    

class MemberManager(Manager):
    def __init__(self):

        super().__init__(key_type_=tuple)
        self.__object_dict = {}


    def add(self, node_pair, object_, **kwargs):
        super().add(node_pair, **kwargs)
        id = self.get(node_pair)
        self.__object_dict[id] = object_

    def get_object_by_id(self, id):
        return self.__object_dict[id]

    def get_all_has_attr(self, attr_name):
        output = []
        for id, attr in self.id_attributes.items():
            if attr_name in attr:
                output.append(id)
        return output

    

    