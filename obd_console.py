#!/usr/bin/env python

import obd_io
import serial
import platform
import obd_sensors
from datetime import datetime
import time
import MySqldb

from obd_utils import scanSerial

class OBD_Console():
    def __init__(self):
        self.port = None
        self.mysql = MySqldb.connect("localhost", "obdlogger", "HSNtHVvTpE5CSUPa", "obdlogger")
        self.cursor = self.mysql.cursor()
        self.cursor.execute("INSERT INTO trip (description) VALUES ('')")
        self.cursor.execute("SELECT MAX(id) FROM trip")
        self.tripid = self.cursor.fetchone()
    
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

    def addDatapoint(self):
        self.cursor.execute("INSERT INTO datapoint (tripid) VALUES (%s)", self.tripid)
        self.cursor.execute("SELECT MAX(datapointid) FROM datapoint WHERE tripid=%s", self.tripid)
        self.datapointid = self.cursor.fetchone()

    def showOBDData(self):
        if(self.port is None):
            return None
        
        print "Showing current obd data:"
        for index,  e in enumerate(obd_sensors.SENSORS):
            if(self.port.State != 0):
                (name,  value,  unit) = self.port.sensor(index)
                print name,  value,  unit
                self.cursor.execute("INSERT INTO sensorvalues "
                                    "(tripid, datapointid, sensorid, name, value, unit)"
                                    " VALUES (%s, %s, %s, %s, %s, %s"
                                    , self.tripid, self.datapointid, index, name, value, unit)


c = OBD_Console()
c.connect()
if(c.is_connected()):
  c.showOBDData()
else:
  for index, e in enumerate(obd_sensors.SENSORS):
    print index, e.name
    
