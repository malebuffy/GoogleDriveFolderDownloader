import os
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload

# Define the scope and the API version
SCOPES = ['https://www.googleapis.com/auth/drive.readonly']
API_VERSION = 'v3'

def sanitize_file_name(file_name):
    return "".join(x for x in file_name if x.isalnum() or x in [" ", ".", "_", "-"])

def log(log_file, message):
    with open(log_file, "a") as f:
        f.write(message + "\n")

def download_file(file_id, file_name, local_directory, drive_service, log_file):
    local_path = os.path.join(local_directory, file_name)
    if os.path.exists(local_path):
        log(log_file, f'Skipping download of {local_path} as it already exists')
        print(f'Skipping download of {local_path} as it already exists')
        return

    request = drive_service.files().get_media(fileId=file_id)
    try:
        os.makedirs(local_directory, exist_ok=True)
    except Exception as e:
        log(log_file, f'Error creating directory: {local_directory} ({e})')
        print(f'Error creating directory: {local_directory} ({e})')
        return

    fh = open(local_path, 'wb')
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while not done:
        try:
            status, done = downloader.next_chunk()
        except Exception as e:
            log(log_file, f'Error downloading {local_path}: {e}')
            print(f'Error downloading {local_path}: {e}')
        else:
            log(log_file, f'Downloaded {local_path}')
            print(f'Downloaded {local_path}')
    fh.close()

def download_folder(folder_id, local_directory, drive_service, log_file):
    results = drive_service.files().list(q=f"'{folder_id}' in parents", fields="files(id, name, mimeType)").execute()
    items = results.get('files', [])

    if not items:
        log(log_file, f'No files found in this folder: {local_directory}')
        print(f'No files found in this folder: {local_directory}')
    else:
        for item in items:
            file_id = item['id']
            file_name = item['name']
            file_mime_type = item['mimeType']

            # Check if it's a folder
            if 'google-apps' in file_mime_type:
                subdirectory = os.path.join(local_directory, sanitize_file_name(file_name))
                download_folder(file_id, subdirectory, drive_service, log_file)
            else:
                download_file(file_id, sanitize_file_name(file_name), local_directory, drive_service, log_file)

def main():
    # Replace with the secret file downloaded from the console
    flow = InstalledAppFlow.from_client_secrets_file('REPLACE WITH YOUR SECRET FILE NAME.json', SCOPES)
    creds = flow.run_local_server(port=0)
    drive_service = build('drive', API_VERSION, credentials=creds)

    # Replace with the folder ID of the shared folder you want to download
    folder_id = 'YOUR FOLDER ID'

    # Replace with the local directory where you want to save the downloaded files
    download_directory = '.'  

    # Replace with the path to the log file
    log_file = 'download_log.txt'

    # Start downloading the folder
    download_folder(folder_id, download_directory, drive_service, log_file)

if __name__ == '__main__':
    main()
