from niscope.errors import DriverError

def replace_non_serializable(obj):
    if isinstance(obj, dict):
        return {k: replace_non_serializable(v) for k, v in obj.items()}
    elif isinstance(obj, (list, tuple)):
        return [replace_non_serializable(item) for item in obj]
    elif isinstance(obj, (int, float, bool, str)):
        return obj
    else:
        # Convert non-serializable value to its string representation
        return str(obj)

def trai(acquis, trig):
    global flag
    try:
        
        return acquis(trig)
    except DriverError:
        flag += 1
        print(flag)
        
        if flag <= 10:
            print('PROVO')
            trai(acquis, trig)
        else:
            print('ERRORE')
        return [[],[],[],[]]


class Exceptions(object):

    def __init__(self,logger):
        logger = logger
        print('Exception!!')

    @property
    def CREATION(self):
        print("DAQ class object creation went wrong!")
        self.logger.info("CIAO!")

    @property
    def RESET(self):
        print("Could not reset DAQ")
    
    @property
    def DAQ_INIT_DIC(self):
        print("Mistake initializing configuration dictionaries")

    @property
    def JSON_DUMP(self):
        print("Could not dump!")