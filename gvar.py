
g_engine = None
g_timer = None

Debug = False

Client = True

host = ""
port = 0
clients = 0
interval = 0
at_sec = 0

def Engine():
    global g_engine
    if not g_engine:
        import engine
        g_engine = engine.Engine()
    return g_engine

def Timer():
    global g_timer
    if not g_timer:
        import timer
        g_timer = timer.Timer()
    return g_timer
