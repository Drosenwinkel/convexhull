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
def rotate(l, n):
    return l[-n:] + l[:-n]



def mergeWhile(a,b):
    a = sorted(a, key=lambda p: p[0])  # sort the points by x value
    b = sorted(b, key=lambda p: p[0])  # sort the points by x value



    a_closest_to_L=a[len(a)-1]
    #print(a_closest_to_L)
    b_closest_to_L=b[0]
    #print(b_closest_to_L)
    mid_L= (a_closest_to_L[0]+b_closest_to_L[0])/2

    clockwiseSort(a)
    clockwiseSort(b)

    print('merging: ' + str(a) + '~~~' + str(b))


    print(str(a.index(a_closest_to_L)))
    a_index = a.index(a_closest_to_L)
    b_index = b.index(b_closest_to_L)

    i=a_index
    j=b_index


    # y(i, j+1)
    y_i_j1= yint(a[i],b[(j - 1) % len(b)],mid_L,0,3000)[1]
   # print('yint between a[i](' + str(a[i]) + ') , b[j+1](' + str(b[a[i],b[(j + 1) % len(b]) + ')      =' +str(y_i_j1))


    #y(i,j)
    y_i_j= yint(a[i],b[j],mid_L,0,3000)[1]
    #print('yint between a[i](' + str(a[i]) + ') , b[j](' + str(b[j]) + ')      =' + str(y_i_j))

    #y(i-1,j)
    y_1i_j=yint(a[(i + 1) % len(a)],b[j],mid_L,0,3000)[1]
    #print('yint between a[i-1](' + str(a[i-1]) + ') , b[j](' + str(b[j]) + ')      =' + str(y_1i_j))

    print('initial i: ' + str(i) + '  j: ' + str(j) )

    while((y_i_j1 > y_i_j) or (y_1i_j > y_i_j)):
        print('y_i_j1: ' + str(y_i_j1) + '  > y_i_j' + str(y_i_j))
        print('i: '+str(i)+'  j: '+str(j))
        if( y_i_j1 > y_i_j):
            print('if true')
            j=(j-1)%len(b)
        else:
            i=(i+1)%len(a)

        y_i_j1 = yint(a[i], b[(j-1)%len(b)], mid_L, 0, 3000)[1]
        y_i_j = yint(a[i], b[j], mid_L, 0, 3000)[1]
        y_1i_j = yint(a[(i + 1) % len(a)], b[j], mid_L, 0, 3000)[1]

        print('yint between a[i](' + str(a[i]) + ') , b[j+1](' + str(b[(j+1)%len(b)]) + ')      =' + str(y_i_j1))
        print('yint between a[i](' + str(a[i]) + ') , b[j](' + str(b[j]) + ')      =' + str(y_i_j))
        print('yint between a[i-1](' + str(a[(i - 1) % len(a)]) + ') , b[j](' + str(b[j]) + ')      =' + str(y_1i_j))
        print('i: '+str(i)+'  j: '+str(j)+'\n\n')

    print('lower tangent:  '+str(a[i])+' , '+str(b[j]))

    lower_bound_a = a[i]
    lower_bound_b= b[j]
    lower_bound_a_i=i
    lower_bound_b_i=j



