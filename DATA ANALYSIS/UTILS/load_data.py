from UTILS import drive

def get_data(folder_id = '1yYLE5oZD8xLRU-p8sOcruevWP0dqUzAT',max_files=5):
    #Authenticate in Google Cloud Console, use your institutional email address
    service = drive.authenticate()
    #Google Drive folder
    
    #Get files in folder
    files = drive.list_files_in_folder(service, folder_id,max_files)

    return files, service

def in_memory(file, service):
    #Read data and put them in RAM memory
    if file['name'].endswith('.h5') or file['name'].endswith('.hdf5'):
        file_id = file['id']
        #print(f"Downloading file: {file['name']}")
        file_stream = drive.download_file_to_memory(service, file_id)

    # Now read the HDF5 files from memory
    data = drive.read_hdf5_file_phase(file_stream)

    return data

if __name__ == '__main__':
    data = get_data()
    # Now you can use the 'data' variable as needed
    print(f"Processed data: {data}")