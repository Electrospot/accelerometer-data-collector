#include <SPI.h>
#include <ADXL345Arduino.h> // see https://github.com/tnishimura/ADXL345Arduino

//////////////////////////////////////////////////////////////////////////
// 

boolean is_connected = false; // don't check every single loop() b/c it takes time to check
uint16_t counter = 0; // signed so that it's easier to parse the scratch data.

unsigned long time_of_connection_start;
int16_t fifo_buffer[32 * 3]; 
uint8_t scratch[20];

void setup() {
    adxl345_set_cs_pin(2);
    adxl345_setup();
    adxl345_set_range_16g_full_res();
    adxl345_set_fifo_stream_mode();
    adxl345_set_bw_rate_1600hz();
    Bean.setLed(0, 0, 0); 
    Bean.setBeanName("MameBinary");
}

void loop() {
    if(is_connected){
        uint16_t current = (millis() - time_of_connection_start) % 65536;
        adxl345_measurement_mode();
        int occupancy = adxl345_get_fifo_occupancy();
        int step = occupancy / 3;

        // read everything in fifo
        for (int i = 0; i < occupancy * 3; i+=3) {
            adxl345_readXYZ(fifo_buffer + i, fifo_buffer + i + 1, fifo_buffer + i + 2);
        }

        for (int i = 2; i < 20; i++) {
            scratch[i] = 0;
        }

        scratch[0] = current & 0xFF;
        scratch[1] = current >> 8;
        if (occupancy >= 1){
            scratch[2] = fifo_buffer[0] & 0xFF;
            scratch[3] = fifo_buffer[0] >> 8;
            scratch[4] = fifo_buffer[1] & 0xFF;
            scratch[5] = fifo_buffer[1] >> 8;
            scratch[6] = fifo_buffer[2] & 0xFF;
            scratch[7] = fifo_buffer[2] >> 8;
        }
        if (occupancy >= 2){
            int middle = step > 1 ? step : 1;
            scratch[8] = fifo_buffer[middle * 3 + 0] & 0xFF;
            scratch[9] = fifo_buffer[middle * 3 + 0] >> 8;
            scratch[10] = fifo_buffer[middle * 3 + 1] & 0xFF;
            scratch[11] = fifo_buffer[middle * 3 + 1] >> 8;
            scratch[12] = fifo_buffer[middle * 3 + 2] & 0xFF;
            scratch[13] = fifo_buffer[middle * 3 + 2] >> 8;
        }
        if (occupancy >= 3){
            int end = step > 1 ? 2 * step : 2;
            scratch[14] = fifo_buffer[end * 3 + 0] & 0xFF;
            scratch[15] = fifo_buffer[end * 3 + 0] >> 8;
            scratch[16] = fifo_buffer[end * 3 + 1] & 0xFF;
            scratch[17] = fifo_buffer[end * 3 + 1] >> 8;
            scratch[18] = fifo_buffer[end * 3 + 2] & 0xFF;
            scratch[19] = fifo_buffer[end * 3 + 2] >> 8;
        }
        Bean.setScratchData(1, (uint8_t *)scratch + 0, 20);

        ++counter;
        
        // only check connection state every 200 samples b/c it's slow.
        if (counter % 200 == 0){
            is_connected = Bean.getConnectionState();
        }
    }
    else{
        adxl345_sleep_mode();
        Bean.setLed(60, 0, 0);
        Bean.sleep(50);
        Bean.setLed(0, 0, 0);
        Bean.sleep(2000);
        is_connected = Bean.getConnectionState();
        if (is_connected){
            time_of_connection_start = millis();
            counter = 0;
        }
    }
}
