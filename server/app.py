from dataclasses import dataclass
from datetime import date, datetime
import logging
from typing import List
from flask import Flask, json, redirect, render_template, request

from send_notification import send_sms

logging.basicConfig(
    format="{asctime} - {levelname} - {message}", style="{", datefmt="%Y-%m-%d %H:%M"
)

app = Flask(__name__)


@dataclass
class Log:
    level: str
    date:date
    time: datetime
    message: str


log_storage: List[Log] = []

def convert_password(password:str):
    return "*" * len(password)

@app.route("/", methods=["GET"])
def home():
    
    with open("app_config.json") as f:
        data = json.load(f)

        contact_list = data["contactList"]
        message = data["message"]
        wifi_list = [{"name":wifi["name"],"password":convert_password(wifi["password"]) } for wifi in data["wifiList"]]
        
    return render_template("index.html", contact_list = contact_list, message = message, wifi_list=wifi_list), 200


def send_notification():
        
    with open("app_config.json") as f:
        data = json.load(f)

        contact_list = [contact["phoneNumber"] for contact in data["contactList"]]
        message = data["message"]
        send_sms(contact_list,message)
        
    return "ok", 200

@app.route("/status", methods=["GET"])
def status():
    return "ok", 200


@app.route("/log", methods=["GET"])
def log():

    level = request.args.get("level", "INFO")
    message = request.args.get("message", None)

    if message is not None:
        time = datetime.now().strftime("%H:%M:%S")
        date = datetime.now().strftime("%d/%m/%Y")
        
        global log_storage
        log_storage.append(Log(level=level, date = date, time=time, message=message))
        
        if level == "ACTIVATE":
            send_notification()
        
        return "ok", 200
    
    return "error", 400
    


@app.route("/get_logs", methods=["GET"])
def get_logs():
    count = request.args.get("count", default=0)
    return log_storage[int(count):], 200


@app.route("/get_wifi_info", methods=["GET"])
def get_wifi_info():
    access_key = request.args.get("access_key", default=None)
    if access_key is None or access_key != "DPYSfvktxWnFEoDqK891":
        return "error", 401
    
    with open("app_config.json") as f:
        data = json.load(f)        
        return data["wifiList"], 200
    
@app.route("/clear_log", methods=["GET"])
def clear_log():
    global log_storage
    log_storage = []

    return redirect("/")


@app.route("/update_form", methods=["GET"])
def update_form():
    name = request.args.get("name", default=None)
    phone_number = request.args.get("phoneNumber", default=None)
    wifi_name = request.args.get("wifiName", default=None) 
    wifi_password = request.args.get("wifiPassword", default=None) 

    message = request.args.get("message", default=None)

    with open("app_config.json") as f:
        data = json.load(f)

    if message is not None and len(message) != 0:
        data["message"] = message

    elif (
        name is not None
        and len(name) != 0
        and phone_number is not None
        and len(phone_number) != 0
    ):
        data["contactList"].append({"name": name, "phoneNumber": phone_number})
        
    elif (
        wifi_name is not None
        and len(wifi_name) != 0
        and wifi_password is not None
        and len(wifi_password) != 0
    ):
        data["wifiList"].append({"name": wifi_name, "password": wifi_password})
        
    else:
        return "error", 400

    with open("app_config.json", "w") as f:
        json.dump(data, f)

    return redirect("/")


@app.route("/remove_contact", methods=["GET"])
def remove_contact():
    phone_number = request.args.get("phoneNumber")
    if phone_number is None or len(phone_number) == 0:
        return "error", 400

    ids_removed = []
    new_contact_list = []
    with open("app_config.json") as f:
        data = json.load(f)

        for id, contact in enumerate(data["contactList"]):  
            if contact["phoneNumber"].lower().replace(" ","").replace("+","") != phone_number.lower().replace(" ","").replace("+",""):
                new_contact_list.append(contact)
            else:
                ids_removed.append(id)
        data["contactList"] = new_contact_list
        
    with open("app_config.json", "w") as f: 
        json.dump(data, f)
        
    return ids_removed, 200

@app.route("/remove_wifi", methods=["GET"])
def remove_wifi():
    name = request.args.get("name")
    if name is None or len(name) == 0:
        return "error", 400

    ids_removed = []
    new_wifi_list = []
    with open("app_config.json") as f:
        data = json.load(f)

        for id, wifi in enumerate(data["wifiList"]):  
            if wifi["name"] != name:
                new_wifi_list.append(wifi)
            else:
                ids_removed.append(id)
        data["wifiList"] = new_wifi_list
        
    with open("app_config.json", "w") as f: 
        json.dump(data, f)
        
    return ids_removed, 200

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8080)
