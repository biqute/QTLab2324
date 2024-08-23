import sys
sys.path.append(r'C:\Users\ricca\Desktop\MAGISTRALE\QTLab2324\DATA ANALYSIS')
import logging
from UTILS import drive

# Logger configuration for the calling script
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    handlers=[
                        logging.FileHandler('calling_script.log'),
                        logging.StreamHandler(sys.stdout)
                    ])
logger = logging.getLogger()

folders = ['1yYLE5oZD8xLRU-p8sOcruevWP0dqUzAT','19y3UZN5FfFp0G1GCUJGydX3f8oTiwivq','12Cq--BfZONfpXNnzqw1xnwpKd4HLN5QY','1EZwnzFDOlW20t1Ufkj66OG_oNNCVGLGK']

for fol in folders:
    try:
        logger.info(f"Running script for folder ID: {fol}")
        drive.run_script(r'C:\Users\ricca\Desktop\MAGISTRALE\QTLab2324\DATA ANALYSIS\ALIGNMENT\Alignment.py', fol)
        drive.play_alert_sound()
    except Exception as e:
        logger.error(f"Error running script for folder ID {fol}: {e}")
