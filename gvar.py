
eng = None

Debug = False
#Debug = True

Client = True

host = ""
port = 0
clients = 0
interval = 0
at_sec = 0

def Engine():
    return eng

def SetEngine(e):
    global eng
    eng = e
