import network
import requests
import utime
import gc
from machine import Pin, ADC, PWM
import _thread

URL = "http://192.168.0.122:8080/"
ACCESS_KEY = 'DPYSfvktxWnFEoDqK891'
# URL = "https://dev.randomscience.org"

RESISTOR = Pin(18,Pin.OUT ) 
RESISTOR.toggle()

MIC = ADC(Pin(26))
PWM = PWM(Pin(16))
PWM.freq(1000)

wifi_list = [
        {
            "name": "FurFur_2.4G",
            "password": "m0n41154"
        },  
    ]

def led_animation():

    while True:
        for duty in range(0, 65025, 1):
            PWM.duty_u16(duty)
            utime.sleep(0.0001)
            
        for duty in range(65025, 0, -1):
            PWM.duty_u16(duty)
            utime.sleep(0.0001)
            

def update_vlan_info():
    global wifi_list
    
    response = requests.get(f"{URL}/get_wifi_info?access_key={ACCESS_KEY}", timeout=10)
    if response.status_code != 200:
        return wifi_list
    known_networks = response.json()
    wifi_names = [network["name"] for network in wifi_list]
   
    for network in known_networks:
        if network["name"] not in wifi_names:
            wifi_list.append(network)            
    
    return wifi_list
     
    
    
def connect_to_wlan(ssid:str, password:str)->bool:
    
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    response = requests.get("https://www.google.com/", timeout=10)
    if response.status_code == 200:
        log(f"Connected to network: {ssid}") 
        return True
    return False

def log(message:str, level:str = "INFO"):
    
    message = message.replace(" ","_")
    requests.get(f"{URL}/log?level={level}&message={message}")
    
def measure_microphone(samples = 20):
    avg = 0
    for _ in range(samples):
        avg += MIC.read_u16()/65531
        utime.sleep(0.1)
    return avg / samples


def main():
    
    ssid = 'FurFur_2.4G' # wifi name
    password = 'm0n41154'
    
    connect_to_wlan(ssid, password)
    x = 0

    while(True):
        val = measure_microphone()
        log(f"{val}", "MIC_VAL")    
        x += 1
        gc.collect()

second_thread = _thread.start_new_thread(led_animation, ())
main()

