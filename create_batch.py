import os
import sys
import csv
import requests
from ftplib import FTP
from dotenv import load_dotenv
import traceback
import tempfile
import logging

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(filename='email_verification.log', level=logging.INFO)

# Function to upload file via FTP
def upload_file_to_ftp(file_data):
    """
    Function to upload a file to an FTP server.

    Parameters:
    file_data (str): The data of the file to be uploaded.

    Returns:
    str: The URL of the uploaded file.
    """
    try:
        # Retrieve FTP credentials from environment variables
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

    except Exception as e:
        logging.error(f"Error occurred while uploading file to FTP: {str(e)}")
        raise

def main():
    """
    Main function to upload a CSV file to an FTP server and validate the email list using debounce.io API.

    Returns:
    None
    """
    try:
        # Check if CSV filename argument is provided
        if len(sys.argv) != 2:
            print("Usage: python create_batch.py <csv_filename>")
            sys.exit(1)

        # Extract CSV filename from command-line arguments
        csv_filename = sys.argv[1]

        # Check if CSV file exists
        if not os.path.isfile(csv_filename):
            logging.error("CSV file does not exist.")
            sys.exit(1)

        # Read CSV data
        with open(csv_filename, 'r') as file:
            csv_data = file.read()

        # Upload CSV to FTP server
        file_url = upload_file_to_ftp(csv_data)
        logging.info("CSV file uploaded to FTP server.")

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
                logging.error("List ID not found in response.")
        else:
            logging.error(f"Error occurred during validation: {response.text}")

    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")
        logging.error(traceback.format_exc())

if __name__ == "__main__":
    main()
