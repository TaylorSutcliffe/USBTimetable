import requests 
import json
from icalendar import Calendar, Event
import datetime

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


    #print(data)
    return returned

def timeTableGet(studentNo):
    g = open("calendar.ics", "w")
    #print(requests.get(f"https://m.ncl.ac.uk/itservice/ical/ical.php?personal={studentNo}&type=C;F;H;L;P;S;T;V;W;A").text)
    g.write(requests.get(f"https://m.ncl.ac.uk/itservice/ical/ical.php?personal={studentNo}&type=C;F;H;L;P;S;T;V;W;A").text)
    g.close()
    g = open("calendar.ics", "r")
    gcal = Calendar.from_ical(g.read())
    dic = {}
    l = []
    for component in gcal.walk():
         if component.name == "VEVENT":
            dic["title"] = component.decoded('SUMMARY')
            dic["start"] = component.decoded('dtstart').strftime("%Y-%M-%dT%XZ")
            dic["end"] = component.decoded('dtend').strftime("%Y-%M-%dT%XZ")
            dic["location"] = component.decoded('Location')
            l.append(dict(dic))
            #print(component.decoded('SUMMARY'))
            #print(component.decoded('dtstart'))
            #print(component.decoded('dtend'))
            #print(component.decoded('Location'))
    g.close()

    return l


    
#apiGet("room-6.025", values[0], tfStart="2019-04-27T00:00:00Z", tfEnd="2019-05-27T23:59:59")
#print(timeTableGet(160508552))