import itertools
import numpy
grid_points = []
grid_size_n = 5
grid_x = range(grid_size_n)
grid_y = range(grid_size_n)
x_coordinates, y_coordinates = numpy.meshgrid(grid_x,grid_y,indexing='xy')
coordinate_array = itertools.zip_longest(x_coordinates,y_coordinates)
for field in coordinate_array:
    x_field       = field[0]
    y_field       = field[1]
    grid_location = [itertools.zip_longest(x_field,y_field)]
    grid_points.append(grid_location)

for cell_x_position ,cell_y_position in coordinate_array:
    grid_points.append(itertools.zip_longest(cell_x_position,cell_y_position))

#for (x_coord, y_coord) in coordinate_array:

#>>> x_coordinates
#array([[0, 1, 2, 3, 4],
#       [0, 1, 2, 3, 4],
#       [0, 1, 2, 3, 4],
#       [0, 1, 2, 3, 4],
#       [0, 1, 2, 3, 4]])
#>>> x_coordinates[0]

#array([0, 1, 2, 3, 4])
#>>> asdf = itertools.zip_longest(x_coordinates,y_coordinates)

#>>> for each in asdf:
#...     print(each)
#... 
#>>> asdf = itertools.zip_longest(x_coordinates,y_coordinates)
#>>> for each in asdf:
#...     print(each[1]) # this is y field
#...                     
#[0 0 0 0 0]
#[1 1 1 1 1]
#[2 2 2 2 2]
#[3 3 3 3 3]
#[4 4 4 4 4]
#       field[0]                 field[1]
#       x axis                   y axis
#(array([0, 1, 2, 3, 4]), array([0, 0, 0, 0, 0]))
#(array([0, 1, 2, 3, 4]), array([1, 1, 1, 1, 1]))
#(array([0, 1, 2, 3, 4]), array([2, 2, 2, 2, 2]))
#(array([0, 1, 2, 3, 4]), array([3, 3, 3, 3, 3]))
#(array([0, 1, 2, 3, 4]), array([4, 4, 4, 4, 4]))