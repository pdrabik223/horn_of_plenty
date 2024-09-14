# horn_of_plenty
The motivation: ![image](motivation.png)
https://wiki.dfrobot.com/Fermion_MEMS_Microphone_Sensor_SKU_SEN0487
https://www.waveshare.com/wiki/Li-polymer_Battery_HAT

The 3d model of horn:
![alt text](./horn v13.png)
![alt text](ec2320e2-66a5-4aaf-af42-1675388f602c.jpg)
![alt text](ce554bdc-3af6-494f-b9c0-e35705f75e8e.jpg)



[Fusion 360 model link](https://a360.co/46Jb5fT)

[twilio console with billing info](https://console.twilio.com/us1/billing/manage-billing/billing-overview)


## Docker 

1. Build
```
docker build . -t horn_backend:v0.1.0 
```

2. run locally
```
docker run -p 8080:8080 horn_backend:v0.1.0

```
