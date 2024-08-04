from dataclasses import dataclass
from datetime import date, datetime
import logging
from typing import List
from flask import Flask, json, redirect, render_template, request

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


log_storage: List[Log] = [
   
    
]



@app.route("/", methods=["GET"])
def home():
    
    with open("app_config.json") as f:
        data = json.load(f)

        contact_list = data["contactList"]
        message = data["message"]

    return render_template("index.html", contact_list = contact_list, message = message), 200


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
        
        return "ok", 200
    
    return "error", 400
    


@app.route("/get_logs", methods=["GET"])
def get_logs():
    return log_storage, 200


@app.route("/clear_log", methods=["GET"])
def clear_log():
    global log_storage
    log_storage = []

    return redirect("/")


@app.route("/update_form", methods=["GET"])
def update_form():
    name = request.args.get("name", default=None)
    phone_number = request.args.get("phoneNumber", default=None)
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
    else:
        return "error", 400

    with open("app_config.json", "w") as f:
        json.dump(data, f)

    return redirect("/")


@app.route("/remove_contact", methods=["GET"])
def remove_contact():
    phone_number = request.args.get("phoneNumber")
    if phone_number is None and len(phone_number) == 0:
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


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8080)
