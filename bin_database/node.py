class Node:
    def __init__(self, min_lat, max_lat, min_long, max_long):
        self.parent=Node()
        self.children=[None, None]
#the values below will all be floats
        self.min_lat = min_lat
        self.max_lat = max_lat
        self.min_long = min_long
        self.max_long = max_long
        self.bin = bin()

    def get_min_lat(self):
        return self.min_lat
    
    def get_max_lat(self):
        return self.max_lat
    
    def get_min_long(self):
        return self.min_long
    
    def get_max_long(self):
        return self.max_long
    
    def update_lat(self, max_lat_new, min_lat_new):
        self.min_lat=min_lat_new
        self.max_lat=max_lat_new  
        
    def update_long(self, min_long_new, max_long_new):
        self.min_long= min_long_new
        self.max_ling=max_long_new
    def within_lat(self, node1): #checks if node1 is within the current node (for the latitude bounds)
        if self.min_lat < node1.min_lat:
            if self.max_lat > node1.max_lat:
                return True
        else:
            return False
    def within_long(self,node1): #checks if node1 is within the current node (for longitude bounds)
        if self.min_long < node1.min_long:
            if self.max_long > node1.max_long:
                return True
        else:
            return False