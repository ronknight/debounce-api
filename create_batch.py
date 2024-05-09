import os
import sys
import csv
import requests
from ftplib import FTP
from dotenv import load_dotenv
import traceback

# Load environment variables from .env file
load_dotenv()

# Function to upload file via FTP
def upload_file_to_ftp(file_data):
    ftp_username = os.getenv('FTP_USERNAME')
    ftp_password = os.getenv('FTP_PASSWORD')
    ftp_hostname = '4sgm.us'

    ftp = FTP(ftp_hostname)
    ftp.login(user=ftp_username, passwd=ftp_password)

    # Example path where file will be uploaded on FTP server
    ftp_path = '/uploads/'  

    # Write the file to a temporary location
    temp_file_path = '/tmp/uploaded_file.csv'
    with open(temp_file_path, 'wb') as f:
        f.write(file_data)

    # Upload the file to FTP server
    with open(temp_file_path, 'rb') as f:
        ftp.storbinary(f'STOR {ftp_path}/uploaded_file.csv', f)
    
    # Close FTP connection
    ftp.quit()

    # Generate URL for the uploaded file
    file_url = f'https://{ftp_hostname}{ftp_path}/uploaded_file.csv'

    # Clean up temporary file
    os.remove(temp_file_path)

    return file_url

def get_list_id(file_url):
    url = "https://bulk.debounce.io/v1/upload/"

    # Get API key from environment variables
    api_key = os.getenv("API_KEY")

    # Check if API key is available
    if api_key is None:
        print("Error: API_KEY not found in .env file.")
        sys.exit(1)

    # Headers
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {api_key}"  # Add authorization header with API key
    }

    # Upload CSV data
    response = requests.post(url, headers=headers, json={"file_url": file_url})

    # Check if upload was successful
    if response.status_code == 200:
        # Extract list ID from response
        response_data = response.json()
        if 'list_id' in response_data:
            list_id = response_data['list_id']
            return list_id
        else:
            print("Error: List ID not found in response.")
            return None
    else:
        print("Error:", response.text)
        return None

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

        # Upload CSV to 4sgm.us via FTP
        file_url = upload_file_to_ftp(csv_data)

        # Get list ID from debounce.io
        list_id = get_list_id(file_url)

        if list_id:
            print("List ID:", list_id)
        else:
            print("Failed to get List ID.")

    except Exception as e:
        print("An error occurred:")
        print(traceback.format_exc())

if __name__ == "__main__":
    main()
