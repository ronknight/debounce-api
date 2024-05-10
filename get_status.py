import os
import sys
import requests
import time
from dotenv import load_dotenv
import logging

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(filename='response.log', level=logging.INFO)

def get_debounce_status(list_id, api_key):
    """
    Function to get the status of a list from the Debounce API.

    Parameters:
    list_id (str): The ID of the list to check.
    api_key (str): The API key to use for the request.

    Returns:
    dict: The JSON response from the API, or None if the request was unsuccessful.
    """
    url = f"https://bulk.debounce.io/v1/status/?list_id={list_id}&api={api_key}"
    headers = {"accept": "application/json"}

    logging.info("Request URL: %s", url)  # Log the constructed URL

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        logging.error("Error: %s", response.text)
        return None

def download_file(url, filename):
    """
    Function to download a file from a given URL.

    Parameters:
    url (str): The URL of the file to download.
    filename (str): The name to give to the downloaded file.

    Returns:
    None
    """
    response = requests.get(url)
    if response.status_code == 200:
        with open(filename, 'wb') as f:
            f.write(response.content)
        logging.info("File downloaded successfully.")
    else:
        logging.error("Error: %s", response.text)

def main():
    """
    Main function to check the status of a list on the Debounce API and download the file when it's ready.

    Returns:
    None
    """
    try:
        # Load API key from environment variables
        api_key = os.getenv("API_KEY")

        if not api_key:
            logging.error("API_KEY not found in .env file.")
            return

        # Check if list ID argument is provided
        if len(sys.argv) != 2:
            logging.error("Usage: python get_status.py <list_id>")
            return

        list_id = sys.argv[1]

        # Loop until status is complete
        while True:
            # Check debounce status
            status_data = get_debounce_status(list_id, api_key)

            if status_data:
                debounce_info = status_data.get("debounce", {})
                success = status_data.get("success", "0")
                status = debounce_info.get("status")

                if success == "1":
                    logging.info("Debounce Status: %s", status)
                    logging.info("Percentage: %s", debounce_info.get("percentage"))
                    logging.info("Download Link: %s", debounce_info.get("download_link"))

                    if status == "completed":
                        download_link = debounce_info.get("download_link")
                        if download_link:
                            download_file(download_link, "downloaded_file.csv")
                            break  # Exit the loop if status is completed and file is downloaded
                        else:
                            logging.error("Error: Download link not available yet.")

                else:
                    logging.error("Error: Request was not successful.")

            logging.info("Will check again after 1 minute...")  # Wait for 60 seconds before checking status again
            time.sleep(60)

    except Exception as e:
        logging.error("An error occurred: %s", e)

if __name__ == "__main__":
    main()
