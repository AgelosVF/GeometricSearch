import numpy as np
import random
import matplotlib.pyplot as plt

def generate_random_points(num):
    points=[]
    for i in range(num):
        x=round(random.uniform(-10,10),1)
        y=round(random.uniform(-10,10),1)
        points.append((x,y))
    return points

class Node:

    def __init__(self, point, depth, left, right):
        self.point=point #cut point
        self.depth=depth
        self.left =left
        self.right = right



def buildKDTree(Points,depth):
    if len(Points)==1:
        #leaf node
        return Node(Points[0],depth,None,None)
    
    cutDirection=depth%2 #0 means vertical, 1 means horizontal
    if cutDirection==1:
        sorted_points=sorted(Points, key=lambda x: x[1]) #arrange the list by y
    else:
        sorted_points=sorted(Points, key=lambda x: x[0]) #arrange the list by x
    listLength=len(sorted_points)
    middleIndex=listLength//2
    if listLength%2==1:
        middleIndex+=1
    leftList=sorted_points[:middleIndex] #left list
    
    rightList=sorted_points[middleIndex:] #right list
    return Node(leftList[-1],depth,buildKDTree(leftList,depth+1),buildKDTree(rightList,depth+1))
    

def print_tree(node,dir="root"):
    if node is None:
        return
    print("depth= ",node.depth,"Node= ",dir,"value= ",node.point) 
    print_tree(node.left,"left")
    print_tree(node.right,"right")



    import numpy as np

def check_parallelogram_position_x(point, parallelogram):
    x, y = point
    x_coords = parallelogram[:, 0]

    # Check if all x-coordinates of the parallelogram are less than the point's x-coordinate
    if np.all(x_coords < x):
        return "left"
    
    # Check if all x-coordinates of the parallelogram are greater than the point's x-coordinate
    if np.all(x_coords > x):
        return "right"
    
    # If neither condition is met, the parallelogram is on both sides of the line
    return "both"

def check_parallelogram_position_y(point, parallelogram):
    x, y = point
    y_coords = parallelogram[:, 1]

    # Check if all y-coordinates of the parallelogram are less than the point's y-coordinate
    if np.all(y_coords < y):
        return "under"
    
    # Check if all y-coordinates of the parallelogram are greater than the point's y-coordinate
    if np.all(y_coords > y):
        return "above"
    
    # If neither condition is met, the parallelogram is on both sides of the line
    return "both"


def KD_search(node,query_range):
    results=[] #empty list to save the results and return them
    if node.left==None and node.right==None:
        #its a leaf node
        if check_parallelogram_position_x(node.point,query_range)=="both":
            if check_parallelogram_position_y(node.point,query_range)=="both":
                results.append(node.point) #if the leaf is in the query range append it to the list
        return results # Return the list if the leaf is in the query range it will contain it else it will be empty
    if node.depth%2==0:
        #vertical node
        paral_position=check_parallelogram_position_x(node.point,query_range)
        if paral_position=="left":
            results.extend(KD_search(node.left,query_range)) #search the left subtree
        elif paral_position=="right":
            results.extend(KD_search(node.right,query_range)) #search the right subtree
        elif paral_position=="both":
            results.extend(KD_search(node.left,query_range))
            results.extend(KD_search(node.right,query_range)) #if the node is inside the query range search both ways
        else:
            print("ERROR IN KD_SEARCH depth%2==0")
            print_tree(node)
            return -1
    
    elif node.depth%2==1:
        #horizontal node
        paral_position=check_parallelogram_position_y(node.point,query_range)
        if paral_position=="under":
            results.extend(KD_search(node.left,query_range)) #search the left subtree
        elif paral_position=="above":
            results.extend(KD_search(node.right,query_range)) #search the right subtree
        elif paral_position=="both":
            results.extend(KD_search(node.left,query_range))
            results.extend(KD_search(node.right,query_range)) #if the node is inside the query range search both ways
        else:
            print("ERROR IN KD_SEARCH depth%2==1")
            print_tree(node)
    return results



if __name__=="__main__":
    parallelogram = np.array([(1, 1), (1, 5), (5, 5), (5, 1)])
    random_points=generate_random_points(70)
    kdtree=buildKDTree(random_points,0)
    result=KD_search(kdtree,parallelogram)
    print("The points in the parallelogram [(1, 1), (1, 5), (5, 5), (5, 1)] are:",result)

x_coordinates = [point[0] for point in random_points]
y_coordinates = [point[1] for point in random_points]

x_result = [point[0] for point in result]
y_result = [point[1] for point in result]

plt.scatter(x_coordinates, y_coordinates)

plt.scatter(x_result, y_result,c='black',marker='o',edgecolors='red')
plot_parallelogram=np.array([(1, 1), (1, 5), (5, 5), (5, 1),(1,1)])
plt.plot(plot_parallelogram[:, 0], plot_parallelogram[:, 1], 'r-')  # Plot the parallelogram

plt.xlabel('X Coordinate')
plt.ylabel('Y Coordinate')
plt.title('Search for points inside a parallelogram')
plt.show()
