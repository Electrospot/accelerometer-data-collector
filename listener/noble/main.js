var util = require('util');
var noble = require('noble');
var binary = require('binary');
var _ = require('lodash');

if (process.argv.length != 3){
    console.log("usage:");
    console.log("on mac:   node main.js xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx");
    console.log("on linux: node main.js xxxxxxxxxxxx");
    process.exit(1);
}
var MY_BEAN_UUID = process.argv[2];
console.log(MY_BEAN_UUID);

var BEAN_SCRATCH1_SERVICE_UUID = 'a495ff20c5b14b44b5121370f02d74de';
var BEAN_SCRATCH1_CHAR_UUID    = 'a495ff21c5b14b44b5121370f02d74de';

Buffer.prototype.toByteArray = function() { return Array.prototype.slice.call(this, 0); };

var connectedBean = null;
var count = 0;

noble.on('stateChange', function(state) {
    if (state === 'poweredOn') {
        noble.startScanning();
        console.log('Scanning for BLE devices...');
    } else {
        noble.stopScanning();
        console.log('State changed to ' + '. Scanning stopped.');
    }
});

noble.on('discover', function(peripheral) {
    var name = peripheral.advertisement.localName;
    var uuid = peripheral.uuid;
    console.log(name);
    console.log(uuid);
    if (uuid == MY_BEAN_UUID){
        noble.stopScanning();
        console.log('Connecting to ' + name + '...');
        peripheral.connect(function(err) {
            if (err) throw err;
            console.log('Connected!');
            connectedBean = peripheral;
            peripheral.discoverSomeServicesAndCharacteristics([BEAN_SCRATCH1_SERVICE_UUID], [BEAN_SCRATCH1_CHAR_UUID], 
                function(error, services, characteristics){
                    console.log('in discoverSomeServicesAndCharacteristics!');
                    console.log(services);
                    console.log(characteristics);
                    var scratch1 = characteristics[0];
                    scratch1.on('data', function(data, isNotification) {
                        var ba = data.toByteArray();
                        var reading = binary.parse(ba)
                            .word16ls('timestamp')
                            .word16ls('x1') .word16ls('y1') .word16ls('z1')
                            .word16ls('x2') .word16ls('y2') .word16ls('z2')
                            .word16ls('x3') .word16ls('y3') .word16ls('z3')
                            .vars;
                        console.log('scratch1: ', 
                            [
                                count, 
                                reading['timestamp'],
                                reading['x1'], reading['y1'], reading['z1'],
                                reading['x2'], reading['y2'], reading['z2'],
                                reading['x3'], reading['y3'], reading['z3'],
                            ].join("\t"));
                        count += 1;
                    });

                    // true to enable notify
                    scratch1.notify(true, function(error) {
                        if (error) throw error;
                    }); 
            });
        });
    }

});

process.stdin.resume();//so the program will not close instantly

var triedToExit = false;

function exitHandler(options, err) {
    if (connectedBean && !triedToExit) {
        triedToExit = true;
        console.log('Disconnecting from Bean...');
        connectedBean.disconnect(function(err) {
            console.log('Disconnected.');
            process.exit();
        });
    } else {
        process.exit();
    }
}

// catches ctrl+c event
process.on('SIGINT', exitHandler.bind(null, {exit:true}));
