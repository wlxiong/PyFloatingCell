# Match handover sequence
#
# Usage:
#       python match_path.py sample_file coord_x_file coord_y_file inquiry_file
#
# Outputs:
#       1) One output (the match result) is a csv file whose name consists of the string 
#       "inquiry_file" and a suffix "_matched". 
#       2) Another output (the handover graph) is a csv file whose name consists of the string
#       "sample_file" and a suffix "_graph". 
# Arguments:
#       1) "sample_file" is a csv file including the samples for calibrating the handover positions. 
#       2) "coord_x_file" and "coord_y_file" are csv files including the coordinations of handovers. 
#       3) "inquiry_file" is a csv file including sequences of handover inquiries. 
# 
# Input file sample 1 (sample_file):
# | 12 | 13 | 15 | 18 | 19 | 21 | 24 | 28 | 32 | 31 | 33 | 31 | 33 | 34 |  1 | 34 |  1 |  0 |  0 |  0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
# | 12 | 13 | 15 | 18 | 19 | 22 | 19 | 21 | 24 | 28 | 32 | 31 | 33 | 31 | 33 | 34 |  1 |  0 |  0 |  0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
# | 12 | 13 | 15 | 18 | 19 | 21 | 24 | 28 | 32 | 31 | 34 |  1 |  0 |  0 |  0 |  0 |  0 |  0 |  0 |  0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
# | 12 | 13 | 16 | 15 | 18 | 19 | 21 | 24 | 28 | 32 | 31 | 33 | 31 | 33 | 34 |  1 |  0 |  0 |  0 |  0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
# | 12 | 13 | 15 | 18 | 19 | 21 | 24 | 28 | 32 | 31 | 33 | 34 |  1 |  0 |  0 |  0 |  0 |  0 |  0 |  0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
# ...
# 
# Input file sample 2 (coord_x_file):
# |  11361.2958 | 10441.13209 | 9038.550444 | 7433.826953 | 5306.411997 | 4031.877606 | 3015.403424 |  2261.01044 |  1574.87707 | 996.5322182 |  909.091449 | 918.6788013 | 922.8524701 | 1047.146769 | 1065.977775 | 1144.883036 |    1837.944 |           0 |           0 |           0 |        0 | 0 | 0 | 0 | 0 | 0 | 0 |
# | 11456.06932 | 10441.13209 | 9088.793015 | 7183.158421 | 5518.165729 | 5433.464235 | 5348.762744 | 3942.165648 |  3166.26764 | 2311.301632 | 1399.088826 | 1058.058429 | 936.4792633 | 906.2985263 | 922.8524701 | 1056.767075 |    1837.944 |           0 |           0 |           0 |        0 | 0 | 0 | 0 | 0 | 0 | 0 |
# | 11456.06932 | 10441.13209 | 8988.307873 | 7534.094366 | 5306.411997 | 4031.877606 | 3015.403424 | 2411.884016 | 1484.642484 | 922.8524701 | 1056.767075 |    1837.944 |           0 |           0 |           0 |           0 |           0 |           0 |           0 |           0 |        0 | 0 | 0 | 0 | 0 | 0 | 0 |
# | 11408.68256 | 10491.27149 | 10390.99269 | 9038.550444 | 7333.559543 | 5306.411997 | 4116.948291 | 3065.691494 |  2261.01044 | 1484.642484 | 1034.957086 | 927.0384723 | 914.5051328 | 922.8524701 | 1065.977775 |    1837.944 |           0 |           0 |           0 |           0 |        0 | 0 | 0 | 0 | 0 | 0 | 0 |
# |  11361.2958 | 10441.13209 | 9088.793015 | 7333.559543 | 5348.762744 | 4031.877606 | 3115.979565 | 2562.779297 | 1399.088826 | 907.6949877 | 914.5051328 | 1053.560306 |    1837.944 |           0 |           0 |           0 |           0 |           0 |           0 |           0 |        0 | 0 | 0 | 0 | 0 | 0 | 0 |
# ...
# 
# Input file sample 3 (coord_y_file):
# | 5581.750389 | 5381.705546 | 5453.714123 | 5419.000859 | 6403.423414 |  7207.56647 | 7430.738463 | 7422.588111 | 7519.740005 | 8113.935816 | 8451.492638 | 8853.183782 | 8903.302299 | 11158.32086 | 11358.10075 | 11647.88707 |  12889.3824 |           0 |           0 |           0 |          0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
# | 5615.441926 | 5381.705546 | 5451.484928 |  5399.06551 | 6267.804501 | 6322.052064 |  6376.29963 | 7253.051691 | 7432.624264 | 7422.873209 | 7614.893987 | 7976.843201 | 8304.282812 | 8552.037856 | 8903.302299 | 11308.88984 |  12889.3824 |           0 |           0 |           0 |          0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
# | 5615.441926 | 5381.705546 | 5455.943314 | 5426.974997 | 6403.423414 |  7207.56647 | 7430.738463 | 7423.443405 |  7564.17941 | 8903.302299 | 11308.88984 |  12889.3824 |           0 |           0 |           0 |           0 |           0 |           0 |           0 |           0 |          0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
# | 5598.596158 | 5377.790759 | 5385.620337 | 5453.714123 | 5411.026718 | 6403.423414 | 7155.921164 | 7431.367065 | 7422.588111 |  7564.17941 | 8020.980609 | 8353.680755 | 8803.065265 | 8903.302299 | 11358.10075 |  12889.3824 |           0 |           0 |           0 |           0 |          0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
# | 5581.750389 | 5381.705546 | 5451.484928 | 5411.026718 |  6376.29963 |  7207.56647 | 7431.995666 | 7424.728103 | 7614.893987 | 8501.765247 | 8803.065265 | 11258.70018 |  12889.3824 |           0 |           0 |           0 |           0 |           0 |           0 |           0 |          0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
# ...
# 
# Input file sample 4 (inquiry_file):
# | GLOBALVEHICLEID | Handoff_sequence |    |    |    |   |
# |-----------------|------------------|----|----|----|---|
# |             257 |               34 |  0 |  0 |  0 |   |
# |             425 |               15 | 18 | 19 |  0 | 0 |
# |             446 |               19 | 21 | 24 | 32 | 0 |
# |             473 |               34 |  2 |  0 |  0 |   |
# |             624 |               34 |  0 |  0 |    |   |
# |            1119 |               33 | 34 |  1 |  0 |   |
# |            1177 |               32 | 31 |  0 |  0 |   |
# |            1280 |               13 |  0 |  0 |  0 |   |
# |            1514 |               21 | 28 | 32 | 31 | 0 |
# |            1564 |               13 | 15 | 18 |  0 | 0 |
# ... 
# 
# Output file sample 1 (_matched):
# | GLOBALVEHICLEID | FROM_NODE | TO_NODE |       COORD_X |       COORD_Y |
# |-----------------|-----------|---------|---------------|---------------|
# |             --- |       --- |     --- |           --- |           --- |
# |             425 |      15_1 |    18_1 | 9074.78610441 | 5452.10665094 |
# |             425 |      18_1 |    19_1 | 7317.96882883 | 5410.08811921 |
# |             --- |       --- |     --- |           --- |           --- |
# |             446 |      19_1 |    21_1 | 5381.50354186 | 6355.38893762 |
# |             446 |      21_1 |    24_1 | 4039.41076997 |  7201.2591223 |
# |             446 |      24_1 |    32_1 |            -1 |            -1 |
# |             --- |       --- |     --- |           --- |           --- |
# |             473 |      34_1 |     2_1 |            -1 |            -1 |
# ...
# 
# Output file sample 2 (_graph):
# | FROM_NODE | TO_NODE | WEIGHT |       COORD_X |       COORD_Y |
# |-----------|---------|--------|---------------|---------------|
# |      12_1 |    13_1 |     97 | 11367.8162044 | 5584.33715087 |
# |      12_1 |    14_1 |      2 |   11409.00318 |    5598.97749 |
# |      12_2 |    13_2 |      5 |  11295.297412 |  5558.7422716 |
# |      13_1 |    12_2 |      5 |  11418.308992 |   5602.058663 |
# |      13_1 |    15_1 |     89 | 10453.2846373 | 5382.47014713 |
# |      13_1 |    16_1 |      5 |  10540.803624 |  5377.4097384 |
# |      13_2 |    15_1 |      5 |  10381.083512 |    5386.37797 |
# |      14_1 |    13_1 |      2 |   11361.56434 |   5582.279671 |
# |      15_1 |    16_1 |      1 |   10491.27149 |   5377.790759 |
# |      15_1 |    16_2 |      1 |   9340.005871 |   5440.338965 |
# |      15_1 |    18_1 |     97 | 9074.78610441 | 5452.10665094 |
# ...
# 
#  match_path.py
#  PyFloatingCell 
#  
#  Created by Xiong Yiliang on 2011-05-29.
#  Copyright 2011 Xiong Yiliang. All rights reserved.
# 

