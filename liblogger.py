from datetime import datetime
ENABLE_LOGGING=True
class colorama:
    class Fore:
        RESET=""
        YELLOW=""
        RED=""
        GREEN=""
try:
    import colorama
    colorama.init()
except: pass
def info(log:str):
    if ENABLE_LOGGING==None:
        print("Logging ERROR!")
        raise LookupError()
    if ENABLE_LOGGING: print(colorama.Fore.RESET+"[{}] [INFO] ".format(datetime.today().strftime('%Y-%m-%d %H:%M:%S'))+str(log)+colorama.Style.RESET_ALL) 
def warn(log:str):
    if ENABLE_LOGGING==None:
        print("Logging ERROR!")
        raise LookupError()
    if ENABLE_LOGGING: print(colorama.Fore.YELLOW+"[{}] [WARN] ".format(datetime.today().strftime('%Y-%m-%d %H:%M:%S'))+str(log)+colorama.Style.RESET_ALL) 
def error(log:str):
    if ENABLE_LOGGING==None:
        print("Logging ERROR!")
        raise LookupError()
    if ENABLE_LOGGING: print(colorama.Fore.RED+"[{}] [ERROR] ".format(datetime.today().strftime('%Y-%m-%d %H:%M:%S'))+str(log)+colorama.Style.RESET_ALL) 
def success(log:str):
    if ENABLE_LOGGING==None:
        print("Logging ERROR!")
        raise LookupError()
    if ENABLE_LOGGING: print(colorama.Fore.GREEN+"[{}] [SUCCESS] ".format(datetime.today().strftime('%Y-%m-%d %H:%M:%S'))+str(log)+colorama.Style.RESET_ALL)