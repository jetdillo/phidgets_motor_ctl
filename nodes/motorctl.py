#!/usr/bin/env python
import sys
import getopt
import time
from  threading import Timer
from ctypes import *

import rospy
import roslib; roslib.load_manifest('phidgets_motor_ctl')
import numpy
from std_msgs.msg import *
from diagnostic_msgs.msg import DiagnosticArray, DiagnosticStatus, KeyValue

from Phidgets.Devices.MotorControl import MotorControl
from Phidgets.PhidgetException import PhidgetErrorCodes, PhidgetException
from Phidgets.Events.Events import EncoderPositionUpdateEventArgs
from Phidgets.Devices.Encoder import Encoder
from Phidgets.Manager import Manager
from Phidgets.Phidget import PhidgetID

class MotorCtl(object):

   def __init__(self,motornum,motorname):
     
     self.sernum=motornum
     self.motorName=motorname
     self.mc = MotorControl() 
     try:
        self.mc.openPhidget(self.sernum)
        self.mc.waitForAttach(10000) 
     except PhidgetException as e:
        print("Phidget Exception %i: %s" % (e.code, e.details))
        print("Exiting....")
        exit(1)
 
     self.motorstate_d={'motor':0,'serial':self.sernum,'state':0,'velocity':0,'ticks':0}
   
     self.motordata=Int32MultiArray()
     self.motordata.layout.dim = [MultiArrayDimension('motor_state',4,1)] 
     self.motordata.data=self.motorstate_d.values()
     self.rsp = rospy.Publisher('phidget_motor_state',Int32MultiArray,queue_size=10)
     rospy.init_node('aux_motor_ctl',anonymous=True)
     rospy.on_shutdown(self.shutdown)
      
     robotrate=10
     r=rospy.Rate(robotrate)

   def shutdown(self):
      # Always stop the robot when shutting down the node.
      #Stop the motor
      self.mc.setVelocity(self.motorstate_d['motor'],0) 
      rospy.loginfo("Stopping the Node...")
      rospy.sleep(1)

   def procMotorCtl(self,data):

      rospy.loginfo("Got command for motor=%s command=%f",self.motorName,data.data[1])
      self.motorCmd(data.data[0],data.data[1])

   def motorCmd(self,motor,velocity):
 
       self.mc.setAcceleration(motor, 50.00)
       self.mc.setVelocity(motor, velocity) 
       
       self.motorstate_d['motor']=motor
       self.motorstate_d['velocity']=velocity
       if velocity >0:
          self.motorstate_d['state']=1
       else:
          self.motorstate_d['state']=0

       self.motorstate_d['ticks']=self.mc.getEncoderPosition(0)
       rospy.loginfo("encoder ticks=%d",self.motorstate_d['ticks'])
       print (self.motorstate_d.values())
       self.motordata.data=self.motorstate_d.values()
       self.rsp.publish(self.motordata)
 
   def runner(self):
         motorCtl = rospy.Subscriber('motor_ctl',Int32MultiArray,self.procMotorCtl)
         rospy.spin()
 
if __name__ == '__main__':
   sernum=0
   motorname=''
   params=rospy.get_param_names()
#This is kind of a janky way to do this, but it's better than separate code for each motor
   num_motors=rospy.get_param('/motorcount')
 
   print "params are %s" % params
   if num_motors == 0:
      sernum=int(rospy.get_param('/phidget1_motorctl/motor_id'))
      rospy.set_param('/motorcount',1)
      motorname="motor1"
   if num_motors == 1:
      sernum=int(rospy.get_param('/phidget2_motorctl/motor_id'))
      rospy.set_param('/motorcount',2)
      motorname="motor2"
    
   motor = MotorCtl(sernum,motorname)
   motor.runner()
