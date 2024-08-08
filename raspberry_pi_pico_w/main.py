import json
import network
import requests
import utime
import gc
from machine import Pin, ADC, PWM
import _thread

URL = "http://192.168.0.122:8080"
ACCESS_KEY = "DPYSfvktxWnFEoDqK891"
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
        }
    ]

def save_wifi_to_memory(wifi_list):
    with open("wifi_list.json", 'w') as f:
        f.write(json.dumps(wifi_list))
            

def load_wifi_from_memory():
    try:
        with open("wifi_list.json") as f:
            data = json.load(f)
            return data
    except OSError:
        save_wifi_to_memory(wifi_list) 
        return wifi_list
           
def led_animation_breath(no_cycles = 1000):
    for i in range(no_cycles):
        for duty in range(0, 65025, 1):
            PWM.duty_u16(duty)
            utime.sleep(0.0001)
            
        for duty in range(65025, 0, -1):
            PWM.duty_u16(duty)
            utime.sleep(0.0001)

def led_animation_blink(no_cycles = 1000):
    for i in range(no_cycles):
        for duty in range(0, 65025, 100):
            PWM.duty_u16(duty)
            utime.sleep(0.001)
            
        for duty in range(65025, 0, -100):
            PWM.duty_u16(duty)
            utime.sleep(0.001)

def update_vlan_info(wifi_list):
    
    response = requests.get(f"{URL}/get_wifi_info?access_key={ACCESS_KEY}")
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
    
    for _ in range(5):
        if wlan.isconnected():
            break
    
        utime.sleep(1)
    
    if not wlan.isconnected():
        return False
    
    try:
        response = requests.get("https://www.google.com/", timeout=5)
        if response.status_code == 200:
            log(f"Connected to network: {ssid}") 
            return True
    except OSError:
        pass   
    
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

    led_animation_blink(1)
    wifi_list = load_wifi_from_memory()
    

    for i in wifi_list:
        if connect_to_wlan(i["name"], i["password"]):
            wifi_list.remove(i)
            wifi_list.insert(0,i)
            led_animation_blink(1)
            break
        
    wifi_list = update_vlan_info(wifi_list)
    save_wifi_to_memory(wifi_list)
   
    _thread.start_new_thread(led_animation_breath, ())
    x = 0
    activations = [False,False,False] 
    while(True):
        val = measure_microphone()
        if val > 0.5 or val < 0.3:
            activations[x%3] = True
        else:
            activations[x%3] = False
        
        if all(activations):
            log("send notification", "ACTIVATE")
            activations = [False,False,False]
            
        log(f"{val}, {activations}", "MIC_VAL")    
        x += 1
        gc.collect()


main()

