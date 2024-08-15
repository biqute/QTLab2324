import sys
sys.path.append(r'C:\Users\ricca\Desktop\MAGISTRALE\QTLab2324\DATA ANALYSIS')
from UTILS.load_data import get_data, in_memory
from UTILS.drive import compress_hdf5, upload_file_to_drive, create_hdf5_file
import numpy as np
import os

begin = 1.0*1e6
stop = begin+2*1e4

def main():
    
    files, svc = get_data(max_files=1000)

    for i,file in enumerate(files):
        print(f'Working on file n° {i}')
        data = np.array(in_memory(file,svc)[int(begin):int(stop)])     

        print(f'{file} done!')

        hdf5_file_path = 'noise'+str(i)+'.hdf5'  # Path for the HDF5 file to create
        compressed_file_path = hdf5_file_path+'.gz'  # Path for the compressed file

        # Create HDF5 file
        create_hdf5_file(hdf5_file_path,data)

        # Compress HDF5 file
        compress_hdf5(hdf5_file_path, compressed_file_path)

        upload_folder_id = '1jlqfOxQdq06XjZmWYrYFiQhtDJbilT8f'

        # Upload to Google Drive
        upload_file_to_drive(compressed_file_path, upload_folder_id)

        # Clean up
        os.remove(hdf5_file_path)
        os.remove(compressed_file_path)

if __name__ == "__main__":
    main()