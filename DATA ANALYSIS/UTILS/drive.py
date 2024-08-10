import os
import io
import sys
import h5py
import gzip
import shutil
sys.path.append(r'C:\Users\ricca\Desktop\MAGISTRALE\QTLab2324\IR_SING_PHOT')
from googleapiclient.http import MediaFileUpload
import pickle
from google.auth.transport.requests import Request
from googleapiclient.http import MediaIoBaseDownload
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import numpy as np


# If modifying these SCOPES, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/drive']

def authenticate():
    """Authenticate the user and return the service."""
    creds = None
    # The token.pickle stores the user's access and refresh tokens
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no valid credentials, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                r'C:\Users\ricca\Desktop\MAGISTRALE\QTLab2324\DATA ANALYSIS\UTILS\credentials.json', SCOPES)
            creds = flow.run_local_server(port=8080)  # Set port=0 to choose an available port
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    
    # Build the service object
    service = build('drive', 'v3', credentials=creds)
    return service

def list_files_in_folder(service, folder_id, max_files=5):
    """List a limited number of files in the specified Google Drive folder and its subfolders."""
    files = []
    page_token = None
    file_count = 0

    while True:
        if file_count >= max_files:
            break

        query = f"'{folder_id}' in parents"
        response = service.files().list(
            q=query,
            pageSize=100,
            fields="nextPageToken, files(id, name, mimeType)",
            pageToken=page_token
        ).execute()

        items = response.get('files', [])
        for item in items:
            if file_count >= max_files:
                break
            if item['mimeType'] == 'application/vnd.google-apps.folder':
                files += list_files_in_folder(service, item['id'], max_files - file_count)
            else:
                files.append(item)
                file_count += 1

        page_token = response.get('nextPageToken')
        if not page_token or file_count >= max_files:
            break

    return files

def read_hdf5_file(file_stream):
    # Use h5py to read from the in-memory file (BytesIO stream)
    with h5py.File(file_stream, 'r') as f:
        # Assuming 'Signals/I' is the correct path inside the HDF5 structure
        dataset = f['Signals']['I'][:]
    return dataset

def create_hdf5_file(file_path,data):
    """Create a sample HDF5 file with some example data."""
    with h5py.File(file_path, 'w') as hdf5_file:
        # Create a dataset with random data
        hdf5_file.create_dataset('example_data', data=data)
    print(f'HDF5 file created at {file_path}')

def compress_hdf5(file_path, output_path):
    """Compress HDF5 file using gzip."""
    with open(file_path, 'rb') as f_in:
        with gzip.open(output_path, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)

def upload_file_to_drive(file_path, drive_folder_id=None):
    """Upload a file to Google Drive."""
    service = authenticate()  # Get the Google Drive service
    
    file_name = os.path.basename(file_path)
    file_metadata = {'name': file_name}
    if drive_folder_id:
        file_metadata['parents'] = [drive_folder_id]
    
    media = MediaFileUpload(file_path, resumable=True)
    file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
    
    print(f'File {file_name} uploaded to Google Drive with file ID: {file["id"]}')
    
def download_file_from_drive(service, file_id):
    """Download a file from Google Drive to a destination."""
    request = service.files().get_media(fileId=file_id)
    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while not done:
        status, done = downloader.next_chunk()
        #print(f"Download progress: {int(status.progress() * 100)}%")
    fh.seek(0)
    return fh

def decompress_hdf5_to_memory(compressed_file_io):
    """Decompresses a .gz file from a BytesIO object and loads it into memory as an HDF5 file."""
    with gzip.GzipFile(fileobj=compressed_file_io, mode='rb') as f_in:
        decompressed_data = io.BytesIO(f_in.read())
        with h5py.File(decompressed_data, 'r') as hdf_file:
            # List all datasets in the file
            #print("Datasets available in the file:")
            # Replace 'dataset' with the correct name after inspecting the printout
            data = np.array(hdf_file['example_data'])  # Adjust 'dataset' to match the correct dataset name
    return data

def download_file_to_memory(service, file_id):
    """Download a file from Google Drive into memory."""
    request = service.files().get_media(fileId=file_id)
    file_stream = io.BytesIO()
    downloader = MediaIoBaseDownload(file_stream, request)
    done = False
    while done is False:
        status, done = downloader.next_chunk()
        print(f"Download {int(status.progress() * 100)}%.")
    
    # Make sure the stream position is at the start
    file_stream.seek(0)
    return file_stream
