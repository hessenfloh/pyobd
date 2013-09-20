#!/usr/bin/env python

import obd_io
import serial
import platform
import obd_sensors
from datetime import datetime
import time

from obd_utils import scanSerial

class OBD_Console():
    def __init__(self):
        self.port = None
        
    
    def connect(self):
        portnames = scanSerial()
        #portnames = ['COM10']
        print portnames
        for port in portnames:
            self.port = obd_io.OBDPort(port, None, 2, 2)
            if(self.port.State == 0):
                self.port.close()
                self.port = None
            else:
                break

        if(self.port):
            print "Connected to "+self.port.port.name
            
    def is_connected(self):
        return self.port
        

    def showOBDData(self):
        if(self.port is None):
            return None
        
        print "Showing current obd data:"
        for index,  e in enumerate(obd_sensors.SENSORS):
            (name,  value,  unit) = self.port.sensor(index)
            print name,  value,  unit
#            print index, e.name

c = OBD_Console()
c.connect()
if(c.is_connected()):
     c.showOBDData()
    
