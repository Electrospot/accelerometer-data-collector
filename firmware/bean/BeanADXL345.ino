#include <SPI.h>

//Assign the Chip Select signal to pin 10.
int CS=2;

char POWER_CTL = 0x2D;	//Power Control Register
char DATA_FORMAT = 0x31;
char DATAX0 = 0x32;	//X-Axis Data 0
char DATAX1 = 0x33;	//X-Axis Data 1
char DATAY0 = 0x34;	//Y-Axis Data 0
char DATAY1 = 0x35;	//Y-Axis Data 1
char DATAZ0 = 0x36;	//Z-Axis Data 0
char DATAZ1 = 0x37;	//Z-Axis Data 1

void writeRegister(char registerAddress, char value){
    digitalWrite(CS, LOW);
    SPI.transfer(registerAddress);
    SPI.transfer(value);
    digitalWrite(CS, HIGH);
}

void readRegister(char registerAddress, int numBytes, unsigned char * values){
    char address = 0x80 | registerAddress;    
    if(numBytes > 1)address = address | 0x40;

    digitalWrite(CS, LOW);
    SPI.transfer(address);

    //Continue to read registers until we've read the number specified, storing the results to the input buffer.
    for(int i=0; i<numBytes; i++){
        values[i] = SPI.transfer(0x00);
    }
    digitalWrite(CS, HIGH);                   // Set the Chips Select pin high to end the SPI packet.
}

void adxl345_readXYZ(int * x, int *y, int *z){
    unsigned char values[6];
    readRegister(DATAX0, 6, values);
    *x = ((int)values[1]<<8) | (int)values[0];
    *y = ((int)values[3]<<8) | (int)values[2];
    *z = ((int)values[5]<<8) | (int)values[4];
}

int sleeping = 0;
void adxl345_measurement_mode(){
    if (sleeping)
        writeRegister(POWER_CTL, 1 << 3);   
    sleeping = 0;
}
void adxl345_sleep_mode(){
    if (! sleeping) 
        writeRegister(POWER_CTL, 1 << 2);   
    sleeping = 1;
}

void adxl345_setup(){ 
    SPI.begin();                      // Initiate an SPI communication instance.
    SPI.setDataMode(SPI_MODE3);       // Configure the SPI connection for the ADXL345.

    pinMode(CS, OUTPUT);              // Set up the Chip Select pin to be an output from the Arduino.
    digitalWrite(CS, HIGH);           // Before communication starts, the Chip Select pin needs to be set high.

    writeRegister(DATA_FORMAT, 0x01); // Put the ADXL345 into +/- 4G range by writing the value 0x01 to the DATA_FORMAT register.
    adxl345_measurement_mode();
}

int16_t convertToMg(int16_t rawAcceleration, uint8_t sensitivity) {
    int32_t convertedValue = (int32_t)rawAcceleration * (int32_t)sensitivity * 1000L;
    convertedValue /= 511;
    return (int16_t)convertedValue;
}

void setup() {
    adxl345_setup();
    Bean.setLed(0, 0, 0); 
    Bean.setBeanName("Mame1");
}

const uint16_t disconnected_sleep = 2000;

int32_t count = 0; // signed so that it's easier to parse the scratch data.
uint8_t buffer[8];
const int buffer_size = 8;
int x_buffer[buffer_size];
int y_buffer[buffer_size];
int z_buffer[buffer_size];

void loop() {
    if(Bean.getConnectionState()){
        adxl345_measurement_mode();

        adxl345_readXYZ(x_buffer + count % buffer_size, y_buffer + count % buffer_size, z_buffer + count % buffer_size);
        if (count % buffer_size == 0 && count > 0){
            String s(millis());
            s.concat(",");
            s.concat(count);
            for (int j = 0; j < buffer_size; j++){
              s.concat(",");
              s.concat(x_buffer[j]);
              s.concat(",");
              s.concat(y_buffer[j]);
              s.concat(",");
              s.concat(z_buffer[j]);
            }
            s.concat(";");
            Serial.println(s);
        }
        /*
        // alternatively, use scratch data. harder to access (code-wise) than serial
        int x,y,z;
        adxl345_readXYZ(&x, &y, &z);
        // signed, little endian
        buffer[0] = count & 0xFF;
        buffer[1] = count >> 8;
        buffer[2] = x & 0xFF;
        buffer[3] = x >> 8;
        buffer[4] = y & 0xFF;
        buffer[5] = y >> 8;
        buffer[6] = z & 0xFF;
        buffer[7] = z >> 8;
        Bean.setScratchData(1, buffer, 8);
        */
        ++count;
    }
    else{
        adxl345_sleep_mode();
        Bean.setLed(60, 0, 0);
        Bean.sleep(50);
        Bean.setLed(0, 0, 0);
        Bean.sleep(disconnected_sleep);
    }
}
