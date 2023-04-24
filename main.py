# LiveReplay
# CopyRight Techus 2023
# License: public domain
import importlib
import liblogger  # LibLogger is a bundled library. Used for logging.
liblogger.info("Initializing requierd libraries...")
plugins = []
EVENT_ON_START_DOWNLOAD=[]
EVENT_ON_FINISH_DOWNLOAD=[]
EVENT_COMPLETE_MOVE=[]
try:
    import shutil
    import os
    from flask import Flask, request
    import flask
    import asyncio
    from waitress import serve
    import yaml
    import traceback
    import sys
except ImportError:
    liblogger.error(
        "Couldn't initialize requierd libraries. Trying to download...")
    os.system("python3 -m pip install flask waitress pyyaml")
    liblogger.info(
        "If the command above succeeded, restart this program.\nIf not, try \"pip install waitress flask pyyaml\"")
    raise SystemExit()
except Exception as e:
    liblogger.error(
        f"Couldn't initialize requierd libraries. There is an error in a library.\nShort description: {e}\nFull traceback:\n"+traceback.format_exc())
    raise SystemExit()
liblogger.success("Initialized requierd libraries")
config = yaml.safe_load(open("config.yml"))
sys.path.append("plugins/")
liblogger.info("Creating folder for replay and temporary files...")
if not os.path.isdir(config["replay-folder"]):os.mkdir(config["replay-folder"])
if not os.path.isdir(config["temp-folder"]):os.mkdir(config["temp-folder"])
liblogger.info("Loading {} plugins".format(len(config["plugins"])))
for i in config["plugins"]:
    liblogger.info("Loading {} ".format(i))
    plguindata=importlib.import_module(i)
    plguindata.CONFIGS_FOLDER=config["plugin-config-folder"]
    if not plguindata.EVENT_ON_START_DOWNLOAD==None:
        liblogger.warn("{} has hooked into EVENT_ON_START_DOWNLOAD. Be aware.".format(i))
        EVENT_ON_START_DOWNLOAD.append(plguindata.EVENT_ON_START_DOWNLOAD)
    if not plguindata.EVENT_ON_FINISH_DOWNLOAD==None:
        liblogger.warn("{} has hooked into EVENT_ON_FINISH_DOWNLOAD. Be aware.".format(i))
        EVENT_ON_FINISH_DOWNLOAD.append(plguindata.EVENT_ON_FINISH_DOWNLOAD)
    if not plguindata.EVENT_COMPLETE_MOVE==None:
        liblogger.warn("{} has hooked into EVENT_COMPLETE_MOVE. Be aware.".format(i))
        EVENT_COMPLETE_MOVE.append(plguindata.EVENT_COMPLETE_MOVE)
    plguindata.ACTION_INIT()
    liblogger.success("Loaded {} ".format(i))
liblogger.success("Loaded {} plugins".format(len(config["plugins"])))

app = Flask(__name__)

@app.route('/upload', methods=['POST'])
def upload_video():
    ip_address = request.remote_addr
    liblogger.info("{} has started uploading data".format(ip_address))
    for i in EVENT_ON_START_DOWNLOAD:
        try:
            event=i(ip_address)
            if event!=False:
                return event
        except:
            liblogger.error("A plugin has raised an exception.\n"+traceback.format_exc())

    file = request.files['file']
    temp_filepath = os.path.join(config["temp-folder"], ip_address)
    file.save(temp_filepath)
    liblogger.info("Saved data from {} to {}".format(ip_address,temp_filepath))
    for i in EVENT_ON_FINISH_DOWNLOAD:
        event=i(ip_address,temp_filepath)
        if event!=False:
            return event
    replay_filepath = os.path.join(config["replay-folder"], ip_address+os.path.splitext(file.filename)[1])
    shutil.move(temp_filepath, replay_filepath)
    liblogger.info("Moved data from {} to {} (got it from IP {})".format(temp_filepath,replay_filepath,ip_address))
    liblogger.success("{}: Data ready".format(ip_address))
    for i in EVENT_COMPLETE_MOVE:
        event=i(ip_address,temp_filepath, replay_filepath)
        if event!=False:
            return event
    return flask.Response(status=200,response="200 OK")

if __name__=="__main__":
    liblogger.info("Starting up a server on {} port {}".format(config["address"],config["port"]))
    serve(app,host=config["address"],port=config["port"])