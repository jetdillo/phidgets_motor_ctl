#!/usr/bin/env python
import rospy
from std_msgs.msg import *
from sensor_msgs.msg import Joy
import time
import getopt

md={'motor':0,'velocity':0} 
motorbtn={'motor1':0,'motor2':2,'up':3,'down':1,'L1':4,'L2':6,'R1':5,'R2':7}

def motor_pusher():

    global mdir,mdev,msafety,msel

    mdata=Int32MultiArray()
    mdata.layout.dim = [MultiArrayDimension('motor_state',2,1)] 
    mdata.data=md.values()

    msel={'motor1':False,'motor2':False} 
    mdir=0   


    rospy.init_node('motor_publisher', anonymous=True)
    rate = rospy.Rate(10) # 10hz

    motor1pub = rospy.Publisher('phidget1_motorctl',Int32MultiArray,queue_size=10)
    motor2pub = rospy.Publisher('phidget2_motorctl',Int32MultiArray,queue_size=10)
    msub = rospy.Subscriber('joy', Joy,joybutton_cb)
    rate = rospy.Rate(10) # 10hz
    while not rospy.is_shutdown():

       #rospy.loginfo("motor=%d velocity=%d %d",mdata.data[0],mdata.data[1],mstate)   

       if msafety:
          if mdir == 1:
             mdata.data[1]=50.00
          if mdir == -1:
             mdata.data[1]=-50.00
          if mdir == 0:
             mdata.data[1]=0.00

          if msel['motor1']:
             motor1pub.publish(mdata)

          if msel['motor2']: 
             motor2pub.publish(mdata)
          rospy.loginfo("motor=%d velocity=%d mdir=%d motor1=%d motor2=%d",mdata.data[0],mdata.data[1],mdir,msel['motor1'],msel['motor2'])
       else:
            mdata.data[1]=0.00
            motor1pub.publish(mdata)
            motor2pub.publish(mdata)
            msel['motor1']=0
            msel['motor2']=0
            mdir=0

       time.sleep(1)

def joybutton_cb(joy_msg):

   global mstate,msafety,mdir

   if joy_msg.buttons[motorbtn['motor1']]==1:
      msel['motor1']= not msel['motor1']
      msel['motor2']=False

   if joy_msg.buttons[motorbtn['motor2']]==1:
      msel['motor2']= not msel['motor2']
      msel['motor1']=False

   if joy_msg.buttons[motorbtn['L1']]==1:
      msafety=1
   else: 
      msafety=0

   if joy_msg.buttons[motorbtn['up']]==1:
      mdir=1

   if joy_msg.buttons[motorbtn['down']]==1:
      mdir=-1

   rospy.loginfo("msafety:%d motor1_state:%s motor2_state:%s" ,msafety,msel['motor1'],msel['motor2']) 

if __name__ == '__main__':

    mserial=0
    mname=''
    global msafety
    msafety=False
    try:
        opts, args = getopt.getopt(sys.argv[1:],"s:n:", ["serial=", "name=" ] )

    except getopt.GetoptError:
        # print help information and exit:
        print "Invalid parameters for %s " % sys.argv
        sys.exit(2)
    
    for o, a in opts:
     
        if o in ("-s","serial"): 
           mserial=a
        
        if o in ("-n","name"): 
           mname=a 

    mstate=0
    try:
        motor_pusher()
    except rospy.ROSInterruptException:
        pass
