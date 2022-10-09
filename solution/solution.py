import os
import sys
import argparse
import csv
import time
import datetime
import json
import operator
from collections import deque

def inputs():
    # required args
    path = ""
    input_origin = ""
    input_destination = ""

    # optional args
    input_bags = 0

    is_return = False

    parser = argparse.ArgumentParser(description="Parser tutorial")
    parser.add_argument("--bags", default=0, type=int,
                        required=False, help="This is the number of bags")
    parser.add_argument("--return",dest = 'roundtrip', action='store', default=False,
                        nargs='?', required=False, help="This is the return flight option")
    parser.add_argument("--days", default=0, type=int, 
                        required=False, help="This is the number of days to spend on destination before the return flight")                    
    parser.add_argument("--exp", default="", type=str, nargs='*',
                        required=False, help="This is the option to save the json export")

    args, _ = parser.parse_known_args()

    # required args
    assert(sys.argv[1]), "Please provide path, origin and destination"
    path = sys.argv[1]
    is_exist = os.path.exists(path)

    assert(is_exist), "Provided path to csv is not valid"

    assert(sys.argv[2]), "Please provide both, origin and destination"
    input_origin = sys.argv[2]

    assert(sys.argv[3]), "Please provide both, origin and destination"
    input_destination = sys.argv[3]

    # optional args
    input_bags = args.bags
    days = args.days
    print(days)    

    if args.roundtrip is None:
        is_return = True
    else:
        is_return = args.roundtrip
    
        
    # export .json name
    if args.exp == '':
        is_export = False
    elif args.exp == []:
        is_export = "export"
    else:
        is_export = args.exp[0]


    return path, input_origin, input_destination, input_bags, is_return, days, is_export


