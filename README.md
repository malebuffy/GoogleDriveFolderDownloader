# Google Drive Folder Downloader

Sometimes downloading a large folder with many subfolders is not possible via the right click on Google Drive, especially if it is a folder shared with you. This Python script allows you to create an exact copy of a Google Drive folder on your local hard drive, complete with OAuth for secure access. It also generates a log text file to keep track of any files that haven't been downloaded. Additionally, it skips files that already exist in the destination folder, so you don't need to download everything again in case of errors.

## Requirements

Before using this script, make sure you have the following:

- **Python**: Make sure you have Python installed on your system.

- **Google Console OAuth Setup**: You'll need OAuth 2.0 credentials configured for the Google account that has access to the Google Drive folder you want to download.

## Setting Up OAuth

To set up OAuth 2.0 credentials for your Google account, follow these steps:

1. **Go to the Google Cloud Console**:

   Visit the [Google Cloud Console](https://console.cloud.google.com/) and log in with your personal Google account (e.g., YourGoogleEmailName@gmail.com).

2. **Create a New Project**:

   If you don't have an existing project, create a new one by clicking on the project name in the top menu and selecting "New Project." Follow the prompts to create the project.

3. **Enable the Google Drive API**:

   In your project, click on "APIs & Services" > "Library" in the left sidebar. Search for "Google Drive API" and click on it. Then click the "Enable" button to enable the API for your project.

4. **Create OAuth 2.0 Client Credentials**:

   - In the Google Cloud Console, navigate to "APIs & Services" > "Credentials."
   - Click the "Create Credentials" button and select "OAuth client ID."
   - Choose "Desktop app" as the application type, and give your client ID a name.

5. **Download the Client Secret JSON**:

   After creating the OAuth 2.0 client credentials, click the "Download" button to get the client secret JSON file. This file contains the client ID and client secret, which you'll need for authentication.

## Editing the Download Script

Before executing the script, make the following edits:

- Set the `FOLDER_ID` variable to the ID of the Google Drive folder you want to download. Remove the "https://" part of the folder URL.
- Specify the name and path of your downloaded `secret.json` file.
- (Optional) Define the download path. You can use `'.'` to download the folder in the directory where `Downloader.py` is located.

## Execute

Make sure you install the necessary packages:

```bash
pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client
```

To execute the script, open your console or command prompt, navigate to the folder containing the script, and run the following command:

```bash
python Downloader.py
