from shapely.geometry import Point, Polygon
import matplotlib.pyplot as plt
area = [(0,0), (0,10), (10,10), (10,0)]
start_pos = (3,3)
def shrink_or_swell_shapely_polygon(my_polygon, factor=0.10, swell=False):
    ''' returns the shapely polygon which is smaller or bigger by passed factor.
        If swell = True , then it returns bigger polygon, else smaller '''


    xs = list(my_polygon.exterior.coords.xy[0])
    ys = list(my_polygon.exterior.coords.xy[1])
    x_center = 0.5 * min(xs) + 0.5 * max(xs)
    y_center = 0.5 * min(ys) + 0.5 * max(ys)
    min_corner = Point(min(xs), min(ys))
    max_corner = Point(max(xs), max(ys))
    center = Point(x_center, y_center)
    shrink_distance = center.distance(min_corner)*factor

    if swell:
        my_polygon_resized = my_polygon.buffer(shrink_distance) #expand
    else:
        my_polygon_resized = my_polygon.buffer(-shrink_distance) #shrink

    #visualize for debugging
    #x, y = my_polygon.exterior.xy
    #plt.plot(x,y)
    #x, y = my_polygon_shrunken.exterior.xy
    #plt.plot(x,y)
    ## to net let the image be distorted along the axis
    #plt.axis('equal')
    #plt.show()    
    
    return my_polygon_resized
def map2graph(drivable_area,starting_pos):
    #plot map
    map_poly= Polygon(drivable_area)
    pos = Point(starting_pos)
    map_x,map_y = map_poly.exterior.xy
    pos_x, pos_y = pos.xy

    plt.plot(map_x, map_y)
    plt.plot(pos_x, pos_y,'o')
    shrinked_poly = map_poly
    for i in range(5):
        shrinked_poly = shrink_or_swell_shapely_polygon(shrinked_poly)
        shrinked_x,shrinked_y = shrinked_poly.exterior.xy
        plt.plot(shrinked_x,shrinked_y)
    plt.show()
if __name__ == "__main__":

    map2graph(area, start_pos)