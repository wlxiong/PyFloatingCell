# extract vehicle tracks from the full vehicle records
import csv
from random import sample
from random import randint

sample_rate = .02
sample_interval = (120, 180) 

def read_records(csv_reader):
    vehicle_records = []
    vehicle_IDs = set()
    # extract information from csv file
    for record in csv_reader:
        # vehicle ID, upnode, downnode, simulaiton time, link ID, coord_x, coord_y, speed 
        t, p, q, h, l, x, y, v = record[0], record[1], record[2], record[3], record[21], record[26], record[27], record[14]
        vehicle_records.append((int(h),int(t),l,x,y,v))
        vehicle_IDs.add(int(h))
    vehicle_list = sorted(list(vehicle_IDs))
    return vehicle_list, vehicle_records

def write_tracks(csv_writer, sampled_tracks):
    # vehicle ID, simulaiton time, link ID, coord_x, coord_y, speed 
    csv_writer.writerow(['GLOBALVEHICLEID', 'SIMULATIONTIME', 'LINKID', 'VEHICLE_X', 'VEHICLE_Y', 'VELOCITY'])
    csv_writer.writerows(sampled_tracks)
    
def sample_vehicles(vehicle_list, vehicle_records):
    num_vehicle = len(vehicle_list)
    sampled_index = sample(xrange(num_vehicle), int(sample_rate * num_vehicle))
    # generate the set of sampled vehicles
    sampled_vehicles = set([vehicle_list[i] for i in sampled_index])
    # select the records of sampled vehicles
    sampled_records = []
    for record in vehicle_records:
        if record[0] in sampled_vehicles:
            sampled_records.append(record)
    # sort the records according to vehicle ID and simulation time
    sampled_records.sort()
    return sampled_vehicles, sampled_records

def sample_tracks(vehicle_set, vehicle_records):
    # find the entering time and leaving time for each vehicle 
    entering_time = {}
    leaving_time = {}
    for record in vehicle_records:
        vehicle_ID = record[0]
        time_record = record[1]
        if vehicle_ID not in entering_time or entering_time[vehicle_ID] > time_record:
            entering_time[vehicle_ID] = time_record
        if vehicle_ID not in leaving_time or leaving_time[vehicle_ID] < time_record:
            leaving_time[vehicle_ID] = time_record
    # generate a random calling duration for each vehicle
    calling_duration = {}
    for vehicle_ID in vehicle_set:
        calling_duration[vehicle_ID] = randint(sample_interval[0], sample_interval[1])
    # calculate the start and end of each call
    calling_start = {}
    calling_end = {}
    for vehicle_ID in vehicle_set:
        if leaving_time[vehicle_ID] - entering_time[vehicle_ID] < calling_duration[vehicle_ID]:
            # extract all the time window of the vehicle 
            calling_start[vehicle_ID] = entering_time[vehicle_ID]
            calling_end[vehicle_ID] = leaving_time[vehicle_ID]
        else:
            # center the calling duration in the time window
            calling_start[vehicle_ID] = (entering_time[vehicle_ID] + leaving_time[vehicle_ID]) // 2 - \
                                        calling_duration[vehicle_ID] // 2
            calling_end[vehicle_ID] = calling_start[vehicle_ID] + calling_duration[vehicle_ID] - 1
    # extract the records within the calling interval 
    sampled_tracks = []
    for record in vehicle_records:
        vehicle_ID = record[0]
        time_record = record[1]
        if calling_start[vehicle_ID] <= time_record <= calling_end[vehicle_ID]:
            sampled_tracks.append(record)
    return sampled_tracks

def main(argv=None):
    if argv is None:
        argv = sys.argv
    for each_file_name in argv[1:]:
        record_reader = csv.reader(open(each_file_name, 'rb'))
        vehicle_list, vehicle_records = read_records(record_reader)
        print 'extract_fields(csv_file)'
        sampled_vehicles, sampled_records = sample_vehicles(vehicle_list, vehicle_records)
        print 'sample_vehicles(vehicle_list, vehicle_records)'
        sampled_tracks = sample_tracks(sampled_vehicles, sampled_records)
        print 'sample_tracks(sampled_vehicles, sampled_records)'
        print '---------------------'
        print sampled_vehicles
        print '---------------------'
        print len(sampled_vehicles)
        print len(sampled_records)
        print len(sampled_tracks)
        print '---------------------'
        track_writer = csv.writer(open('sampled_'+each_file_name, 'wb'))
        write_tracks(track_writer, sampled_tracks)

if __name__ == "__main__":
    import sys
    sys.exit(main())
