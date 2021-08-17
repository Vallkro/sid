from map2graph import Grid
import networkx as nx
from shapely.geometry import Polygon, Point, LineString
import matplotlib.pyplot as plt
import math
import numpy as np
import time

from matplotlib.animation import FuncAnimation

fig, ax = plt.subplots()
xdata, ydata = [], []
ln, = plt.plot([], [], 'r')

def init():
    ax.set_xlim(-2, 12)
    ax.set_ylim(-2, 12)
    return ln,

def update(frame):
    xdata.append(frame[0])
    ydata.append(frame[1])
    ln.set_data(xdata, ydata)
    return ln,

if __name__ == "__main__":

    # define square grid 
    bounds = Polygon([(0,0),(0,10),(10,10),(10,0)])
    minx, miny, maxx, maxy = bounds.bounds # shapely minmax bounds
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
    x,y = LineString(T).xy

    hl, = plt.plot([], [])

    ani = FuncAnimation(fig, update, frames=T,
                        init_func=init, blit=True)
    plt.show()
    #plt.plot(x,y,'r',linewidth=2,)
    #plt.show()