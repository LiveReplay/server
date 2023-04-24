def onDownloadStart(ip):
    """Will be called upon new server connection.
       ip: the IP of the client.
       Can return: False or flask.wrappers.Response
       """
    print(f"File in memory from {ip}")
    return False
def onDownloadFinish(ip,file):
    """Will be called upon file saved to temp folder.
       ip: the IP of the client.
       file: will give you the relative path of the file.
       Can return: False or flask.wrappers.Response
       """
    print(f"File from {ip} saved at {file}")
    return False
def onMoveComplete(ip,oldfile,newfile):
    """Will be called upon file saved to temp folder.
       ip: the IP of the client.
       oldfile: relative old path
       newfile: relative new path
       Can return: False or flask.wrappers.Response
       """
    print(f"File from ip {ip} moved temp {oldfile} to replay {newfile}")
    return False
def init():
    pass
ACTION_INIT=init
EVENT_ON_START_DOWNLOAD=onDownloadStart
EVENT_ON_FINISH_DOWNLOAD=onDownloadFinish
EVENT_COMPLETE_MOVE=onMoveComplete