
eng = None

Debug = False
#Debug = True

Client = True

def Engine():
    return eng

def SetEngine(e):
    global eng
    eng = e
