# Extract vehicle tracks from the full vehicle records
# 
# Usage:
#       python extract_tracks.py vehicle_record_file road_link_file
#
# Outputs:
#       The output is a csv file whose name consists of the string 
#       "vehicle_record_file" and a suffix "_sampled". 
# 
# Arguments:
#       1) "vehicle_record_file" is a csv file containing a set of vehicle records. 
#       2) "road_link_file" is a csv file defining the nodes on a road. 
# 
# Input file sample 1 (vehicle_record_file): 
# | SIMULATIONTIME | UPNODE | DOWNNODE | GLOBALVEHICLEID | FLEET | VEHICLETYPE | VEHICLELENGTH | DRIVERTYPE | LANEID | VEHICLEPOSITION | PREVIOUSUSN | TURNCODE | QUEUESTATUS | ACCELERATION | VELOCITY | LANECHANGESTATUS | TARGETLANE | DESTINATIONNODE | LEADERVEHICLEID | FOLLOWERVEHICLEID | PREVIOUSLANEID | LINKID | UPNODEX | UPNODEY | DOWNNODEX | DOWNNODEY |  VEHICLE_X |  VEHICLE_Y |
# |----------------|--------|----------|-----------------|-------|-------------|---------------|------------|--------|-----------------|-------------|----------|-------------|--------------|----------|------------------|------------|-----------------|-----------------|-------------------|----------------|--------|---------|---------|-----------|-----------|------------|------------|
# |              0 |     53 |       42 |             148 |     0 |           1 |            16 |          3 |      4 |             249 |          56 |        1 |           0 |            0 |       34 |                0 |          0 |               0 |             662 |               234 |              2 | 530042 |   17141 |   21130 |     16434 |     21882 |  16970.442 | 21311.4138 |
# |              1 |     53 |       42 |             148 |     0 |           1 |            16 |          3 |      4 |             283 |          56 |        1 |           0 |            0 |       34 |                0 |          0 |               0 |             662 |               234 |              2 | 530042 |   17141 |   21130 |     16434 |     21882 |  16947.153 | 21336.1852 |
# |              2 |     53 |       42 |             148 |     0 |           1 |            16 |          3 |      4 |             317 |          56 |        1 |           0 |            0 |       34 |                0 |          0 |               0 |             662 |               234 |              2 | 530042 |   17141 |   21130 |     16434 |     21882 |  16923.864 | 21360.9566 |
# |              3 |     53 |       42 |             148 |     0 |           1 |            16 |          3 |      4 |             351 |          56 |        1 |           0 |            0 |       34 |                0 |          0 |               0 |             662 |               234 |              2 | 530042 |   17141 |   21130 |     16434 |     21882 | 16900.5749 | 21385.7279 |
# |              4 |     53 |       42 |             148 |     0 |           1 |            16 |          3 |      4 |             385 |          56 |        1 |           0 |            0 |       34 |                0 |          0 |               0 |             662 |               234 |              2 | 530042 |   17141 |   21130 |     16434 |     21882 | 16877.2859 | 21410.4993 |
# ...
#
# Input file sample 2 (road_link_file): 
# |  Link_ID | Up_Node | Down_Node | Up_Node_X | Up_Node_Y | Down_Node_X | Down_Node_Y |
# |----------|---------|-----------|-----------|-----------|-------------|-------------|
# | 8013_195 |    8013 |       195 |     45185 |     20926 |       45047 |       20913 |
# |  195_227 |     195 |       227 |     45047 |     20913 |       44277 |       20857 |
# |  227_194 |     227 |       194 |     44277 |     20857 |       43598 |       20806 |
# |  194_189 |     194 |       189 |     43598 |     20806 |       43307 |       20735 |
# ...
# 
# Output file sample:
# | GLOBALVEHICLEID | SIMULATIONTIME | UPNODE | DOWNNODE |   LINKID |  VEHICLE_X |  VEHICLE_Y | VELOCITY |
# |-----------------|----------------|--------|----------|----------|------------|------------|----------|
# |             412 |              0 |    127 |      160 |  1270160 |  4795.2054 | 40206.0577 |       96 |
# |             412 |              1 |    127 |      160 |  1270160 |  4845.3777 | 40289.0742 |       97 |
# |             412 |              2 |    127 |      160 |  1270160 |    4895.55 | 40372.0907 |       96 |
# |            1172 |             90 |      3 |        4 |    30004 | 28096.1544 | 17959.0966 |       99 |
# ...
# 
#  extract_tracks.py
#  PyFloatingCell
#  
#  Created by Xiong Yiliang on 2011-05-29.
#  Copyright 2011 Xiong Yiliang. All rights reserved.
# 

import os
import csv
from random import sample
from random import randint

sample_rate_tests = [.02]
sample_interval_tests = [(120, 180)]

def create_csv_reader(filepath):
    csv_file = open(filepath, 'rU')
    csv_reader = csv.reader(csv_file)
    # if the first row is heading, skip it
    if csv.Sniffer().has_header( csv_file.read(1) ):
        csv_reader.next()
    return csv_reader

def read_records(csv_reader):
    vehicle_records = []
    # vehicle_IDs = set()
    # extract information from csv file
    for record in csv_reader:
        # vehicle ID, upnode, downnode, simulaiton time, link ID, coord_x, coord_y, speed 
        t, p, q, h, l, x, y, v = \
            record[0], record[1], record[2], record[3], record[21], record[26], record[27], record[14]
        vehicle_records.append((int(h),int(t),p,q,l,x,y,v))
        # vehicle_IDs.add(int(h))
    # vehicle_list = sorted(list(vehicle_IDs))
    # return vehicle_list, vehicle_records
    return vehicle_records

