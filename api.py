import requests 
import json
from icalendar import Calendar, Event
import datetime

values = ["occupancy-sensor", "co2", "room-temperature", "relative-humidity"]
roomId = {}


def apiGet(room, sensor, tfStart = None, tfEnd = None):
    """ A function that returns the values for either the latest value for a specified time frame exclusively
        
        room: in the format of a USB room such as "room-8.025"
        
        sensor: one of ["occupancy-sensor", "co2", "room-temperature", "relative-humidity"]
        
        tfStart, tfEnd: tfEnd must be greater than tfStart and both in format 2019-04-27T00:00:00Z"""
    returned = None
    data = None
    if room == "room-4.022" or "room-2.022": #add rooms here with multiple zones
        if sensor == "occupancy-sensor":
            room = room.replace(".", "-")
            if tfStart and tfEnd:
                returned = requests.get(f"https://api.usb.urbanobservatory.ac.uk/api/v2/sensors/timeseries/{room}-zone-1/{sensor}/raw/historic?startTime={tfStart}&endTime={tfEnd}").json()
                data = returned["historic"]["values"]
            else:
                returned = requests.get(f"https://api.usb.urbanobservatory.ac.uk/api/v2/sensors/timeseries/{room}-zone-1/{sensor}/raw/").json()
                data = returned["latest"]
        else:
            room = room.replace("room-", "")
            if tfStart and tfEnd:
                if room in roomId:
                    returned = requests.get(f'https://api.usb.urbanobservatory.ac.uk/api/v2/sensors/timeseries/{roomId[room]}/historic?startTime={tfStart}&endTime={tfEnd}').json()
                else:
                    print(f"https://api.usb.urbanobservatory.ac.uk/api/v2.0a/sensors/entity?meta:roomNumber={room}&metric={sensor}")
                    tid = requests.get(f'https://api.usb.urbanobservatory.ac.uk/api/v2.0a/sensors/entity?meta:roomNumber={room}&metric={sensor}').json()
                    timeseriesid= tid['items'][0]['feed'][0]['timeseries'][0]['timeseriesId']
                    roomId[room] = timeseriesid
                    returned = requests.get(f'https://api.usb.urbanobservatory.ac.uk/api/v2/sensors/timeseries/{timeseriesid}/historic?startTime={tfStart}&endTime={tfEnd}').json()
                data = returned["historic"]["values"]
            else:
                returned = requests.get(f"https://api.usb.urbanobservatory.ac.uk/api/v2/sensors/timeseries/{room}-zone-3/{sensor}/raw/").json()
                data = returned["latest"]
    else:
        if tfStart and tfEnd:
            returned = requests.get(f"https://api.usb.urbanobservatory.ac.uk/api/v2/sensors/timeseries/{room}/{sensor}/raw/historic?startTime={tfStart}&endTime={tfEnd}").json()
            data = returned["historic"]["values"]
        else:
            returned = requests.get(f"https://api.usb.urbanobservatory.ac.uk/api/v2/sensors/timeseries/{room}/{sensor}/raw/").json()
            data = returned["latest"]


    #print(data)
    return data

def timeTableGet(studentNo):
    g = open("calendar.ics", "w")
    #print(requests.get(f"https://m.ncl.ac.uk/itservice/ical/ical.php?personal={studentNo}&type=C;F;H;L;P;S;T;V;W;A").text)
    g.write(requests.get(f"https://m.ncl.ac.uk/itservice/ical/ical.php?personal={studentNo}&type=C;F;H;L;P;S;T;V;W;A").text)
    g.close()
    g = open("calendar.ics", "r")
    gcal = Calendar.from_ical(g.read())
    dic = {}
    timetableList = []
    for component in gcal.walk():
         if component.name == "VEVENT":
            dic["title"] = component.decoded('SUMMARY').decode("utf-8")
            dic["start"] = component.decoded('dtstart').strftime("%Y-%m-%dT%XZ")
            dic["end"] = component.decoded('dtend').strftime("%Y-%m-%dT%XZ")
            dic["location"] = component.decoded('Location').decode("utf-8")
            timetableList.append(dict(dic))
            #print(component.decoded('SUMMARY'))
            #print(component.decoded('dtstart'))
            #print(component.decoded('dtend'))
            #print(component.decoded('Location'))
    g.close()

    return timetableList


    
#print(apiGet("room-6.025", values[0], tfStart="2019-04-27T00:00:00Z", tfEnd="2019-05-27T23:59:59Z"))
#print(timeTableGet(160508552))