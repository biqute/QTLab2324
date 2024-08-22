import os
import sys
import h5py
import numpy as np
import multiprocessing
import logging
from matplotlib import rc
import winsound
sys.path.append(r'C:\Users\ricca\Desktop\MAGISTRALE\QTLab2324\DATA ANALYSIS')
from UTILS.load_data import get_data, in_memory
from UTILS.drive import upload_file_to_drive
from UTILS.Trigger import derivative_trigger, live_show, align_signal

# Matplotlib configuration
rc('text', usetex=False)
rc('font', family='serif', size=20)
rc('figure', figsize=(12,8))
rc('axes',linewidth=2)

# Logger configuration
logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s', 
                    handlers=[
                        logging.FileHandler("data_analysis.log"),
                        logging.StreamHandler(sys.stdout)
                    ])
logger = logging.getLogger()

begin = 1.0*1e6
stop = begin + 2*1e4

def main():

    counter = 0
    counter_not_work = 0

    # Log the start of the process
    logger.info("Starting data retrieval...")
    
    try:
        files, svc = get_data(folder_id=str(sys.argv[1]), max_files=1000)
        hdf5_file_path = 'data'+str(sys.argv[1])+'.hdf5'  # Path for the HDF5 file to create
    except Exception as e:
        logger.error(f"Failed to retrieve data: {e}")
        sys.exit(1)

    logger.info(f"Retrieved {len(files)} files.")

    # Start live_show in a separate process
    logger.info("Starting live_show process...")
    live_show_process = multiprocessing.Process(target=live_show, args=('Alignments.txt',))
    live_show_process.start()

    with h5py.File(hdf5_file_path, 'w') as hdf5_file:
        for i, file in enumerate(files):
            try:
                logger.info("Data in memory...")
                data = in_memory(file, svc)
            except Exception as e:
                logger.error(f"Could not load file {file} to memory: {e}")
                continue  # Continue to the next file

            noise = data[int(begin):int(stop)]

            Timestamp = np.linspace(0, len(data), len(data), dtype=int)
            idx = np.array(Timestamp[:int(0.4 * 1e6)])
            signal = data[idx]

            try: 
                logger.info("Triggering...")
                a, b, _ = derivative_trigger(signal, 100, plot=False)
            except Exception as e:
                logger.error(f"Something went wrong with trigger: {e}")
                continue  # Continue to the next file

            if (b<int(2.5e5) and b>int(1.5e5)):

                with open('Alignments.txt', 'a') as align_file:
                    align_file.writelines(str(b) + '\n')

                try:
                    logger.info("Aligning...")
                    final, _ = align_signal(data, 100, 1000, 20000)
                except Exception as e:
                    logger.warning(f"Could not align signal! {e}")
                    final = None  # Handle the case where alignment fails
                    
                try:
                    logger.info("Creating datasets")
                    if final is not None:
                        hdf5_file.create_dataset(f'Raw data{i}', data=final, compression='gzip', compression_opts=9)
                    hdf5_file.create_dataset(f'Noise{i}', data=noise, compression='gzip', compression_opts=9)
                except Exception as e:
                    logger.error(f"Could not create dataset: {e}")
                    continue  # Continue to the next file

            else:
                logger.warning("Alignment did not work")
                counter_not_work += 1

            if counter % 10 == 0:
                winsound.MessageBeep()

            logger.info(f'{file} processed successfully.')
            counter += 1

    # Ensure the live_show process completes
    logger.info("Waiting for live_show process to complete...")
    live_show_process.join(timeout=300)
    if live_show_process.is_alive():
        logger.warning("live_show process did not finish in time and will be terminated.")
        live_show_process.terminate()
    logger.info("live_show process completed.")

    upload_folder_id = '1F7OUtFBa1pjhLHwCA0mb6zoNt4UwXyfr'

    try:
        # Upload to Google Drive
        logger.info("Uploading file to Google Drive...")
        upload_file_to_drive(hdf5_file_path, upload_folder_id)
        logger.info("File uploaded successfully.")
    except Exception as e:
        logger.error(f"Failed to upload file: {e}")

    try:
        # Clean up
        os.remove(hdf5_file_path)
        logger.info("Clean up completed.")
    except Exception as e:
        logger.error(f"Failed to clean up files: {e}")

if __name__ == "__main__":
    main()