import os
import csv

nodes = { }
edges = { }

def get_node(name):
    " Return the node with the given name, creating it if necessary. "
    if name in nodes:
        node = nodes[name]
    else:
        node = nodes[name] = Node(name)
    return node

def get_edge(name1, name2):
    " Return the node with the given endpoints, creating it if necessary. "
    edge_name = name1 + name2
    if edge_name in edges:
        edge = edges[edge_name]
    else:
        edge = edges[edge_name] = Edge(name1, name2)
    return edge

def create_csv_reader(filepath):
    csv_file = open(filepath, 'rU')
    csv_reader = csv.reader(csv_file)
    # if the first row is heading, skip it
    if csv.Sniffer().has_header( csv_file.read(1) ):
        csv_reader.next()
    return csv_reader

def read_inquiries(csv_reader):
    " read the inquiries from csv file"
    inquiries = [] 
    for line in csv_reader:
        line = [int(node) for node in line if node.isdigit()]
        inquiries.append( ( line[0], line[1:] ) )
    return inquiries

def read_handovers(csv_reader):
    " read the records from csv file"
    lines = []
    for line in csv_reader:
        lines.append( [int(node) for node in line if node.isdigit()] )
    return lines

def read_coordinations(csv_reader):
    " read the records from csv file" 
    lines = []
    for line in csv_reader:
        lines.append( [float(coord) for coord in line] )
    return lines

