accelerometer-study
===================

Introduction
------------

This is a data collection and analysis package for accelerometer data, collected using an ADXL345 accelerometer and a Punchthrough Bean wireless Bluetooth Low Energy board.

Hardware
--------

![Mame](https://raw.githubusercontent.com/tnishimura/accelerometer-study/master/img/mame.png)

The device is a [Punchthrough Bean](https://punchthrough.com/bean/) with an ADXL345 accelerometer (on a Sparkfun breakout board).  (Though the Bean has a built-in accelerometer as well, it is not used because it cannot be sampled fast enough, due to the overhead of communication from  accelerometer (connected to the BLE module) to ATMega328p on the Bean.)

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
    http://arduino.cc

Programming on Linux is possible via ICSP and an AVR programmer.

You will also need my library for using the ADXL345 from here:

    https://github.com/tnishimura/ADXL345Arduino


Contents
--------

-  `bean/BeanADXL345.ino` -  Bean/Arduino code which uses serial-emulation.  Samples at around 35Hz.
-  `bean/BeanADXL345Binary.ino` - A more refined version, which communicates via raw BLE using the Bean's `scratch` characteristics.  Samples at over 100HZ.
-  `listener/noble` - A "listener", or an application to let you capture data from the bean, written in node.js and the noble library.  OS X and Linux.
-  `listener/gatttool` - Another listener, which uses the gatttool command line utility. Linux only.


Communication with the Bean
---------------------------

On OSX/Windows: in Bean Loader, you can create a virtual serial port connection to a Bean and then you can read from it with suitable software (e.g. screen or pyserial).

On Linux: There is code in `linux/`, details coming soon.


Seial Data Format
-----------------

Each line from the virtualized serial port has the following format:

    <timestamp>,<count>,<x1>,<y1>,<z1>,<x2>,<y2>,<z2>,<x4>,<y4>,<z4>,<x5>,<y5>,<z5>,<x6>,<y6>,<z6>,<x7>,<y7>,<z7>,<x8>,<y8>,<z8>;

-  `timestamp` is the number of miliseconds since the bean started.
-  `count` is the number of samples taken as of this datum.  Multiple of 8, since each line contains 8 data points.
-  `xN` x coordinate from accelerometer.  Range from -511 to +512, mapping to the acceleration in -4g to 4g (`g` == 9.8 m/s/s).
-  `yN` y coordinate from accelerometer.  
-  `zN` z coordinate from accelerometer.  

Binary Data Format
------------------

For `BeanADXL345Binary.ino`, the `scratch1` characteristic has the three most recent samples from the ADXL345.  It is always twenty bytes, encoded 10 little-endian signed 16 byte integers.  The first of these integers is the timestamp (number of milliseconds since power-on) modulo'd to fit in a 16 bytes integer, and the next nine are 3 triplets of x,y,z coordinates.  (More details coming soon).




