class Database:
    def __init__(self,min_lat,max_lat,min_long,max_long):
        self.head_node = Node(min_lat,max_lat,min_long,max_long)
        
