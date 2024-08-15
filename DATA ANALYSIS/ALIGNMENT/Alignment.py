import os
import sys
import numpy as np
import multiprocessing
from matplotlib import rc
import matplotlib.pyplot as plt
sys.path.append(r'C:\Users\ricca\Desktop\MAGISTRALE\QTLab2324\DATA ANALYSIS')
from UTILS.load_data import get_data, in_memory
from UTILS.drive import compress_hdf5, upload_file_to_drive, create_hdf5_file
from UTILS.Trigger import derivative_trigger, live_show, align_signal

rc('text', usetex=False)
rc('font', family='serif', size=20)
rc('figure', figsize=(12,8))
rc('axes',linewidth=2)

begin = 1.0*1e6
stop = begin+2*1e4

def main():

    files, svc = get_data(folder_id=str(sys.argv[1]),max_files=1000)

    #Run 13 done
    #Run 14 done

    # Start live_show in a separate process
    live_show_process = multiprocessing.Process(target=live_show, args=('Alignments.txt',))
    live_show_process.start()

    for i,file in enumerate(files):
        data = in_memory(file, svc)
        noise = data[int(begin):int(stop)]

#        bl = False
#        if len(sys.argv) > 1:
#            bl = True

        Timestamp = np.linspace(0, len(data), len(data), dtype=int)
        idx = np.array(Timestamp[:int(0.4 * 1e6)])
        T = Timestamp[idx]
        signal = data[idx]

        plt.figure(figsize=(20, 5))
        plt.plot(T, signal)
        plt.title('CUT I SIGNAL')
        plt.ylabel('[V]')
        plt.xlabel('Timestamp')

        a, b, _ = derivative_trigger(signal, 100, plot=False)

        print(f'{file} done!')

        with open('Alignments.txt', 'a') as file:
            file.writelines(str(b) + '\n')

        final, _ = align_signal(data,100,1000,20000)

        hdf5_file_path = 'data.hdf5'  # Path for the HDF5 file to create
        compressed_file_path = 'data.hdf5.gz'  # Path for the compressed file

        hdf5_file_path_noise = 'noise'+str(i)+'.hdf5'  # Path for the HDF5 file to create
        compressed_file_path_noise = hdf5_file_path_noise+'.gz'  # Path for the compressed file

        # Create HDF5 file
        create_hdf5_file(hdf5_file_path,final)
        create_hdf5_file(hdf5_file_path_noise,noise)

        # Compress HDF5 file
        compress_hdf5(hdf5_file_path, compressed_file_path)
        compress_hdf5(hdf5_file_path_noise, compressed_file_path_noise)

        upload_folder_id = '1hySBkWm_w7BPn4PMBf5OrxPtVIvVP1ln'
        upload_folder_id_noise = '1RwmgPIPpVKh0tqE4fx79U7RfeJAlOJjI'

        # Upload to Google Drive
        upload_file_to_drive(compressed_file_path, upload_folder_id)
        upload_file_to_drive(compressed_file_path_noise, upload_folder_id_noise)

        # Clean up
        os.remove(hdf5_file_path)
        os.remove(compressed_file_path)
        os.remove(hdf5_file_path_noise)
        os.remove(compressed_file_path_noise)

        # Ensure the live_show process completes
    live_show_process.join()

if __name__ == "__main__":
    main()