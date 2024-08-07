import os
import io
import sys
sys.path.append(r'C:\Users\ricca\Desktop\MAGISTRALE\QTLab2324\IR_SING_PHOT')
from HDF5 import HDF5
from googleapiclient.http import MediaFileUpload
import pickle
import h5py
from google.auth.transport.requests import Request
from googleapiclient.http import MediaIoBaseDownload
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import h5py
import os
import gzip
import shutil

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


def download_file_to_memory(service, file_id):
    """Download a file from Google Drive into memory."""
    request = service.files().get_media(fileId=file_id)
    file_stream = io.BytesIO()
    downloader = MediaIoBaseDownload(file_stream, request)
    done = False
    while done is False:
        status, done = downloader.next_chunk()
    
    file_stream.seek(0)  # Move to the beginning of the file
    return file_stream


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