##########now looking for lower tangent#####
    i = a_index
    j = b_index

    # y(i, j+1)
    y_i_j1 = yint(a[i], b[(j + 1) % len(b)], mid_L, 0, 3000)[1]
    # print('yint between a[i](' + str(a[i]) + ') , b[j+1](' + str(b[a[i],b[(j + 1) % len(b]) + ')      =' +str(y_i_j1))

    # y(i,j)
    y_i_j = yint(a[i], b[j], mid_L, 0, 3000)[1]
    # print('yint between a[i](' + str(a[i]) + ') , b[j](' + str(b[j]) + ')      =' + str(y_i_j))

    # y(i-1,j)
    y_1i_j = yint(a[(i - 1) % len(a)], b[j], mid_L, 0, 3000)[1]
    # print('yint between a[i-1](' + str(a[i-1]) + ') , b[j](' + str(b[j]) + ')      =' + str(y_1i_j))

    print('initial i: ' + str(i) + '  j: ' + str(j))

    while ((y_i_j1 < y_i_j) or (y_1i_j < y_i_j)):
        print('y_i_j1: ' + str(y_i_j1) + '  > y_i_j' + str(y_i_j))
        print('i: ' + str(i) + '  j: ' + str(j))
        if (y_i_j1 < y_i_j):
            print('if true')
            j = (j + 1) % len(b)
        else:
            i = (i - 1) % len(a)

        y_i_j1 = yint(a[i], b[(j + 1) % len(b)], mid_L, 0, 3000)[1]
        y_i_j = yint(a[i], b[j], mid_L, 0, 3000)[1]
        y_1i_j = yint(a[(i - 1) % len(a)], b[j], mid_L, 0, 3000)[1]

        print('yint between a[i](' + str(a[i]) + ') , b[j+1](' + str(b[(j + 1) % len(b)]) + ')      =' + str(y_i_j1))
        print('yint between a[i](' + str(a[i]) + ') , b[j](' + str(b[j]) + ')      =' + str(y_i_j))
        print('yint between a[i-1](' + str(a[(i - 1) % len(a)]) + ') , b[j](' + str(b[j]) + ')      =' + str(y_1i_j))
        print('i: ' + str(i) + '  j: ' + str(j) + '\n\n')

    print('upper tangent:  ' + str(a[i]) + ' , ' + str(b[j]))


    upper_bound_a = a[i]
    upper_bound_b= b[j]
    upper_bound_a_i=i
    upper_bound_b_i=j

    i=upper_bound_a_i+1
    while((a[i %len(a)]!=lower_bound_a)and (a[i%len(a)]!=upper_bound_a)):
        print('deleting')
        del a[i %len(a)]

    print('new a : '+str(a))


    i=lower_bound_b_i+1
    while((b[i %len(b)]!=lower_bound_b)and (b[i%len(b)]!=upper_bound_b)):
        print('deleting')
        del b[i %len(b)]


    print('new b : '+str(b))

    return a+b