def write_matched_inquiries(match_tab, csv_writer):
    " write the results of the inquiries"
    # 'GLOBALVEHICLEID', 'FROM_NODE', 'TO_NODE', 'COORD_X', 'COORD_Y'
    csv_writer.writerow(['GLOBALVEHICLEID', 'FROM_NODE', 'TO_NODE', 'COORD_X', 'COORD_Y'])
    for vehicle_ID, matched_handovers in match_tab:
        for edge in matched_handovers:
            # print ( edge.nodes[0].name, edge.nodes[1].name ) + edge.estimated_coord
            csv_writer.writerow( ( vehicle_ID, 
                                   edge.nodes[0].name, 
                                   edge.nodes[1].name ) + \
                                   edge.avg_handover_coord() )
        csv_writer.writerow( ['---', '---', '---', '---', '---'] ) 

def write_handover_graph(csv_writer):
    " write the handover graph to a csv file"
    csv_writer.writerow(['FROM_NODE', 'TO_NODE', 'WEIGHT', 'COORD_X', 'COORD_Y'])
    edge_list = sorted(list(edges))
    for edge_name in edge_list:
        csv_writer.writerow( ( edges[edge_name].nodes[0].name, \
                               edges[edge_name].nodes[1].name, \
                               edges[edge_name].get_link_weight() ) + \
                               edges[edge_name].avg_handover_coord() )
        #print ( ( edges[edge_name].nodes[0].name, \
                   #edges[edge_name].nodes[1].name, \
                   #edge_name, hash(edge_name) ) )

class Node(object):
    " A node has a name and a list of edges emanating from it. "
    
    def __init__(self, name):
        self.name = name
        self.edgelist = [ ]

