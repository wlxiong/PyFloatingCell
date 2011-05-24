import os
import csv

def read_records(csv_reader):
    vehicle_records = []
    # extract information from csv file
    for record in csv_reader:
        # GLOBALVEHICLEID, VEHICLE_X, VEHICLE_Y, UPNODE, DOWNNODE, 
        # SIMULATIONTIME, LINKID, Length, Handoff_Tag
        h, x, y, p, q, t, l, n, g = record[0], record[1], record[2], record[3], record[4], \
                                    record[5], record[6], record[7], record[8]
        if h.isdigit():
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
    record_reader = csv.reader(open(record_filename, 'rU'))
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
