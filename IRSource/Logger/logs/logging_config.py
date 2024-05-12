from datetime import datetime
date = datetime.now().strftime("%m-%d-%Y-%H-%M-%S")

LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'standard': {
            'format': '%(asctime)s.%(msecs)03d - %(name)s - %(funcName)s - %(levelname)s - %(message)s',
            'datefmt': '%H:%M:%S'
        }
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'formatter': 'standard',
            'class': 'logging.StreamHandler',
            'stream': 'ext://sys.stdout'
        },
        'file': {
            'level': 'DEBUG',
            'formatter': 'standard',
            'class': 'logging.FileHandler',
            'filename': r"C:\Users\oper\SynologyDrive\Lab2023\Qubit\QTLab2324\IRSource\Logger\logs\sessions\\" + date + ".log",
            'mode': 'a',
            'encoding': 'utf-8'
        }
    },
    'loggers': {
        '__main__': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
        },
        'DAQ': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
        }
    }
}