"""
I thought we agreed on not structuring our "database" as a tree and instead we were just going to use a python list, so I don't know why this even exists.
"""

class Node:
    def __init__(self):
        self.parent=Node()
        self.children=[Node()]
#the values below will all be floats
        self.min_lat = 0.0
        self.max_lat = 0.0
        self.min_long = 0.0
        self.max_long = 0.0
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