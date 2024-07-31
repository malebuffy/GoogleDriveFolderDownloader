import os

from google.oauth2.credentials import Credentials

from google_auth_oauthlib.flow import InstalledAppFlow

from googleapiclient.discovery import build

from googleapiclient.http import MediaIoBaseDownload



# Define the scope and the API version

SCOPES = ['https://www.googleapis.com/auth/drive.readonly']

API_VERSION = 'v3'



def sanitize_file_name(file_name):

    return "".join(x for x in file_name.strip() if x.isalnum() or x in [" ", ".", "_", "-"])



def log(log_file, message):

    with open(log_file, "a") as f:

        f.write(message + "\n")



def create_directory(path, log_file):

    try:

        os.makedirs(path, exist_ok=True)

    except Exception as e:

        log(log_file, f'Error creating directory: {path} ({e})')

        print(f'Error creating directory: {path} ({e})')

        return False

    return True



def download_file(file_id, file_name, local_directory, drive_service, log_file):

    local_path = os.path.join(local_directory, file_name)

    local_path = os.path.normpath(local_path)



    if os.path.exists(local_path):

        log(log_file, f'Skipping download of {local_path} as it already exists')

        print(f'Skipping download of {local_path} as it already exists')

        return



    if not create_directory(local_directory, log_file):

        return



    request = drive_service.files().get_media(fileId=file_id)



    try:

        with open(local_path, 'wb') as fh:

            downloader = MediaIoBaseDownload(fh, request)

            done = False

            while not done:

                try:

                    status, done = downloader.next_chunk()

                except Exception as e:

                    log(log_file, f'Error downloading {local_path}: {e}')

                    print(f'Error downloading {local_path}: {e}')

                    return

            log(log_file, f'Downloaded {local_path}')

            print(f'Downloaded {local_path}')

    except Exception as e:

        log(log_file, f'Error writing file {local_path}: {e}')

        print(f'Error writing file {local_path}: {e}')



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



            subdirectory = os.path.join(local_directory, sanitize_file_name(file_name))

            subdirectory = os.path.normpath(subdirectory)



            if 'google-apps.folder' in file_mime_type:

                if create_directory(subdirectory, log_file):

                    download_folder(file_id, subdirectory, drive_service, log_file)

            else:

                download_file(file_id, sanitize_file_name(file_name), local_directory, drive_service, log_file)



def main():

    flow = InstalledAppFlow.from_client_secrets_file('REPLACE_WITH_YOUR_CLIENT_SECRET_FILE.json', SCOPES)

    creds = flow.run_local_server(port=0)

    drive_service = build('drive', API_VERSION, credentials=creds)



    # Replace with the folder ID of the shared folder you want to download

    folder_id = 'REPLACE_WITH_THE_FOLDER_ID'



    # Replace with the local directory where you want to save the downloaded files

    download_directory = '.'



    # Replace with the path to the log file

    log_file = 'download_log.txt'



    # Start downloading the folder

    download_folder(folder_id, download_directory, drive_service, log_file)



if __name__ == '__main__':

    main()

