from datetime import datetime
date = datetime.now().strftime("%m-%d-%Y")

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
            'level': 'DEBUG',
            'formatter': 'standard',
            'class': 'logging.StreamHandler',
            'stream': 'ext://sys.stdout'
        },
        'file': {
            'level': 'DEBUG',
            'formatter': 'standard',
            'class': 'logging.FileHandler',
            'filename': r'F:\\LabIV\\QTLab2324\\IRSource\\logs\\sessions\\' + date + '.log',
            'mode': 'a',
            'encoding': 'utf-8'
        }
    },
    'loggers': {
            '__main__': {
                'handlers': ['console','file'],
                'level': 'DEBUG'
            },
            'PXIe-5170R': {
                'handlers': ['console', 'file'],
                'level': 'DEBUG'
            }
    }
}
   
###################################################################
#SMTP not working
'''
,
'smtp': {
    'level': 'DEBUG',
    'formatter': 'standard',
    'class': 'logging.SMTPHandler',
    'mailhost': ('smtp.gmail.com', 465),
    'fromaddr': 'kinekids2324@gmail.com',
    'toaddrs': ['kinekids2324@gmail.com'],
    'subject': 'Data Acquisition',
    'credentials': ('kinekids2324','ylry timq pxfu xxmw')
}
'''
###################################################################
    