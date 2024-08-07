# horn_of_plenty
The motivation: ![image](motivation.png)
https://wiki.dfrobot.com/Fermion_MEMS_Microphone_Sensor_SKU_SEN0487
https://www.waveshare.com/wiki/Li-polymer_Battery_HAT

## Docker 
1. Build
```
docker build . -t horn_backend:v0.1.0 
```
2. run locally
```
docker run -p 8080:8080 horn_backend:v0.1.0
```
