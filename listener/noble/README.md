This listener uses node.js and the [noble](https://github.com/sandeepmistry/noble) library. 
It is largely based off [this example](https://github.com/mplewis/noble-bean) (license in LICENSE.original).

To run:

    node main.js [your bean's uuid or MAC address]

Note, for some reason on OS X you need to provide the 32-byte UUID, whereas on Linux you need to provide the device's MAC address.
