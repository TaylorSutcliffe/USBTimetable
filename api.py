import requests 
import json


values = ["occupancy-sensor", "co2", "room-temperature", "relative-humidity"]


def apiGet(room, sensor, tfStart = None, tfEnd = None):
    """ A function that returns the values for either the latest value for a specified time frame exclusively
        
        room: in the format of a USB room such as "room-8.025"
        
        sensor: one of ["occupancy-sensor", "co2", "room-temperature", "relative-humidity"]
        
        tfStart, tfEnd: tfEnd must be greater than tfStart and both in format 2019-04-27T00:00:00Z"""
    returned = None
    data = None
    if tfStart and tfEnd:
        returned = requests.get(f"https://api.usb.urbanobservatory.ac.uk/api/v2/sensors/timeseries/{room}/{sensor}/raw/historic?startTime={tfStart}&endTime={tfEnd}").json()
        data = returned["historic"]["values"]
    else:
        returned = requests.get(f"https://api.usb.urbanobservatory.ac.uk/api/v2/sensors/timeseries/{room}/{sensor}/raw/").json()
        data = returned["latest"]


    print(data)
    return returned
    
apiGet("room-6.025", values[0], tfStart="2019-04-27T00:00:00Z", tfEnd="2019-05-27T23:59:59")