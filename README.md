# horn_of_plenty
The motivation: ![image](motivation.png)
https://wiki.dfrobot.com/Fermion_MEMS_Microphone_Sensor_SKU_SEN0487
https://www.waveshare.com/wiki/Li-polymer_Battery_HAT

The 3d model of horn:
![horn v13](https://github.com/user-attachments/assets/0fb87d76-b1a9-45e9-8c74-b97f2b190473)

[Fusion 360 model link](https://a360.co/46Jb5fT)

## Docker 
1. Build
```
docker build . -t horn_backend:v0.1.0 
```
2. run locally
```
docker run -p 8080:8080 horn_backend:v0.1.0

```
