import sys
sys.path.append(r'C:\Users\ricca\Desktop\MAGISTRALE\QTLab2324\DATA ANALYSIS')
import logging
import subprocess
import numpy as np

# Logger configuration for the calling script
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    handlers=[
                        logging.FileHandler('calling_script.log'),
                        logging.StreamHandler(sys.stdout)
                    ])
logger = logging.getLogger()

def run_script(script_path, *args):
    """
    Executes a Python script with the provided arguments.

    :param script_path: Path to the Python script to execute.
    :param args: Arguments to pass to the script.
    """
    command = [sys.executable, script_path] + list(args)
    try:
        result = subprocess.run(command, check=True, text=True, capture_output=True)
        print("Script Output:\n", result.stdout)
    except subprocess.CalledProcessError as e:
        print("An error occurred while running the script:\n", e.stderr)

for fol in np.linspace(1,10,9)*0.0015:
    try:
        logger.info(f"Running script for sigma ID: {fol}")
        run_script(r'/home/drtofa/OneDrive/QTLab2324/DATA ANALYSIS/FINAL/analyze.py', str(fol))
    except Exception as e:
        logger.error(f"Error running script for folder ID {fol}: {e}")