def read_links(csv_reader):
    road_links = {}
    # read links and corrsponding nodes from csv file
    for link in csv_reader:
        # link ID, upnode, downnode
        l, p, q = link[0], link[1], link[2]
        road_links[(p,q)] = l
    return road_links

def write_records(csv_writer, sampled_tracks):
    # vehicle ID, simulaiton time, link ID, coord_x, coord_y, speed 
    csv_writer.writerow(['GLOBALVEHICLEID', 'SIMULATIONTIME', 
        'UPNODE', 'DOWNNODE', 'LINKID', 'VEHICLE_X', 'VEHICLE_Y', 'VELOCITY'])
    csv_writer.writerows(sampled_tracks)

def sample_vehicles(vehicle_records, road_links, sample_interval, sample_rate):
    vehicle_set = set()
    entering_time = {}
    leaving_time = {}
    for record in vehicle_records:
        vehicle_ID = record[0]
        time_record = record[1]
        upnode = record[2]
        downnode = record[3]
        if (upnode, downnode) in road_links:
            # select vehicles riding on the specific road links
            vehicle_set.add(vehicle_ID)
            # find the entering time and leaving time for each vehicle 
            if vehicle_ID not in entering_time or entering_time[vehicle_ID] > time_record:
                entering_time[vehicle_ID] = time_record
            if vehicle_ID not in leaving_time or leaving_time[vehicle_ID] < time_record:
                leaving_time[vehicle_ID] = time_record
    for vehicle_ID in list(vehicle_set):
        if leaving_time[vehicle_ID] - entering_time[vehicle_ID] < sample_interval[0]:
            # skip the vehicle with insufficient duration 
            vehicle_set.remove(vehicle_ID)
    # generate the vehicle IDs with the given sample rate
    num_vehicle = len(vehicle_set)
    sampled_vehicles = set(sample(list(vehicle_set), int(sample_rate * num_vehicle)))
    # select the records of sampled vehicles
    sampled_records = []
    for record in vehicle_records:
        if record[0] in sampled_vehicles:
            sampled_records.append(record)
    # sort the records according to vehicle ID and simulation time
    sampled_records.sort()
    return sampled_vehicles, sampled_records, entering_time, leaving_time, vehicle_set

def sample_records(vehicle_set, vehicle_records, entering_time, leaving_time, sample_interval):
    # generate a random calling duration for each vehicle
    calling_duration = {}
    for vehicle_ID in vehicle_set:
        calling_duration[vehicle_ID] = randint(sample_interval[0], sample_interval[1])
    # calculate the start and end of each phone call
    calling_start = {}
    calling_end = {}
    for vehicle_ID in vehicle_set:
        # center the calling duration in the time window
        calling_start[vehicle_ID] = (entering_time[vehicle_ID] + leaving_time[vehicle_ID]) // 2 - \
                                    calling_duration[vehicle_ID] // 2
        calling_end[vehicle_ID] = calling_start[vehicle_ID] + calling_duration[vehicle_ID] - 1
    # extract the records within the calling interval 
    sampled_records = []
    for record in vehicle_records:
        vehicle_ID = record[0]
        time_record = record[1]
        if calling_start[vehicle_ID] <= time_record <= calling_end[vehicle_ID]:
            sampled_records.append(record)
    return sampled_records, calling_start, calling_end

def main(argv=None):
    if argv is None:
        argv = sys.argv
    try:
        record_filename = argv[1]
        link_filename = argv[2]
    except:
        sys.stderr.write(' at least two files should be provided')

    # read data
    record_reader = create_csv_reader(record_filename)
    vehicle_records = read_records(record_reader)
    link_reader = create_csv_reader(link_filename)
    link_list = read_links(link_reader)
    # sampling process
    for sample_rate in sample_rate_tests:
        for sample_interval in sample_interval_tests:
            print '\n====================='
            sampled_vehicles, sampled_records, entering_time, leaving_time, vehicle_set = \
                sample_vehicles(vehicle_records, link_list, sample_interval, sample_rate)
            print ' sample_vehicles()'
            sampled_records, calling_start, calling_end = \
                sample_records(sampled_vehicles, sampled_records, entering_time, leaving_time, sample_interval)
            print ' sample_records()'
            
            print '\n---------------------'
            print " sample_rate = %f, sample_interval = %s" % ( sample_rate, sample_interval )
            print " no. of vehicles in time interval %s: %d" % ( sample_interval, len(vehicle_set) )
            print " no. of sampled vehicles: %d x %f = %d" % ( len(vehicle_set), sample_rate, len(sampled_vehicles) )
            print " no. of sampled records:  %d" % len(sampled_records)
            
            print '\n---------------------'
            print " sampled_vehicles:\n (ID, starting time, ending time, duration)"
            for vehicle_ID in sorted(list(sampled_vehicles)):
                print " %s\t %d\t %d\t %d" % ( vehicle_ID, calling_start[vehicle_ID], calling_end[vehicle_ID], 
                                               calling_end[vehicle_ID] - calling_start[vehicle_ID] )
            # save the sampled records 
            (shortname, extension) = os.path.splitext(record_filename)
            track_writer = csv.writer(open(shortname+'_sampled_'+\
                str(sample_rate)+'_'+str(sample_interval)+extension, 'wb'))
            write_records(track_writer, sampled_records)

if __name__ == "__main__":
    import sys
    sys.exit(main())
