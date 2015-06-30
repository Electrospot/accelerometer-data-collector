# Serial Monitor 
#     make monitor
# mapped ^C to ending monitor in ~/.screenrc 
MONITOR_PORT = /dev/ttyACM0
MONITOR_BAUDRATE = /dev/ttyACM0

### Board Specification
BOARD_TAG = micro
# For officially supported boards, just select one from 'make show_boards' 
# BOARD_TAG = uno
# BOARD_TAG = pro328    # mini pro 3.3v
# BOARD_TAG = pro5v328  # mini pro 5v
# BOARD_TAG = uno       # Arduino uno
# BOARD_TAG = fio       # Arduino fio
# BOARD_TAG = atmega328 # Arduino uno
# ALTERNATE_CORE = attiny
# BOARD_TAG = attiny85  # attiny85
# ALTERNATE_CORE = bean
# BOARD_TAG = lightblue-bean


### Cores
# The official core directory and board spec files are:
#     /usr/share/arduino/hardware/arduino/
#     /usr/share/arduino/hardware/arduino/boards.txt
#
# boards.txt contains configurations for that core. 
#
# instead, you can specify an alternate core with: 
# ALTERNATE_CORE = bean
# Which makes theres the core directory and board spec files:
#     ~/sketchbook/hardware/$(ALTERNATE_CORE)/
#     ~/sketchbook/hardware/$(ALTERNATE_CORE)/boards.txt
#
# notes the core directory is the one with a cores/ directory in it:
#     ~/sketchbook/hardware/$(ALTERNATE_CORE)/cores/
#
# then, BOARD_TAG should be one defined in boards.txt
# BOARD_TAG = lightblue-bean


### Libs
# list of libs found here:
#      /usr/share/arduino/libraries/
#      ~/sketchbook/libraries/
ARDUINO_LIBS = ADXL345Arduino SPI
# ARDUINO_LIBS = SPI 


### Other AVR Programmer
# ISP_PROG = usbtiny
# ISP_PORT = usb     # or a serial port
# redefine upload as ispload so you don't have to remember different command
# for different programmer
# upload: $(TARGET_HEX) verify_size
	# $(MAKE) ispload
flash: upload


### standard vars
# see /usr/share/arduino/Arduino.mk for more details
ARDUINO_DIR   = /usr/share/arduino
ARDMK_DIR     = /usr/share/arduino
AVR_TOOLS_DIR = /usr
include /usr/share/arduino/Arduino.mk

