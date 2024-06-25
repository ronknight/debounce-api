<p><a target="_blank" href="https://app.eraser.io/workspace/6UvuHFuaM5A9aNShIFmW" id="edit-in-eraser-github-link"><img alt="Edit in Eraser" src="https://firebasestorage.googleapis.com/v0/b/second-petal-295822.appspot.com/o/images%2Fgithub%2FOpen%20in%20Eraser.svg?alt=media&amp;token=968381c8-a7e7-472a-8ed6-4a6626da5501"></a></p>

<h1 align="center"><a href="https://github.com/ronknight/debounce-api">Email List Validation and Processing - Debounce-API</a></h1>
<h4 align="center">This project consists of two Python scripts that allow you to validate an email list using the Debounce.io API and download the processed file once it's ready.</h4>

<p align="center">
<a href="https://twitter.com/PinoyITSolution"><img src="https://img.shields.io/twitter/follow/PinoyITSolution?style=social"></a>
<a href="https://github.com/ronknight?tab=followers"><img src="https://img.shields.io/github/followers/ronknight?style=social"></a>
<a href="https://github.com/ronknight/ronknight/stargazers"><img src="https://img.shields.io/github/stars/BEPb/BEPb.svg?logo=github"></a>
<a href="https://github.com/ronknight/ronknight/network/members"><img src="https://img.shields.io/github/forks/BEPb/BEPb.svg?color=blue&logo=github"></a>
  <a href="https://youtube.com/@PinoyITSolution"><img src="https://img.shields.io/youtube/channel/subscribers/UCeoETAlg3skyMcQPqr97omg"></a>
<a href="https://github.com/ronknight/debounce-api/issues"><img src="https://img.shields.io/badge/contributions-welcome-brightgreen.svg?style=flat"></a>
<a href="https://github.com/ronknight/debounce-api/blob/master/LICENSE"><img src="https://img.shields.io/badge/License-MIT-yellow.svg"></a>
<a href="#"><img src="https://img.shields.io/badge/Made%20with-Python-1f425f.svg"></a>
<a href="https://github.com/ronknight"><img src="https://img.shields.io/badge/Made%20with%20%F0%9F%A4%8D%20by%20-%20Ronknight%20-%20red"></a>
</p>

<p align="center">
  <a href="#scripts">Scripts</a> •
  <a href="#setup">Setup</a> •
  <a href="#usage">Usage</a> •
  <a href="#dependencies">Dependencies</a> •
  <a href="#diagrams">Diagrams</a> •
</p>

---

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
2. Create a `.env`  file in the project directory and add the following environment variables:
    - `API_KEY` : Your Debounce.io API key.
    - `FTP_USERNAME` : Your FTP username.
    - `FTP_PASSWORD` : Your FTP password.
    ```bash
    API_KEY=Your_Debounce.io_API_key
    FTP_USERNAME=Your_FTP_username
    FTP_PASSWORD=Your_FTP_password
    ```
3. Install the required dependencies by running `pip install -r requirements.txt` .

## Usage
1. Run `create_batch.py`  with a CSV file containing email addresses as an argument to upload the file and validate the email list.
2. After running `create_batch.py` , it will print the list ID. Copy this ID.
3. Run `get_status.py`  with the list ID as an argument to check the status of the list and download the processed file when it's ready.

## Dependencies
This project uses the following Python libraries:

- `requests` : For making HTTP requests to the Debounce.io API.
- `python-dotenv` : For loading environment variables from a `.env`  file.
- `ftplib` : For uploading files to an FTP server.
These dependencies are listed in the `requirements.txt` file and can be installed using `pip install -r requirements.txt`.


<!-- eraser-additional-content -->
## Diagrams
<!-- eraser-additional-files -->
<a href="/README-Email List Validation and Processing-1.eraserdiagram" data-element-id="ysRZZJomEFdVS3vCbgn-p"><img src="/.eraser/6UvuHFuaM5A9aNShIFmW___3Jivg2tjMecMlrHwbIVIBR8f7U03___---diagram----0b9121b0074d8559aa650d74cac4ad53-Email-List-Validation-and-Processing.png" alt="" data-element-id="ysRZZJomEFdVS3vCbgn-p" /></a>
<!-- end-eraser-additional-files -->
<!-- end-eraser-additional-content -->
<!--- Eraser file: https://app.eraser.io/workspace/6UvuHFuaM5A9aNShIFmW --->