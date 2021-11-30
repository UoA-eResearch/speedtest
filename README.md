# speedtest
Python script to run speedtests against several file storage options supported by UoA

### Installation

`sudo pip3 install -r requirements.txt`  

Copy .env.example to .env and replace with your logins / tokens. Alternatively, set environment variables. You can get a Dropbox token at https://www.dropbox.com/developers/apps. A Scoped App Folder with files.content.write and files.content.read permissions should work fine.

### Running

`./run.py`

### Sample output

```
Testing local disk
Write speed: 1336.11MB/s
Read speed: 1644.35MB/s
Running speedtest
Upload: 184.35 MB/s
Download: 152.19 MB/s
Single-threaded upload: 37.81 MB/s
Single-threaded download: 73.13 MB/s
Testing Unifiles
Upload: 35.03MB/s
Download: 40.9MB/s
Testing Dropbox
Upload: 18.83MB/s
Download: 24.19MB/s
Testing Google Drive
Upload: 5.06MB/s
Download: 8.22MB/s
Testing OneDrive
Upload: 9.57MB/s
Download: 5.57MB/s
```