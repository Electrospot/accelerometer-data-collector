accelerometer-study
===================

Introduction
------------

![GUI](https://raw.githubusercontent.com/tnishimura/accelerometer-study/master/img/data-collector-medium.png)

This is a graphical data collection application for accelerometer based experiments.  It is written in Python and PyQt (the Python binding to the Qt GUI toolkit).  It has several features:

### Time limited sampling

The user collects samples by configuring a delay (in seconds) and sample size. Once the the Start button is clicked, the application will wait for the specified number of seconds, while a progress bar shows the remaining time. This delay is meant to allow the experimental subject some preparation time. As soon as the delay is over, the specific number of samples are collected and then immediately saved, after which a preview of the captured data is shown. The delay, akin to the countdown feature found on cameras obviates the need for a separate data collector. The experimental subject can can easily set a long enough delay to get into position for whatever movement being recorded.

I explored other ways of saving data from a live feed of data, including what I call “explicit stopping” “retrospective saving”. With explicit stopping, the application would have an additional “stop” button which would have to be pressed by a dedicated application operator. Explicit stopping may have uses in collecting movements which are unpredictable in length between samples. With retrospective saving, the data collector would tell the application to save the most recent data points based on the occurrence of some interesting event. This method is useful collecting data of movements which are not readily reproducible, such as earthquakes or driving over a speed bump.
I removed these two collection methods because the data I was interested in was reproducible and of predictable length. Including more than one collection method also hopelessly cluttered the interface.

### Live feed

The real-time, live data feed is displayed even if the user is not saving samples. Live sampling allows the user to “play” with the accelerometer and get a feel for what kind of signal it will produce, and helps determine the appropriate sampling size and delay. It also gives the user positive feedback that the device is actually connected and working. Captured samples are displayed statically in the preview window for inspection.

### Automatic file naming and saving

Given a directory and a sample name, sample data files are automatically named sequentially (for example, if the user is collecting “walking” data, the files can automatically be named “dir/walking-000.txt”, “dir/walking-001.txt”, and so on). This may seem insignificant but it reduces delay between sequential samples.

### Negative acknowledgement

Upon successful collection of a sample, no user input is necessary to collect another sample (besides clicking the start button again). The most recent sample is displayed in the preview window, and that sample can be deleted with a single button click when the data collector feels a sample needs to be rejected for whatever reason. I call this negative acknowledgement, in contrast to “positive acknowledgement”, where the user would be asked every time whether a sample should be saved to disk. I made this change because user-testing (on myself) suggested that mistakes were much less common than successful collection.

### Calibration
Accelerometers are often not perfectly calibrated and thus the application includes a simple specify a linear transformation to apply to each data dimension (a scaling factor and an offset) to compensate.

## User Flow

Thus, the user flow of the application is:

1.    User launches application, immediately sees live stream of data.	
2.    User plays around with accelerometer and previews what kind of data the movement produces.
3.    User sets the delay, and the sample size based on the previous step. Calibrates if necessary.
4.    User clicks Start.
5.    User or experimental subject gets ready during the delay time.
6.    The movement is performed and data is collected.
7.    User inspects the collected data.	
  *     If okay, repeat from step 4.
  *     If not, press cancel to delete most recent sample, and go back to step 3.

## Etc.

Check out the [Arduino library](https://github.com/tnishimura/ADXL345Arduino) I wrote for working with [SparkFun's ADXL345 Accelerometer breakout board](https://www.sparkfun.com/products/9836).

