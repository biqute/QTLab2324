from UTILS.load_data import get_data, in_memory
from UTILS.drive import compress_hdf5, upload_file_to_drive, create_hdf5_file, authenticate
from UTILS.Trigger import derivative_trigger, live_show, align_signal
import matplotlib.pyplot as plt
import numpy as np
import sys
import os
import multiprocessing

def main():
    
    files, svc = get_data(max_files=1000)

    # Start live_show in a separate process
    live_show_process = multiprocessing.Process(target=live_show, args=('Alignments.txt',))
    live_show_process.start()

    for file in files:
        data = in_memory(file, svc)

        bl = False
        if len(sys.argv) > 1:
            bl = True

        Timestamp = np.linspace(0, len(data), len(data), dtype=int)
        idx = np.array(Timestamp[:int(0.4 * 1e6)])
        T = Timestamp[idx]
        signal = data[idx]

        plt.figure(figsize=(20, 5))
        plt.plot(T, signal)
        plt.title('CUT I SIGNAL')
        plt.ylabel('[V]')
        plt.xlabel('Timestamp')

        a, b, _ = derivative_trigger(signal, 100, plot=bl)

        print(f'{file} done!')

        with open('Alignments.txt', 'a') as file:
            file.writelines(str(b) + '\n')

        final, _ = align_signal(data,100,1000,20000)

        hdf5_file_path = 'data.hdf5'  # Path for the HDF5 file to create
        compressed_file_path = 'data.hdf5.gz'  # Path for the compressed file

        # Create HDF5 file
        create_hdf5_file(hdf5_file_path,final)

        # Compress HDF5 file
        compress_hdf5(hdf5_file_path, compressed_file_path)

        upload_folder_id = '19ApmRMhBMmQ7gT2i8akhViuKDyhP3QML'

        # Upload to Google Drive
        upload_file_to_drive(compressed_file_path, upload_folder_id)

        # Clean up
        os.remove(hdf5_file_path)
        os.remove(compressed_file_path)

        # Ensure the live_show process completes
    live_show_process.join()

if __name__ == "__main__":
    main()