def module():
    path, input_origin, input_destination, input_bags, is_return, days, is_export = inputs()

    ## CONVERTING ##

    # conversion of str time from csv

    def convert_to_datetime(str):
        _time = time.strptime(str, "%Y-%m-%dT%H:%M:%S")
        return _time

    ##            ##

    ## F U N C T I O N S    F O R   C L A S S E S ##

    def travel_time(s_t1, s_t2):
        t1 = time.mktime(s_t1)
        t2 = time.mktime(s_t2)
        return datetime.timedelta(seconds=(t1 - t2))

    # calculating the price for the trip including luggage price

    def total_sum(self):
        suma = 0
        for elem in self.flights:
            suma += elem.base_price
            suma += elem.bag_price * self.bags_count
        return suma

    # max bags allowed

    def bags_tolist(self):
        arr = []
        for elem in self.flights:
            arr.append(elem.bags_allowed)
        return min(arr)

    # calculating the actual travel_time for return trips

    def traveltime_corrector(self):
        h1, h2 = "", ""
        for elem in self.flights:
            if elem.destination == self.destination:
                h1 = elem.arrival
            if elem.origin == self.destination:
                h2 = elem.departure
        if h1 != "" and h2 != "":
            return travel_time(
                convert_to_datetime(h2),
                convert_to_datetime(h1)
            )

    ## E N D ##

    class All_Flights:
        """Class All_Flights
        allflights      [FlightQueue]
        """

        def __init__(self, allflights):
            self.allflights = allflights

        def reprJSON(self):
            return dict(allflights=self.allflights)

    class FlightQueue:
        """Class FlightQueue is used for sum up especially when travelling with connecting flights
        flights         [Flight],
        bags_allowed    int,
        bags_count      int,
        destination     string,
        origin          string,
        total_price     float,
        travel_time     str(timedelta) where it does not take the "holiday time" into account with return flights, 
        meaning: "Just time spent at the airports while travelling"
        """

        def __init__(self, flights):
            self.flights = flights

            self.bags_allowed = bags_tolist(self)

            self.bags_count = input_bags

            self.destination = input_destination
            self.origin = input_origin

            self.total_price = total_sum(self)
            diff = traveltime_corrector(self)
            if diff != None:
                self.travel_time = str(travel_time(convert_to_datetime(
                    self.flights[-1].arrival), convert_to_datetime(self.flights[0].departure)) - diff)
            else:
                self.travel_time = str(travel_time(convert_to_datetime(
                    self.flights[-1].arrival), convert_to_datetime(self.flights[0].departure)))

        def reprJSON(self):
            return dict(flights=self.flights,
                        bags_allowed=self.bags_allowed,
                        bags_count=self.bags_count,
                        destination=self.destination,
                        origin=self.origin,
                        totalprice=self.total_price,
                        travel_time=self.travel_time)

    class Flight:
        """Class Flight represents single flight and its atributes.
        flight_no    string,
        origin       string,
        destination  string,
        arrival      string,
        base_price   float,
        bag_price    float,
        bags_allowed int
        """

        def __init__(self, flight_no, origin,
                     destination, departure, arrival,
                     base_price, bag_price, bags_allowed):
            self.flight_no = flight_no
            self.origin = origin
            self.destination = destination
            self.departure = departure
            self.arrival = arrival
            self.base_price = base_price
            self.bag_price = bag_price
            self.bags_allowed = bags_allowed

        def reprJSON(self):
            return dict(flight_no=self.flight_no,
                        origin=self.origin,
                        destination=self.destination,
                        departure=self.departure,
                        arrival=self.arrival,
                        base_price=self.base_price,
                        bag_price=self.bag_price,
                        bags_allowed=self.bags_allowed)

    class ComplexEncoder(json.JSONEncoder):
        def default(self, obj):
            if hasattr(obj, 'reprJSON'):
                return obj.reprJSON()
            return json.JSONEncoder.default(self, obj)

    instances = []
    places = []

    with open(path, newline='') as csvfile:
        spamreader = csv.DictReader(csvfile)
        for row in spamreader:
            places.append(row['origin'])
            places.append(row['destination'])
            instances.append(Flight(row['flight_no'], row['origin'],
                                    row['destination'], row['departure'],
                                    row['arrival'], float(row['base_price']),
                                    float(row['bag_price']), int(row['bags_allowed'])))

    # creating index list to navigate
    just_places = list(set(places))

    # creating a template for list of successors
    targets = [[] for _ in just_places]

    # list of successors
    for elem in instances:
        targets[just_places.index(elem.origin)].append(elem)

    ## FUNCTIONS FOR LAME_BFS ##

    # layout time to be not be less than 1 hour and more than 6 hours.
    def layout_time_pred(t1, t2):
        delta = travel_time(convert_to_datetime(t1), convert_to_datetime(t2))
        return (delta >= datetime.timedelta(hours=1) and delta < datetime.timedelta(hours=6))

    # check destination against all origins, to avoid cyclic flights

    def check_destination(arr, fli):
        for flight in arr:
            if flight.origin == fli.destination:
                return False
        return True

    # check for the preffered number of bags

    def check_n_bags(fli):
        if fli.bags_allowed < input_bags:
            return False
        return True

    ##                        ##

    def lame_BFS(origin, destination):
        """This function is a basic altered version of graph searching algorithm, BFS.
        At first, it loads all flights from origin into separate arrays in Queue.
        If the last element's destination in this array isn't the wanted destination,
        it keeps trying to find the connecting flight for it, if not found, the array is poped from queue.
        Else it appends it to the result array.
        In the perfect world, this function could be implemented as O(n^2 * 2^n) but I'm affraid mine is worse, 
        because of the linear treversal of successors and linear helper functions used for it.
        This could be avoided and optimized, but the code would lost it's simplicity for the purpose for this task.

        Disclaimer:
        Using something DFS based might be a better idea, the runtime might be slightly improved,
        but the main issue of mine, BFS approach, could be exhausting of the Queue. 
        Because the actual Airports are the "Vertexes of many Edges" therefore the Queue could be full of those.
        Also the helper functions are working in O(n) and "simple" lists in python ain't really fast.
        """
        result = []
        q = deque()
        # push all flights from origin
        for e in targets[just_places.index(origin)]:
            # bags check
            if check_n_bags(e):
                q.append([e])

        while q != deque([]):
            src = q.popleft()
            if src[-1].destination == destination:
                # conversion to FlightQueue
                result.append(FlightQueue(src))
            else:
                for elem in targets[just_places.index(src[-1].destination)]:
                    # check for cycles, layout time, no.bags
                    if layout_time_pred(elem.departure, src[-1].arrival) and \
                            check_destination(src, elem) and \
                            check_n_bags(elem):
                        q.append(src+[elem])
        return result

    # lets have no assumptions about the time we would like to spend on destination before the return flight trip
    def roundtrip_flight_time_pred(t1, t2):
        delta = travel_time(convert_to_datetime(t1), convert_to_datetime(t2))
        return delta >= datetime.timedelta(days)

    # running the lame_BFS two times, then matching the departures and comming back

    def return_flights(origin, destination):
        way = lame_BFS(origin, destination)
        ways_back = lame_BFS(destination, origin)
        round_trips = []

        for flight in way:
            for fli_ in ways_back:
                arrival = fli_.flights[0].departure
                departure = flight.flights[-1].arrival
                if roundtrip_flight_time_pred(arrival, departure):
                    round_trips.append(FlightQueue(
                        flight.flights + fli_.flights))

        return round_trips

    if is_return:
        res = return_flights(input_origin, input_destination)
    else:
        res = lame_BFS(input_origin, input_destination)

    # sorting flightQueues against their price
    res.sort(key=operator.attrgetter('total_price'))

    # add to class
    aFx = All_Flights(res)

    # conversion, save as json
    if is_export:
        out_file = open(is_export+".json", "w")
        json.dump(aFx.reprJSON()['allflights'], out_file, cls=ComplexEncoder, indent=4)
        out_file.close()

    print(json.dumps(aFx.reprJSON()['allflights'], cls=ComplexEncoder, indent=4))

    


# this is used to call this python script as a module in terminal
if __name__ == "__main__":
    module()
