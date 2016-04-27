# phidgets_motor_ctl
ROS node and example client for controlling a Phidgets Single Motor &amp; Encoder Board (Product ID 62 Model 1065).

Wait, yet Another Phidgets ROS node ? 
Yazzzz
I had to get a Phidgets single-motor board and encoder working on a ROS Robot recently. 
What I found on the ROS Wiki was either unmaintained or buried inside a product namespace (Corobot) AND assumed that the
motors were going to be used as the drive system for the robot, which mine wasn't. 

This is pretty basic stuff right now but it works for the prototype I had to build. 
Ideally one would tie this in with a node that tracks/controls a set of limit switches or other code that controls
and constrains the operation of the motors, but that's more on the implementation side.  My goal here was a minimalist node that you could use to talk directly to the Phidgets board without a lot of extra baggage. 


