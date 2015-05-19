#include <ADXL345Arduino.h>

ADXL345 adxl345(10);
void setup() {
    adxl345.sleep_mode();
    adxl345.set_range_16g_full_res();
    adxl345.set_stream_mode();
    adxl345.set_bw_rate_1600hz();
    adxl345.measurement_mode();
    Serial.begin(115200);
}

unsigned int counter = 0;
void loop() {
    int x,y,z;
    adxl345.readXYZ(&x, &y, &z);
    Serial.println(String("R\t") + counter + "\t" + x + "\t" + y + "\t" + z);
    counter++;
}
