#!/usr/bin/env python2
# -*- coding: utf-8 -*-
import time
import gps
import sys

'''
    Pasos a realizar en ubuntu
    
    adb devices
    
    adb forward tcp:20175 tcp:50000
    
    Editar el siguiente archivo:
        /lib/systemd/system/gpsd.socket
        -ListenStream=127.0.0.1:2947
        +ListenStream=0.0.0.0:2947
        SocketMode=0600
        +SocketMode=0666
    
    sudo service gpsd stop
    
    sudo systemctl daemon-reload
    
    sudo gpsd -D5 -N -n -b tcp://localhost:20175
'''

def main(gpsd_report):
    '''http://code.google.com/apis/kml/documentation/kmlreference.html
       for official kml document'''

    if len (sys.argv) < 2:
         print "Usage: gpsd.py [kml-file]"
         sys.exit();

    print gpsd_report
    if not 'lat' in gpsd_report.keys():
        return
    kml_file = sys.argv[1]
    latitude =  gpsd_report['lat']
    longitude = gpsd_report['lon']
    #speed_in =  gpsd_report['speed'] # meter/second
    #speed = speed_in * 3.6 # Km/h
    #heading =   gpsd_report['track']
    #altitude =  gpsd_report['alt']
    #time_str =   gpsd_report['time'] # time since the Unix epoch UTC
    # time_str = time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime(time_in))
    #gerange = ((speed / 100) * 350) + 650
    #tilt = 0

    #if speed < 1:
    #    gerange = 200
    #    heading = 0

    output = """<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://earth.google.com/kml/2.0">
<Placemark>
    <description>Realtime GPS feeding</description>
    <LookAt>
        <longitude>%s</longitude>
        <latitude>%s</latitude>
    </LookAt>
    <Point>
        <coordinates>%s,%s</coordinates>
    </Point>
</Placemark>
</kml>""" % (longitude,latitude,longitude,latitude)

    #status_line = '<{0}> Speed: {1:.2f} Km/h, Heading: {2:.0f}'.format(time_str,
    #                                                      speed, heading)
    #print status_line
    f = open(kml_file, 'w')
    f.write(output)
    f.close()

if __name__ == "__main__":
    session = gps.gps()
    session.stream(gps.WATCH_ENABLE|gps.WATCH_NEWSTYLE)

    try:
        while True:
            report = session.next()
            print report
            if report['class'] == 'TPV':
                main(report)
    except StopIteration:
        print 'GPSD has terminated'
