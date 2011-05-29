# Interpolate points for each link
# 
# Usage: 
#       python interp_link.py [directory_of_node_files] [step]
# 
# Outputs: 
#       All the csv files under "directory_of_node_files" will be processed, 
#       and the corresponding output files with the same file names are saved 
#       in a subdirectory named "interpolated_step". 
# 
# Arguments:
#       1) "directory_of_node_files" is the directory under which the coordinations of end nodes 
#       of each road are saved. If the argument "directory_of_input_files" is no provided, 
#       the current working directory is used as the default one. 
#       2) "step" is the interpolation step. If "step" is no provided, 
#       the default value is 10. 
# 
# Input file sample: 
# | NODE_ID | NODE_X | NODE_Y | NODE_Length |
# |---------|--------|--------|-------------|
# |    8037 |  29409 |  18187 | 73.10950691 |
# |     182 |  29413 |  18114 | 127.2792206 |
# |      10 |  29395 |  17988 | 253.0019763 |
# |     183 |  29318 |  17747 | 119.4194289 |
# |    8038 |  29308 |  17628 |             |
# |         |        |  total | 572.8101327 |
# |      13 |  27571 |  17926 | 300.8853602 |
# |      14 |  27865 |  17862 | 236.0381325 |
# |      11 |  28070 |  17745 | 105.6503668 |
# |    8056 |  28171 |  17714 |             |
# |         |        |  total | 642.5738595 |
# ...
#
# Output file sample:
# | NODE_ID |        NODE_X |        NODE_Y |      DISTANCE |       MILEAGE |
# |---------|---------------|---------------|---------------|---------------|
# |    8037 |         29409 |         18187 |           0.0 |           0.0 |
# | 8037001 | 29410.0942489 |  18167.029957 |            20 |          20.0 |
# | 8037002 | 29411.1884979 | 18147.0599139 |            20 |          40.0 |
# | 8037003 | 29412.2827468 | 18127.0898709 |            20 |          60.0 |
# |     182 |         29413 |         18114 | 13.1095069057 | 73.1095069057 |
# |  182001 | 29410.1715729 | 18094.2010101 |            20 | 93.1095069057 |
# |  182002 | 29407.3431458 | 18074.4020203 |            20 | 113.109506906 |
# |  182003 | 29404.5147186 | 18054.6030304 |            20 | 133.109506906 |
# |  182004 | 29401.6862915 | 18034.8040405 |            20 | 153.109506906 |
# |  182005 | 29398.8578644 | 18015.0050506 |            20 | 173.109506906 |
# |  182006 | 29396.0294373 | 17995.2060608 |            20 | 193.109506906 |
# |      10 |         29395 |         17988 | 7.27922061358 | 200.388727519 |
# ...
# 
#  interp_link.py
#  PyFloatingCell
#  
#  Created by Xiong Yiliang on 2011-05-29.
#  Copyright 2011 Xiong Yiliang. All rights reserved.
# 

import os
import csv
import math

def create_csv_reader(filepath):
    csv_file = open(filepath, 'rU')
    csv_reader = csv.reader(csv_file)
    # if the first row is heading, skip it
    if csv.Sniffer().has_header( csv_file.read(1) ):
        csv_reader.next()
    return csv_reader

def read_nodes(csv_reader):
    nodes = []
    # extract information from csv file
    for node in csv_reader:
        # NODE_ID, NODE_X, NODE_Y
        i, x, y = node[0], node[1], node[2]
        if i <> '':
            # if this row is not a node record, skip it 
            nodes.append( ( int(i), int(x), int(y) ) )
        # else:
        #     # 'total', num
        #     nodes.append( ( None, node[2], float(node[3]) ) )
    return nodes

def write_points(csv_writer, points):
    # 'NODE_ID', 'NODE_X', 'NODE_Y', 'DISTANCE', 'MILEAGE'
    csv_writer.writerow(['NODE_ID', 'NODE_X', 'NODE_Y', 'DISTANCE', 'MILEAGE'])
    csv_writer.writerows(points)

def linear_interpolate(nodes, interp_step):
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

def main(argv=None):
    if argv is None:
        argv = sys.argv
    try:
        working_dir = argv[1]
    except:
        working_dir = './'
    try:
        if argv[2].isdigit():
            interp_step = int(argv[2])
        else:
            interp_step = 10
            print "default step %d" % interp_step
    except:
        interp_step = 10
        print "default step %d" % interp_step

    # name of directory for output files
    sub_dir = 'interpolated_'+str(interp_step)
    output_dir = os.path.join(working_dir, sub_dir)
    # check if interpolated subdir exists
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    # process the data
    for each_file_name in os.listdir(working_dir):
        (shortname, extension) = os.path.splitext(each_file_name)
        if extension <> '.csv':
            continue
        print 'processing ' + shortname
        # read data
        node_reader = create_csv_reader(os.path.join(working_dir, each_file_name))
        node_list = read_nodes(node_reader)
        # print 'read_nodes(node_reader)'
        # interpolate links
        point_list = linear_interpolate(node_list, interp_step)
        # print 'linear_interpolate(node_list)'
        # write results
        node_writer = csv.writer(open( os.path.join(output_dir, each_file_name), 'wb' ) )
        write_points(node_writer, point_list)
        # print 'write_points(node_writer, point_list)'

if __name__ == "__main__":
    import sys
    sys.exit(main())
