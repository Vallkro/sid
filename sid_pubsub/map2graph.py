import networkx as nx
from shapely.geometry import Polygon, Point, LineString
import matplotlib.pyplot as plt
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
                if self.boundry.contains(p_geom) and not inside_obstacle:

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
                    #TODO: should also check obs
                    # add edge between node and neighbour
                    self.G.add_edge(node, neighbour)

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
    plt.show()
    grid = Grid(bounds, obs, scale)
    grid.generate()
    pos = nx.get_node_attributes(grid.G,'pos')
    nx.draw(grid.G, pos, with_labels=True)
    plt.show()




    

