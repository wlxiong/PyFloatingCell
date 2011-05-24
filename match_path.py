import csv
import os

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
    for inquiry in inquiry_tab:
        match_tab.append(match_handover_seq(inquiry))
    return match_tab

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
    # 'FROM_NODE', 'TO_NODE', 'COORD_X', 'COORD_Y'
    csv_writer.writerow(['FROM_NODE', 'TO_NODE', 'COORD_X', 'COORD_Y'])
    for matched_handovers in match_tab:
        for edge in matched_handovers:
            # print ( edge.nodes[0].name, edge.nodes[1].name ) + edge.estimated_coord
            csv_writer.writerow( (  edge.nodes[0].name, edge.nodes[1].name ) + \
                                    edge.avg_handover_coord() )
        csv_writer.writerow( ['---', '---', '---', '---'] ) 

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
    sample_reader = csv.reader(open(sample_filename, 'rU'))
    coord_x_reader = csv.reader(open(coord_x_filename, 'rU'))
    coord_y_reader = csv.reader(open(coord_y_filename, 'rU'))
    inquiry_reader = csv.reader(open(inquiry_filename, 'rU'))

    sample_tab = read_handovers(sample_reader)
    coord_x = read_coordinations(coord_x_reader)
    coord_y = read_coordinations(coord_y_reader)
    inquiry_tab = read_handovers(inquiry_reader)

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
