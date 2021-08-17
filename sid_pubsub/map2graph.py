import networkx as nx
from shapely.geometry import Polygon, Point, LineString
import matplotlib.pyplot as plt
import math
import numpy as np
import time
class Grid:
    def __init__(self, boundry, obstacles, scale):
        self.boundry = boundry
        self.obstacles = obstacles
        self.scale = scale # in m
        self.G=nx.Graph()
    def in_obstacle(self,geometry):
        """
        takes shapely geometry type
        returns True if the point is inside any of the obstacles"""
        for obstacle in self.obstacles:
            if obstacle.contains(geometry):
                return True

        return False
    def generate(self):
        minx, miny, maxx, maxy = self.boundry.bounds
        
        #iterate over every
        i_x = 0
        while( i_x <= maxx):
            j_y = 0
            while( j_y <= maxy ):
                p = (i_x, j_y)
                print(p)
                p_geom = Point(p)
                inside_obstacle = self.in_obstacle(p_geom)
                if p_geom.within(self.boundry) and not inside_obstacle:

                    # TODO: should also check for obstacles
                    self.G.add_node(p, pos = p)
                j_y = j_y + self.scale
            
            i_x = i_x + self.scale

        node_list = list(self.G.nodes)
        # NW N NE
        # W    E
        # SW S SE
        dirs = [(-self.scale,self.scale),(0,self.scale),(self.scale,self.scale),
                (-self.scale,0),                        (self.scale,0),
                (self.scale,-self.scale),(0,-self.scale),(self.scale,-self.scale)]

        for node in node_list:
            for direction in dirs:
                neighbour = (node[0] + direction[0], node[1] + direction[1])
                neighbour_point = Point(neighbour)
                line = LineString([node, neighbour])

                inside_obstacle = self.in_obstacle(line)
                if self.boundry.contains(line) and neighbour in node_list and not inside_obstacle:
                    # dist = sqrt ( (x1-x2)^2 + (y1-y2)^2)
                    distance = math.sqrt((node[0] - neighbour[0])**2 + (node[1] - neighbour[1])**2)
                    #TODO : maybe add some extra cost for angluar differences
                    self.G.add_edge(node, neighbour, weight=distance)

    def getRoute(self):
        """ Returns an approximation of traveling salesman problem as a circular list of tuples [(x1,y1),...,(xn,yn),(x1,y1)]"""
        # solve the pathplan to cover whole area
        tsp = nx.approximation.traveling_salesman_problem
        T = tsp(self.G, weight="weight", cycle=True)
        return T
if __name__ == "__main__":
    # define square grid 
    bounds = Polygon([(0,0),(0,10),(10,10),(10,0)])
    obs = [Polygon([(3,3),(3,4),(4,4),(4,3)])]
    scale = 0.5
    x,y = bounds.exterior.xy
    for ob in obs:
        ob_x,ob_y = ob.exterior.xy
        plt.plot(ob_x,ob_y)
    plt.plot(x,y)
    grid = Grid(bounds, obs, scale)
    grid.generate()
    pos = nx.get_node_attributes(grid.G,'pos')
    nx.draw(grid.G, pos, with_labels=True)
    T = grid.getRoute()
    ## solve the pathplan to cover whole area
    #tsp = nx.approximation.traveling_salesman_problem
    #T = tsp(grid.G, weight="weight")
    print(T)
    x,y = LineString(T).xy

    hl, = plt.plot([], [])

    def update_line(hl, new_data):
        hl.set_xdata(np.append(hl.get_xdata(), new_data[0]))
        hl.set_ydata(np.append(hl.get_ydata(), new_data[1]))
        plt.draw()
    plt.show()
    for pos in T:
        update_line(hl, pos)
        time.sleep(0.01)        
    #plt.plot(x,y,'r',linewidth=2,)
    #plt.show()



    

