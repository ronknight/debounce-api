import os
import sys
import csv
import requests
from ftplib import FTP
from dotenv import load_dotenv
import traceback
import tempfile

# Load environment variables from .env file
load_dotenv()

# Function to upload file via FTP
def upload_file_to_ftp(file_data):
    ftp_username = os.getenv('FTP_USERNAME')
    ftp_password = os.getenv('FTP_PASSWORD')
    ftp_hostname = '4sgm.us'
    ftp_path = '/new/uploads/'

    # Connect to FTP server
    with FTP(ftp_hostname) as ftp:
        ftp.login(user=ftp_username, passwd=ftp_password)

        # Upload file
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_file.write(file_data.encode())
            temp_file.seek(0)
            ftp.storbinary(f'STOR {ftp_path}/uploaded_file.csv', temp_file)

        # Construct file URL
        file_url = f"https://{ftp_hostname}{ftp_path}uploaded_file.csv"

    return file_url

def main():
    try:
        # Check if CSV filename argument is provided
        if len(sys.argv) != 2:
            print("Usage: python create_batch.py <csv_filename>")
            sys.exit(1)

        # Extract CSV filename from command-line arguments
        csv_filename = sys.argv[1]

        # Check if CSV file exists
        if not os.path.isfile(csv_filename):
            print("Error: CSV file does not exist.")
            sys.exit(1)

        # Read CSV data
        with open(csv_filename, 'r') as file:
            csv_data = file.read()

        # Upload CSV to FTP server
        file_url = upload_file_to_ftp(csv_data)

        # Validate the email list using debounce.io API
        debounce_url = "https://bulk.debounce.io/v1/upload/"
        api_key = os.getenv("API_KEY")

        url = f"{debounce_url}?url={file_url}&api={api_key}"

        headers = {"accept": "application/json"}

        response = requests.get(url, headers=headers)

        # Check if validation was successful
        if response.status_code == 200:
            # Extract list ID from response
            response_data = response.json()
            list_id = response_data.get('debounce', {}).get('list_id')
            if list_id:
                print("List ID:", list_id)
            else:
                print("Error: List ID not found in response.")
        else:
            print("Error:", response.text)

    except Exception as e:
        print("An error occurred:")
        print(traceback.format_exc())

if __name__ == "__main__":
    main()
