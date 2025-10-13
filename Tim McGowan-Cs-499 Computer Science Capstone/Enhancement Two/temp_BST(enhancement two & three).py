# Timouth McGowan\
# Enhancment Two/three
# https://www.w3schools.com/dsa/dsa_data_binarysearchtrees.php

from pymongo import MongoClient # imports mongo

# store temperature data and the timestamps
class TempNode:
    def __init__(self, timestanp, temperature):
        # Time the temp was taken
        self.timestamp = timestamp
        # temp value
        self.temperature = temperature
        # the left child is (lower temp)
        self.left = None
        # the right child is (higher or equa temp)
        self.right = None
        
# Defines the BST 
class TempBST:
    def __init__(self):
        self.root = None
    
    # Insers a new temp reading to the tree
    def insert(self, timestamp, temperature):
        new_node = TempNode(timestamp, temperature)
        if not self.root:
            # sets root if tree is empty
            self.root = new_node
        else:
            self._insert_recursive(self.root, new_node)
    
    # Helper method to insert recursively baseed on temp
    def _insert_recursive(self, current, new_node):
        if new_node.temperature < current.temperature:
            if current.left:
                self._insert_recursive(current.left, new_node)
            else:
                # Insers to the left if no child
                current.left = new_node
        else:
            if current.right:
                self._insert_recursive(current.right, new_node)
            else:
                # Insert to the right if no child
                current.right = new_node
                
    # Traverse the BST in order and print the temp reading
    def in_order_traversal(self, node):
        if node:
            # left subtree
            self.in_order_traversal(node.left)
            # print current node
            print(f"{node.timestamp}: {node.temperature}F")
            # right subtree
            self.in_order_traversal(node.right)

# loads temp loggs from the .txt file and inserts them into the BST
def load_logs_from_file(filename, bst):
    try:
        with open(filename, 'r') as file:
            for line in file:
                parts = line.strip().split(',')
                if len(parts) == 2:
                    timestamp = parts[0].strip()
                    try:
                        temperature = float(parts[1].strip())
                        bst.insert(timestamp, temperature)
                    except ValueError:
                        print(f"Invalid temperature format: {parts[1]}")
    except FileNotFoundError:
        print(f"File not found: {filename}")
        
# Loads temperatures from MongoDB
def load_logs_from_database(bst):
    # connects to mongo
    client = MongoClient("mongodb://localhost:27017/")
    # access theromstat database
    db = client["thermostat"]
    # accesss the readings
    collection = db["readings"]
    # iterates over the doc
    for doc in collection.find():
        timestamp = doc.get("timestamp")
        temperature = doc.get("temperature")
        if timestamp and isinstance(temperature, (int, float)):
            # insers into the BST
            bst.insert(timestamp, temperature)
        
# Example usage
if __name__ == "__main__":
    # create a new bst instance
    temp_bst = TempBST()
    print("choose data source:")
    print("1. Load short term data")
    print("2. Load database data")
    choice = input("Enter 1 or 2: ").strip()
    
    if choice == "1":
        # load data from the log file
        load_logs_from_file('tempLog.txt', temp_bst) 
    elif choice == "2":
        # load data from MongoDB
        load_logs_from_database(temp_bst)
    else:
        print("Invalid option")
        exit()
        
    print("Temperature readings in ascending order:")
    # prints the sorted temps
    temp_bst.in_order_traversal(temp_bst.root)