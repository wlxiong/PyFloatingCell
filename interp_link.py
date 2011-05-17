# interpolate points for each link
import os
import csv
import math

interp_step = 10 # unit: feet? 

def read_nodes(csv_reader):
    nodes = []
    # extract information from csv file
    csv_reader.next()
    for node in csv_reader:
        # NODE_ID, NODE_X, NODE_Y
        i, x, y = node[0], node[1], node[2]
        if i <> '':
            nodes.append( ( int(i), int(x), int(y) ) )
        # else:
        #     # 'total', num
        #     nodes.append( ( None, node[2], float(node[3]) ) )
    return nodes

def linear_interpolate(nodes):
    points = []
    n0 = nodes[0]
    mileage = 0.0
    points.append( (n0[0], n0[1], n0[2], 0.0, mileage) )
    for first, second in zip(nodes[:-1], nodes[1:]):
        i1, i2 = first[0], second[0]
        x1, x2 = first[1], second[1]
        y1, y2 = first[2], second[2]
        # if i1 == None or i2 == None:
        #     if points[-1][0] <> None:
        #         points.append(first)
        ii = i1 * 1000
        dx = x2 - x1
        dy = y2 - y1
        # calculate link length
        leng = math.sqrt(dx*dx + dy*dy)
        for step in xrange(interp_step, int(leng), interp_step):
            grad_x = (step / leng) * dx 
            grad_y = (step / leng) * dy
            point_x = grad_x + x1 
            point_y = grad_y + y1
            ii += 1
            points.append( ( ii, point_x, point_y, interp_step, mileage + step ) )
        points.append( ( i2, x2, y2, leng - step, mileage + leng ) )
        mileage += leng
    return points

def write_points(csv_writer, points):
    # 'NODE_ID', 'NODE_X', 'NODE_Y', 'DISTANCE', 'MILEAGE'
    csv_writer.writerow(['NODE_ID', 'NODE_X', 'NODE_Y', 'DISTANCE', 'MILEAGE'])
    csv_writer.writerows(points)

def main(argv=None):
    if argv is None:
        argv = sys.argv
    try:
        working_dir = argv[1]
    except:
        working_dir = './'
    # check if interpolated subdir exists
    d = os.path.dirname(working_dir+'interpolated/')
    if not os.path.exists(d):
        os.makedirs(d)
                
    for each_file_name in os.listdir(working_dir):
        (shortname, extension) = os.path.splitext(each_file_name)
        if extension <> '.csv':
            continue
        print 'processing ' + each_file_name
        
        node_reader = csv.reader(open(working_dir+each_file_name, 'rU'))
        node_list = read_nodes(node_reader)
        print 'read_nodes(node_reader)'
        
        point_list = linear_interpolate(node_list)
        print 'linear_interpolate(node_list)'
        
        node_writer = csv.writer(open(working_dir+'interpolated/'+each_file_name, 'wb'))
        write_points(node_writer, point_list)
        print 'write_points(node_writer, point_list)'

if __name__ == "__main__":
    import sys
    sys.exit(main())
