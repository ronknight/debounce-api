# Email List Validation and Processing - debounce-api

This project consists of two Python scripts that allow you to validate an email list using the Debounce.io API and download the processed file once it's ready.

## Scripts

### 1. `create_batch.py`

This script uploads a CSV file containing email addresses to an FTP server and validates the email list using the Debounce.io API. Here's how it works:

1. It checks if a CSV filename is provided as a command-line argument.
2. It reads the data from the provided CSV file.
3. It uploads the CSV file to an FTP server using the provided FTP credentials.
4. It sends a request to the Debounce.io API with the URL of the uploaded file and the API key.
5. It prints the list ID returned by the Debounce.io API, which is required for checking the status and downloading the processed file.

**Usage**:
```bash
python create_batch.py <csv_filename>
```
### 2. `get_status.py`

This script checks the status of a list on the Debounce.io API and downloads the file when it's ready. Here's how it works:

1. It checks if a list ID is provided as a command-line argument.
2. It sends a request to the Debounce.io API with the list ID and API key to check the status of the list.
3. It prints the status, percentage completed, and download link (if available).
4. If the status is "completed," it downloads the file using the provided download link.
5. If the status is not "completed," it waits for 1 minute and checks the status again.

**Usage**: 
```bash
python get_status.py <list_id>
```

## Setup

1. Clone the repository or download the scripts.
2. Create a `.env` file in the project directory and add the following environment variables:
   - `API_KEY`: Your Debounce.io API key.
   - `FTP_USERNAME`: Your FTP username.
   - `FTP_PASSWORD`: Your FTP password.
3. Install the required dependencies by running `pip install -r requirements.txt`.

## Usage

1. Run `create_batch.py` with a CSV file containing email addresses as an argument to upload the file and validate the email list.
2. After running `create_batch.py`, it will print the list ID. Copy this ID.
3. Run `get_status.py` with the list ID as an argument to check the status of the list and download the processed file when it's ready.

## Dependencies

This project uses the following Python libraries:

- `requests`: For making HTTP requests to the Debounce.io API.
- `python-dotenv`: For loading environment variables from a `.env` file.
- `ftplib`: For uploading files to an FTP server.

These dependencies are listed in the `requirements.txt` file and can be installed using `pip install -r requirements.txt`.

