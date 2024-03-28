class Database:
    def __init__(self,min_lat,max_lat,min_long,max_long):
        self.head_node = Node(min_lat,max_lat,min_long,max_long)
    
    def add_node(self,node1): #adding node1 (starting from the current node then going down)
        if self.children[0].within(node1): #this checks if the area described by node1 is within the area described by the left child node
            if self.children[0] is None:
               self.children[0] = node1 
            else:
               self.children[0].add_node(self, node1)
        elif self.children[1].within(node1): #checks if area described by node1 is within the area described by the right child node
               if self.children[1] is None:
                  self.children[1] = node1
               else:
                  self.children[1].insert(node1)
        else: #if node1 is not in the area described by either of the children nodes (and hence not in the area described by the current node)
            print("This area is not in Dhaka")
        
    def remove_node(self,node1): #would likely start with self as the root of the three and this recursive function would work its way down to the appropriate bin and delete it
        if self == None:
            return None
        else: 
            leftNode = self.children[0] #left child of the current node
            rightNode = self.children[1] #right child of current node
            if leftNode.isEqualNode(node1): #checking if the node we want to delete is equal to the left child
                self.children.pop(0) #if yes, remove this node
            elif rightNode.isEqualNode(node1): #checking if the node we want to delete is equal to the right child
                self.children.pop(1) #if yes, remove this node
            else: #if neither child node is equal to the node we want to remove
                if leftNode.within(node1): #if node1 is contained within the leftNode
                    remove_node(leftNode, node1) #call remove function with the leftNode
                elif rightNode.within(node1): #check if node1 is contained within the rightNode
                    remove_node(rightNode,node1) #call remove function with the rightNode
                else:
                    print("This bin is not in Dhaka") #if node1 is not contained within either child node, it must not be in Dhaka
            




   
