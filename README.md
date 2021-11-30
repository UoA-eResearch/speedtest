# speedtest
Python script to run speedtests against several file storage options supported by UoA

### Installation

`sudo pip3 install -r requirements.txt`  

Copy .env.example to .env and replace with your logins / tokens. Alternatively, set environment variables.

### Running

`./run.py`

### Sample output

```
Running speedtest
Upload: 184.72 MB/s
Download: 233.23 MB/s
Single-threaded upload: 38.34 MB/s
Single-threaded download: 70.67 MB/s
Testing Unifiles
Upload: 51.7MB/s
Download: 44.85MB/s
Testing Dropbox
Upload: 13.93MB/s
Download: 22.42MB/s
Testing Google Drive
Upload: 5.05MB/s
Download: 7.86MB/s
Testing OneDrive
Upload: 5.72MB/s
Download: 5.44MB/s
```