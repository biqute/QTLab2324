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