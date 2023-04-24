import os
import yaml
from flask import Response
config=None
def onDownloadStart(ip):
    if config["type"] =="all": return False
    elif config["type"]=="whitelist":
        if ip in config["ips"]: return False
        else: 
            return Response(status=403,response="IP Whitelist is enabled here.")
            print("IP above has been blocked.")
    elif config["type"]=="blacklist":
        if not ip in config["ips"]: return False
        else: 
            print("IP above has been blocked.")
            return Response(status=403,response="IP Blacklist is enabled here.")
    else:
        print("Ip blacklist is disabled, incorrect config.")
    return False

def init():
    global config
    if not os.path.exists(os.path.join(CONFIGS_FOLDER,"ip-blacklist.yml")): 
        data = open(os.path.join(CONFIGS_FOLDER,"ip-blacklist.yml"),"w")
        data.write("type: all\nips: [127.0.0.1]")
        data.close()
    config = yaml.safe_load(open(os.path.join(CONFIGS_FOLDER,"ip-blacklist.yml")))

ACTION_INIT=init
CONFIGS_FOLDER=None
EVENT_ON_START_DOWNLOAD=onDownloadStart
EVENT_ON_FINISH_DOWNLOAD=None
EVENT_COMPLETE_MOVE=None