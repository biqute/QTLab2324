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
            'level': 'INFO',
            'formatter': 'standard',
            'class': 'logging.FileHandler',
            'filename': r"C:\Users\kid\SynologyDrive\Lab2023\KIDs\QTLab2324\IRSource\Logger\logs\sessions" + date + ".log",
            'mode': 'a',
            'encoding': 'utf-8'
        },
        'mail': {
            'level': 'INFO',
            'formatter': 'standard',
            'class': 'logging.FileHandler',
            'mailhost': ('smtp.gmail.com', 587),
            'fromaddr': 'kinekids2324@gmail.com',
            'toaddrs' : 'r.maifredi@campus.unimib.it',
            'subject' : 'TEST',
            'credentials': ('kinekids2324', 'Ptx97!2017'),
            'timeout': 5.0
        }
    },
    'loggers': {
        '__main__': {
            'handlers': ['console', 'file', 'mail'],
            'level': 'INFO',
        },
        'DAQ': {
            'handlers': ['console', 'file', 'mail'],
            'level': 'INFO',
        }
    }
}