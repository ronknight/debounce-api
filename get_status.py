import os
import sys
import requests
import time  # Import time module for sleep
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def get_debounce_status(list_id, api_key):
    url = f"https://bulk.debounce.io/v1/status/?list_id={list_id}&api={api_key}"
    headers = {"accept": "application/json"}

    print("Request URL:", url)  # Print the constructed URL

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        print("Error:", response.text)
        return None

def download_file(url, filename):
    response = requests.get(url)
    if response.status_code == 200:
        with open(filename, 'wb') as f:
            f.write(response.content)
        print("File downloaded successfully.")
    else:
        print("Error:", response.text)

def main():
    try:
        # Load API key from environment variables
        api_key = os.getenv("API_KEY")

        if not api_key:
            print("Error: API_KEY not found in .env file.")
            return

        # Check if list ID argument is provided
        if len(sys.argv) != 2:
            print("Usage: python get_status.py <list_id>")
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
                    print("Debounce Status:", status)
                    print("Percentage:", debounce_info.get("percentage"))
                    print("Download Link:", debounce_info.get("download_link"))

                    if status == "completed":
                        download_link = debounce_info.get("download_link")
                        if download_link:
                            download_file(download_link, "downloaded_file.csv")
                            break  # Exit the loop if status is completed and file is downloaded
                        else:
                            print("Error: Download link not available yet.")

                else:
                    print("Error: Request was not successful.")

            # Wait for 30 seconds before checking status again
            time.sleep(30)

    except Exception as e:
        print("An error occurred:")
        print(e)

if __name__ == "__main__":
    main()
