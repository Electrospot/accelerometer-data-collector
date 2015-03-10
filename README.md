accelerometer-study
===================

Introduction
------------

This is code for Spring 2015's accelerometer group study.

Hardware
--------

The device is a Punchthrough Bean with an ADXL345 accelerometer (on a Sparkfun breakout board).  The internal accelerometer on the Bean is not used because it cannot be sampled fast enough, due to the overhead of communication from  accelerometer (connected to the BLE module) to ATMega328p on the Bean. 

Pin conenction between the Bean and ADXL345 are as follows:

  | Bean | ADXL345 |
  |------|---------|
  | GND  | GND     |
  | VCC  | VCC     |
  | 2    | CS      |
  | 3    | SDA     |
  | 4    | SDO     |
  | 5    | SCL     |

Programming
-----------

A bean can be programmed with the standard Bean Loader and Arduino software, described below:

    https://punchthrough.com/bean/getting-started-osx/
    https://punchthrough.com/bean/getting-started-windows/
    http:// arduino.cc

Programming on Linux is possible via ICSP and an AVR programmer, and if you know what that means I assume you know how to do it. 

Contents
--------

-  `bean/` - contains arduino code.  There's only one version right now, which uses serial-emulation. But soon there will be a version with raw-BLE/GATT support.


Communication with the Bean
---------------------------

On OSX/Windows: in Bean Loader, you can create a virtual serial port connection to a Bean and then you can read from it with suitable software (e.g. screen or pyserial).

On Linux: details coming.


Data Format
-----------

Each line from the virtualized serial port has the following format:

    <timestamp>,<count>,<x1>,<y1>,<z1>,<x2>,<y2>,<z2>,<x4>,<y4>,<z4>,<x5>,<y5>,<z5>,<x6>,<y6>,<z6>,<x7>,<y7>,<z7>,<x8>,<y8>,<z8>;

-  `timestamp` is the number of miliseconds since the bean started.
-  `count` is the number of samples taken as of this datum.  Multiple of 8, since each line contains 8 data points.
-  `xN` x coordinate from accelerometer.  Range from -511 to +512, mapping to the acceleration in -4g to 4g (`g` == 9.8 m/s/s).
-  `yN` y coordinate from accelerometer.  
-  `zN` z coordinate from accelerometer.  

