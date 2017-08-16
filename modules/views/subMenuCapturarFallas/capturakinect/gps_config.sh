#!/bin/sh
#MAC de guille
sudo rfcomm connect /dev/rfcomm1 20:2D:07:2C:20:E3 7
sudo gpsd -N -n -b -S 9600 /dev/rfcomm1
