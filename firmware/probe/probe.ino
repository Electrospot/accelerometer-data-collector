#include <ADXL345Arduino.h>

ADXL345 adxl345(SS);
int led = SS;

uint8_t buf[8];

void setup() {
    buf[0] = 0x00; // -32768, unlikely value
    buf[1] = 0x80;
    // pinMode(led, INPUT);   
    // pinMode(led, OUTPUT);   
    adxl345.set_range_16g_full_res();
    adxl345.set_stream_mode();
    adxl345.set_bw_rate_1600hz();
    Serial.begin(115200);
    Serial1.begin(115200);
    // Serial1.print("$");
    // Serial1.print("$");
    // Serial1.print("$");
    // delay(100);
    // Serial1.println("SA,0");
    // Serial1.println("R,1,0");
}

unsigned int counter = 0;

void loop() {
    int x,y,z;
    adxl345.readXYZ(&x, &y, &z);
    buf[2] = x & 0xFF;
    buf[3] = x >> 8;
    buf[4] = y & 0xFF;
    buf[5] = y >> 8;
    buf[6] = z & 0xFF;
    buf[7] = z >> 8;

    Serial1.write(buf, 8);
    
    // Serial1.println(String("R\t") + counter + "\t" + x + "\t" + y + "\t" + z);
    //Serial1.println(String("R\t") + x + "\t" + y + "\t" + z);
    delay(1);
}