def merge(a,b):
    a = sorted(a, key=lambda p: p[0])  # sort the points by x value
    b = sorted(b, key=lambda p: p[0])  # sort the points by x value

    print('\n\n86*******trying to merge a and b******')
    print(a)
    print(b)
    print()

    ## find highest point index index on left polygon
    highest_a = a[len(a)-1] # we will start with the left most point and move clockwise
    highest_b= b[0]
    highest_a_i=len(a)-1
    highest_b_i=len(b)
    lowest_a_i=len(a)-1
    lowest_b_i=len(b)

    mid_line = (highest_a[0]+highest_b[0])/2

    clockwiseSort(a)
    clockwiseSort(b)

    print("106***merge sort: now sorting b upper***")
    #find the leftmost point in the newly sorted b
    #for i in range(len(b)):
    #    if( b[i]== highest_b):
    #        highest_b_i=i
    #        lowest_b_i=i
    #        print('leftmost b: ' + str(highest_b))
    #        print('index: '+str(highest_b_i))
    #for i in range(len(a)):
    #    if(a[i]==highest_a):
    #        highest_a_i=i
    #        lowest_a_i=1




    #a=rotate(a,highest_a_i+1)
    b=rotate(b,highest_b_i+1)
    print('rotated b: '+str(b))
    print('rotated a'+str(a))

    print('midline:  '+str(mid_line))


    print('\n130***merge: now sorting b upper')
   #(yint(a[highest_a_i], b[highest_b_i], mid_line, 0, 3000))[1]
    #find the highest value (closest to top)
    y = yint(a[0], b[0], mid_line, 0, 3000)[1]
    for i in range(1,len(b)-1,1):
        newY=(yint(a[0],b[i],mid_line,0,3000)[1])

        print('123 iterators   i:'+str(i)+'   highest b i : '+str(highest_b_i) +'   point'+str(b[highest_b_i]))
        print('old y: ' + str(y) + ' <  new yint ' + str(newY))
        if(y > newY):
            print('133 if statment true     i='+str(i))
            highest_b_i=i
        else:
            print('136 else statement true')
            break #else break
        y = yint(a[0], b[i], mid_line, 0, 3000)[1]

    print('b: '+ str(b))
    print('b upper: '+str(b[highest_b_i])+'\n\n')




    print("151***merge: now sorting a upper***")
    #now we loop counter clockwise to find the highest a value
    for i in range(-1,-len(a),-1):
        #print('a[i]'+str(a[i]))
        #print('i:'+str(i)+ '  highest a:'+str(a[highest_a_i]))
        newY=(yint(a[i], b[highest_b_i], mid_line, 0, 3000))[1]
        #print('old y:  '+str(y)+'  >     new y: '+str(newY))

        if(y > newY):
            #print('155 if ')
            highest_a_i=i
        else:
            #print('157  break')
            break
        y = newY

    print('a:  '+str(a))
    print('highest_a:  '+ str(a[highest_a_i]))
    print('\n')



    #now we have to find the lower tangent
    print('155***merge sort:now finding b lower')

    lowest_b_i=0
    lowest_a_i=0
    y= yint(a[0],b[0],mid_line,0,3000)[1]
    #this we check iterate b counter clockwise
    for i in range(-1,-len(b),-1):


        newY = yint(a[0], b[i], mid_line, 0, 3000)[1]
       # print('old y:  ' + str(y) + '  >     new y: ' + str(newY))
        if (y <newY):
            lowest_b_i = i
        else:
         #   print('167 break at '+str(i))
            break # else break

        y= newY

    print('b :'+str(b))
    print('lowest b point: '+ str(b[lowest_b_i])+'\n')


    print('196***merge: finding lowest a')
    for i in range(1, len(a), 1):
        newY=(yint(a[i], b[lowest_b_i], mid_line, 0, 3000))[1]
        print('old y:  ' + str(y) + '  >     new y: ' + str(newY))
        if (y < newY ):
            print('133 if statment true     i='+str(i))
            lowest_a_i = i
        else:
            print('199 else statement true')
            break  # else break
        y = newY

    print('a :'+str(a))
    print('lowest a point: '+ str(a[lowest_a_i])+'\n')

    print('\n\n\n')


    highest_a=a[highest_a_i]
    highest_b=b[highest_b_i]
    lowest_a=a[lowest_a_i]
    lowest_b=b[lowest_b_i]
    print('highest a: '+str(highest_a))
    print('lowest  a: '+str(lowest_a))
    print('highest b: '+str(highest_b))
    print('lowest b : '+str(lowest_b))


    print('****trying to splice lists****')
   # print('a before:  :'+str(a)+'  b before:  '+str(b))
    while(a[0]!=highest_a):
        a=rotate(a,1)

    while(b[0]!=lowest_b):
        b=rotate(b,1)
    print('a after rotate:  '+str(a) +'\nb after rotate: '+str(b))

   # newA=a[0]
   # print('newA: '+str(newA))
   # for i in range(len(a)):z







    print('232 lowest a'+str(lowest_a))

    if(lowest_a==highest_a):
        a=[highest_a]
    else:
        a= a[a.index(lowest_a):len(a)]
        a.insert(0,highest_a)


    print(a)

    print('b before:  '+str(b)+'  b lowest before: '+str(lowest_b_i))



    if(lowest_b==highest_b):
        b=[highest_b]
    else:

        b=b[b.index(highest_b):]
        b.insert(0,lowest_b)

    #print('b after :' + str(b))
    print('a+b merged: '+str(a+b)+'\n\n\n')
    return a+b


def computeHull(points):

    #if the hull is only 3 points return the list
    if(len(points)<4):
        print("compute hull called, basecase ")
        print(points)
        print()

        (points)
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

        print(a)
        print(b)
        print('**')



        #get the sublists into covex hulls
        a = computeHull(a)
        b = computeHull(b)

        newPoints= mergeWhile(a,b)

        clockwiseSort(newPoints)
    return newPoints


