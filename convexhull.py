import math
import sys

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



'''
Replace the implementation of computeHull with a correct computation of the convex hull
using the divide-and-conquer algorithm
'''


def computeHull(points):

    #if the hull is only 3 points return the list
    if(len(points)<4):
        print("compute hull called, basecase ")
        print(points)
        print()

        clockwiseSort(points)
        return points
    else:
        print("compute hull called")
        print(points)
        print()

        #start by splitting the hull
        points = sorted(points, key= lambda p: p[0]) #sort the points by x value

        print("points after sort by x val")
        print(points)
        print()

        a= points[0:(int)(len(points)/2)]
        b= points[(int)(len(points) / 2): len(points)]

        #get the sublists into covex hulls
        a = computeHull(a)
        b = computeHull(b)



        #merge the two hulls together

        #start by finding rightmost a and leftmost b
        #a = sorted(a, key= lambda k: k[0])
        #b = sorted(b, key= lambda k: k[0])

        upper_a = a[len(a)-1] #rightmost a
        upper_a_index=len(a)


        upper_b = b[0] #leftmost b
        upper_b_index = 0

        upper_y = 1.1-sys.maxsize

        #center value
        c=(upper_a[0]+upper_b[0])/2

        clockwiseSort(a)
        clockwiseSort(b)

        print(' a then b after clockwise sort')
        print(a)
        print(b)
        print()

        #print('x sorted b[0]' + str(upper_b) +' clockwise sorted b[0]: ' + str(b[0]))


        #loop to find real upper b
        for i in range(len(b)):
            y_intercept = yint(upper_a,b[i], c, upper_a[1], b[i][1])
            if y_intercept[1] > upper_y:
                upper_y=y_intercept[1]
                upper_b = b[i]
                upper_b_index=i
            else:
                break

        print('upper b, upper y found: ')
        print(upper_b)
        print(upper_y)
        print()

        for i in range(len(a),0):
            y_intercept = yint(a[i],upper_b,c, a[i][1],upper_b[1])
            if y_intercept[1] > upper_y:
                upper_y=y_intercept[1]
                upper_a = a[i]
                upper_a_index = i
            else:
                break

        print('upper a, new upper y found: ')
        print(upper_a)
        print(upper_y)
        print()


        lower_a = a[-1]
        lower_a_index = len(a)

        lower_b= b[0]
        lower_b_index = 0

        lower_y = sys.maxsize - 1.1

        for i in range(len(b),0):
            y_intercept = yint(b[i], lower_a , c , b[i][1], lower_a[1])
            if y_intercept[1] < lower_y:
                lower_y= y_intercept[1]
                lower_b = b[i]
                lower_b_index =i
            else:
                break

        for i in range(0, len(a)):
            y_intercept = yint(a[i], lower_b, c , a[i][1], lower_b[1])
            if y_intercept[1] < lower_y:
                lower_y = y_intercept[1]
                lower_a = a[i]
                lower_a_index = i
            else:
                break


        newPoints = a[lower_a_index:upper_a_index]
        newPoints.extend(b[upper_b_index:lower_b_index])

        clockwiseSort(newPoints)
    return newPoints