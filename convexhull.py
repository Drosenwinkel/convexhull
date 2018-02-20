import math
import sys
import random
EPSILON = sys.float_info.epsilon

'''
Given two points, p1 and p2,
an x coordinate, x,
and y coordinates y3 and y4,
compute and return the (x,y) coordinates
of the y intercept of the line segment p1->p2
with the line segment (x,y3)->(x,y4)
'''
def yint(p1, p2, x, y3, y4):
	x1, y1 = p1
	x2, y2 = p2
	x3 = x
	x4 = x
	px = ((x1*y2 - y1*x2) * (x3 - x4) - (x1 - x2)*(x3*y4 - y3*x4)) / \
		 float((x1 - x2)*(y3 - y4) - (y1 - y2)*(x3 - x4))
	py = ((x1*y2 - y1*x2)*(y3-y4) - (y1 - y2)*(x3*y4 - y3*x4)) / \
			float((x1 - x2)*(y3 - y4) - (y1 - y2)*(x3-x4))
	return (px, py)

'''
Given three points a,b,c,
computes and returns the area defined by the triangle
a,b,c. 
Note that this area will be negative 
if a,b,c represents a clockwise sequence,
positive if it is counter-clockwise,
and zero if the points are collinear.
'''
def triangleArea(a, b, c):
	return (a[0]*b[1] - a[1]*b[0] + a[1]*c[0] \
                - a[0]*c[1] + b[0]*c[1] - c[0]*b[1]) / 2.0;

'''
Given three points a,b,c,
returns True if and only if 
a,b,c represents a clockwise sequence
(subject to floating-point precision)
'''
def cw(a, b, c):
	return triangleArea(a,b,c) < EPSILON;
'''
Given three points a,b,c,
returns True if and only if 
a,b,c represents a counter-clockwise sequence
(subject to floating-point precision)
'''
def ccw(a, b, c):
	return triangleArea(a,b,c) > EPSILON;

'''
Given three points a,b,c,
returns True if and only if 
a,b,c are collinear
(subject to floating-point precision)
'''
def collinear(a, b, c):
	return abs(triangleArea(a,b,c)) <= EPSILON

'''
Given a list of points,
sort those points in clockwise order
about their centroid.
Note: this function modifies its argument.
'''
def clockwiseSort(points):
	# get mean x coord, mean y coord
	xavg = sum(p[0] for p in points) / len(points)
	yavg = sum(p[1] for p in points) / len(points)
	angle = lambda p:  ((math.atan2(p[1] - yavg, p[0] - xavg) + 2*math.pi) % (2*math.pi))
	points.sort(key = angle)



'''rotates a list n places'''
def rotate(l, n):
    return l[-n:] + l[:-n]


