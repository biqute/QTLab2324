import drive

#Authenticate in Google Cloud Console, use your institutional email address
service = drive.authenticate()
#Google Drive folder
folder_id = '1yYLE5oZD8xLRU-p8sOcruevWP0dqUzAT' 
#Get files in folder
files = drive.list_files_in_folder(service, folder_id)

#Read data and put them in RAM memory
file_streams = []
for file in files:
    if file['name'].endswith('.h5') or file['name'].endswith('.hdf5'):
        file_id = file['id']
        print(f"Downloading file: {file['name']}")
        file_stream = drive.download_file_to_memory(service, file_id)
        file_streams.append(file_stream)

# Now read the HDF5 files from memory
data = drive.read_hdf5_file(file_streams)

