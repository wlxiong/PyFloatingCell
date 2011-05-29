# Calculate real journey speed
# 
# Usage:
#       python calc_speed.py vehicle_record_file
#
# Outputs:
#       The output is a csv file whose name consists of the string 
#       "vehicle_record_file" and a suffix "_speed". 
# 
# Arguments: 
#       "vehicle_record_file" is a csv file containing a set of vehicle records. 
# 
# Input file sample:
# | GLOBALVEHICLEID |  VEHICLE_X |  VEHICLE_Y | UPNODE | DOWNNODE | SIMULATIONTIME |   LINKID |      Length | Handoff_Tag |
# |-----------------|------------|------------|--------|----------|----------------|----------|-------------|-------------|
# |             425 | 29332.3534 | 17907.0355 |    264 |        3 |             30 |  2640003 | 90.00005738 |           0 |
# |             425 | 29242.4418 | 17911.0248 |    264 |        3 |             31 |  2640003 |  88.9999713 |           1 |
# |             425 | 29153.5293 | 17914.9697 |    264 |        3 |             32 |  2640003 | 90.00005295 |           0 |
# ...
# |             425 | 22874.2628 | 17734.0031 |     21 |      199 |             96 |   210199 | 100.9999769 |           0 |
# |             425 |  22774.485 | 17749.6679 |     21 |      199 |             97 |   210199 | 101.4241947 |           1 |
# |             425 | 22678.9849 | 17783.8234 |    199 |       23 |             98 |  1990023 | 102.0000187 |           0 |
# ...
# 
# Output file sample:
# | GLOBALVEHICLEID |  VEHICLE_X |  VEHICLE_Y | UPNODE | DOWNNODE | SIMULATIONTIME |   LINKID |      Length | Handoff_Tag |       MILEAGE |      VELOCITY |
# |-----------------|------------|------------|--------|----------|----------------|----------|-------------|-------------|---------------|---------------|
# |             425 | 29242.4418 | 17911.0248 |    264 |        3 |             31 |  2640003 |  88.9999713 |           1 | 3073.83560296 |          -1.0 |
# |             425 |  22774.485 | 17749.6679 |     21 |      199 |             97 |   210199 | 101.4241947 |           1 | 9556.88310835 | 98.2279925059 |
# ...
# 
#  calc_speed.py
#  PyFloatingCell
#  
#  Created by Xiong Yiliang on 2011-05-29.
#  Copyright 2011 Xiong Yiliang. All rights reserved.
# 

import os
import csv

def create_csv_reader(filepath):
    csv_file = open(filepath, 'rU')
    csv_reader = csv.reader(csv_file)
    # if the first row is heading, skip it
    if csv.Sniffer().has_header( csv_file.read(1) ):
        csv_reader.next()
    return csv_reader

def read_records(csv_reader):
    vehicle_records = []
    # extract information from csv file
    for record in csv_reader:
        # GLOBALVEHICLEID, VEHICLE_X, VEHICLE_Y, UPNODE, DOWNNODE, 
        # SIMULATIONTIME, LINKID, Length, Handoff_Tag
        h, x, y, p, q, t, l, n, g = record[0], record[1], record[2], record[3], record[4], \
                                    record[5], record[6], record[7], record[8]
        vehicle_records.append( ( int(h), float(x), float(y), int(p), int(q), \
                                  int(t), int(l), float(n), int(g) ) )
    return vehicle_records

def write_speeds(csv_writer, speed_records):
    " write the calculated real vehicle speed"
    csv_writer.writerow( \
        ['GLOBALVEHICLEID', 'VEHICLE_X', 'VEHICLE_Y', 'UPNODE', 'DOWNNODE', \
         'SIMULATIONTIME', 'LINKID', 'Length', 'Handoff_Tag', 'MILEAGE', 'VELOCITY'])
    csv_writer.writerows(speed_records)

def calc_vehicle_mileage(vehicle_records):
    " calculate the real vehicle speed"
    mileage_records = []
    accumulate_leng = 0.0
    prev_vehicle = -1
    # calculate the mileage first
    for i in xrange(len(vehicle_records)):
        if prev_vehicle == vehicle_records[i][0]:
            accumulate_leng += vehicle_records[i-1][7]
        else:
            accumulate_leng = 0.0
            prev_vehicle = vehicle_records[i][0]
        # extract the records with tag equal to ONE
        if vehicle_records[i][8] == 1:
            mileage_records.append( vehicle_records[i] + (accumulate_leng,) )
    return mileage_records

def calc_vehicle_speed(mileage_records):
    # then calculate the speed
    speed_records = []
    prev_vehicle = -1
    for i in xrange(len(mileage_records)):
        if prev_vehicle == mileage_records[i][0]:
            # get the mileage and travel time
            prev_mileage = mileage_records[i-1][9]
            this_mileage = mileage_records[i][9]
            prev_time = mileage_records[i-1][5]
            this_time = mileage_records[i][5]
            speed = (this_mileage - prev_mileage) / (this_time - prev_time)
            speed_records.append( mileage_records[i] + (speed,) )
        else:
            prev_vehicle = mileage_records[i][0]
            speed_records.append( mileage_records[i] + (-1.0,) )
    return speed_records

def main(argv=None):
    if argv is None:
        argv = sys.argv
    try:
        record_filename = argv[1]
    except:
        sys.stderr.write(' no input file')

    # read data
    record_reader = create_csv_reader(record_filename)
    vehicle_records = read_records(record_reader)
    # calculate mileage
    mileage_records = calc_vehicle_mileage(vehicle_records)
    # calculate speed
    speed_records = calc_vehicle_speed(mileage_records)
    # write the speed
    (shortname, extension) = os.path.splitext(record_filename)
    speed_writer = csv.writer(open(shortname+'_speed'+extension, 'wb'))
    write_speeds(speed_writer, speed_records)
    
if __name__ == "__main__":
    import sys
    sys.exit(main())