'''
    merges two convex hulls into one
    input: list a, list b     -- where any x value of a is less than any x value of b, --and both are convex hulls
    output: list -- the convex hull of the merged lists
'''
def merge(a,b):
    a = sorted(a, key=lambda p: p[0])  # sort the points by x value
    b = sorted(b, key=lambda p: p[0])  # sort the points by x value

    a_closest_to_L=a[len(a)-1]
    b_closest_to_L=b[0]
    mid_L= (a_closest_to_L[0]+b_closest_to_L[0])/2

    clockwiseSort(a)
    clockwiseSort(b)

    al=sys.maxsize

    a_index = a.index(a_closest_to_L)
    b_index = b.index(b_closest_to_L)

    i=a_index
    j=b_index

    print(str(a[i]))
    print(str(b[j]))

    # y(i, j+1)
    y_i_j1= yint(a[i],b[(j - 1) % len(b)],mid_L,0,al)[1]
    #y(i,j)
    y_i_j= yint(a[i],b[j],mid_L,0,al)[1]
    #y(i-1,j)
    y_1i_j=yint(a[(i + 1) % len(a)],b[j],mid_L,0,al)[1]

    """
    Initialization:
    -The list is initialized with the right most point of a and the leftmost point of b. Therefore incrementing
    will either cause the y intercept to increase or the initial value is the upper tangent.
    
    Maintenance:
    -A change of indices means that either a comparision point on A (with index i) or a point on b (index b) has caused the
     y intercept to increase. Since A and B are already convex hulls, when the y intercept decreases for either side
    (by checking i+1  or  j-1 to see next possible values) then the current values are the maximum possible points.
    -Though the while loop will run when incrementing indices of A or B, the IF statement ensures that the 
    indices only change when the y intercept increases
    
    Termination:
    -When moving clockwise for A (and counter clockwise for B) once a point causes the y intercept to decrease there
     is no possibility of a higher point being further on because both A and B are already convex hulls.
    """
    while((y_i_j1 > y_i_j) or (y_1i_j > y_i_j)):
        if( y_i_j1 > y_i_j):
            j=(j-1)%len(b)
        else:
            i=(i+1)%len(a)
        y_i_j1 = yint(a[i], b[(j-1)%len(b)], mid_L, 0, al)[1]
        y_i_j = yint(a[i], b[j], mid_L, 0, al)[1]
        y_1i_j = yint(a[(i + 1) % len(a)], b[j], mid_L, 0, al)[1]


    lower_bound_a = a[i]
    lower_bound_b= b[j]
    lower_bound_b_i=j



    ##now looking for upper tangent##
    i = a_index
    j = b_index

    # y(i, j+1)
    y_i_j1 = yint(a[i], b[(j + 1) % len(b)], mid_L, 0, al)[1]
    # y(i,j)
    y_i_j = yint(a[i], b[j], mid_L, 0, al)[1]
    # y(i-1,j)
    y_1i_j = yint(a[(i - 1) % len(a)], b[j], mid_L, 0, al)[1]

    '''
    This loop is the same as the one above except we are traversing down the lists moving in opposite directions.
    Like before, an increment means that there is a lower y intercept from a change in i or j and the loop
    terminates when attempting to increment (by checking the next values) would increase the y intercept.
    '''
    while ((y_i_j1 < y_i_j) or (y_1i_j < y_i_j)):
        if (y_i_j1 < y_i_j):
            j = (j + 1) % len(b)
        else:
            i = (i - 1) % len(a)

        y_i_j1 = yint(a[i], b[(j + 1) % len(b)], mid_L, 0, al)[1]
        y_i_j = yint(a[i], b[j], mid_L, 0, al)[1]
        y_1i_j = yint(a[(i - 1) % len(a)], b[j], mid_L, 0, al)[1]


    upper_bound_a = a[i]
    upper_bound_b= b[j]
    upper_bound_a_i=i




    '''
    Initialization: 
    -The list is sorted in clockwise order with the index as the upperbound+1 (because we do not want to delete
     the upperbound). The while statment checks to make sure that y does not equal both lower and upper bound 
     because there are some cases where the upper and lower bound maybe the same.
    
    Maintenance:
    -for each iteration the value next to the upperbound is deleted. Because this shortens the list i does not 
    need to be incremented.
    
    Termination:
    -once we reach the lowerbound the loop terminates, preserving the elements other than those between the lower
    and upper bound
    
    '''
    i=upper_bound_a_i+1
    while((a[i %len(a)]!=lower_bound_a)and (a[i%len(a)]!=upper_bound_a)):
        del a[i %len(a)]


    '''
    This is the same case as before with the exception that the loop starts at the lower bound and terminates at the
    upper bound of b.
    '''
    i=lower_bound_b_i+1
    while((b[i %len(b)]!=lower_bound_b)and (b[i%len(b)]!=upper_bound_b)):
        del b[i %len(b)]
    return a+b



def naive_compute_hull(points):
    print(len(points))
    if(len(points) < 4):
        return points
    else:
        hull = []
        for i in range(len(points)):
            for j in range(len(points)):
                num_cw = 0
                for k in range(len(points)):
                    if(cw(points[i], points[j], points[k]) and k != i and k != j and i != j):
                        num_cw += 1
                if(num_cw == (len(points))-2):
                    hull.append(points[i])
                    hull.append(points[j])

        hull = list(set(hull))

        return hull


def generate_points(num_points):
    points = []
    point_x_min = 5
    point_x_max = 990
    point_y_min = 100
    point_y_max = 790

    for i in range(num_points):
        point = (random.randint(point_x_min, point_x_max),
                    random.randint(point_y_min, point_y_max))
        points.append(point)

    return points


'''
generates the convex hulls of a set of points using recursion
input:set of points
output: convex hull of those points

Algorithm:
    if the num points less than 7 (base case) use the naive_compute_hull
    otherwise split the list into two and evaluate recursively

Complexity: nlog(n)
    The merge algorithm uses linear time for merging the lists
    The computeHull is recursively called log(n) times.
'''

def computeHull(points):

    #if the hull is only 3 points return the list
    if(len(points)<7):
        return naive_compute_hull(points)
    else:

        #start by splitting the hull
        points = sorted(points, key= lambda p: p[0]) #sort the points by x value

        a= points[0:(int)(len(points)/2)]
        b= points[(int)(len(points) / 2): len(points)]

        #get the sublists into covex hulls
        a = computeHull(a)
        b = computeHull(b)

        newPoints= merge(a,b)

        clockwiseSort(newPoints)
    return newPoints