class Edge(object):
    " An edge connects two nodes. "

    def __init__(self, name1, name2):
        self.nodes = get_node(name1), get_node(name2)
        for n in self.nodes:
            n.edgelist.append(self)
        self.handover_coord = [ ]
        self.estimated_coord = None

    def __repr__(self):
        return self.nodes[0].name + ',' + self.nodes[1].name

    def add_handover_coord(self, x, y):
        self.handover_coord.append( (x,y) )

    def avg_handover_coord(self):
        if self.estimated_coord <> None:
            return self.estimated_coord
        sum_x = sum(x for x, y in self.handover_coord)
        sum_y = sum(y for x, y in self.handover_coord)
        leng = len(self.handover_coord)
        if leng == 0:
            return (-1, -1)
        self.estimated_coord = (sum_x/leng, sum_y/leng) 
        return self.estimated_coord

    def get_link_weight(self):
        return len(self.handover_coord)

def ren_handover_seq(handover_seq):
    " rename the node in each handover: name_#(times of visiting node)"
    renamed_seq = [ ]
    for i, node in enumerate(handover_seq):
        if node <> 0:
            renamed_seq.append(str(node) + '_' + str( handover_seq[:i+1].count(node) ) )
    # print renamed_seq
    return renamed_seq

def gen_handover_graph(sample_tab, handover_x, handover_y):
    for i, handover_seq in enumerate(sample_tab):
        renamed_seq = ren_handover_seq(handover_seq)
        # generate handover graph and add the handover coordinations 
        sequences = zip(renamed_seq[:-1], renamed_seq[1:], handover_x[i], handover_y[i])
        for this_node, next_node, x, y in sequences:
            edge = get_edge(this_node, next_node)
            edge.add_handover_coord(x,y)

def match_handover_seq(handover_seq):
    matched_handovers = [ ]
    renamed_seq = ren_handover_seq(handover_seq)
    for this_node, next_node in zip(renamed_seq[:-1], renamed_seq[1:]):
        edge_name = this_node + next_node
        if edge_name in edges:
            matched_handovers.append( edges[edge_name] )
        else:
            matched_handovers.append( Edge(this_node, next_node) )
    return matched_handovers

def process_inquries(inquiry_tab):
    match_tab = [ ]
    for vehicle_ID, sequence in inquiry_tab:
        matched_seq = match_handover_seq(sequence)
        match_tab.append( (vehicle_ID, matched_seq) )
    return match_tab

def main(argv=None):
    if argv is None:
        argv = sys.argv
    try:
        sample_filename = argv[1]
        coord_x_filename = argv[2] 
        coord_y_filename = argv[3]
        inquiry_filename = argv[4]
    except:
        raise Exception(' four files must be input: \
                handover records, x and y coordinations and match inquiries')
    
    # read samples and inquiries
    sample_reader = create_csv_reader(sample_filename)
    coord_x_reader = create_csv_reader(coord_x_filename)
    coord_y_reader = create_csv_reader(coord_y_filename)
    inquiry_reader = create_csv_reader(inquiry_filename)

    sample_tab = read_handovers(sample_reader)
    coord_x = read_coordinations(coord_x_reader)
    coord_y = read_coordinations(coord_y_reader)
    inquiry_tab = read_inquiries(inquiry_reader)

    # generate the handover graph
    gen_handover_graph(sample_tab, coord_x, coord_y)

    # process the inquiries
    match_tab = process_inquries(inquiry_tab)

    # write matched handovers
    (shortname, extension) = os.path.splitext(inquiry_filename)
    match_writer = csv.writer(open(shortname+'_matched.csv', 'wb'))
    write_matched_inquiries(match_tab, match_writer)

    # write the handover graph
    (shortname, extension) = os.path.splitext(sample_filename)
    graph_writer = csv.writer(open(shortname+'_graph.csv', 'wb'))
    write_handover_graph(graph_writer)


if __name__ == "__main__":
    import sys
    sys.exit(main())
