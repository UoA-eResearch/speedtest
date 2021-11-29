# speedtest
Python script to run speedtests against several file storage options supported by UoA

### Installation

`sudo pip3 install -r requirements.txt`  

Copy .env.example to .env and replace with your logins / tokens

### Running

`./run.py`

### Sample output

```
Running speedtest
Upload: 167.33 MB/s
Download: 203.19 MB/s
Single-threaded upload: 36.93 MB/s
Single-threaded download: 67.02 MB/s
Testing Unifiles
Upload: 47.36MB/s
Download: 53.42MB/s
Testing Dropbox
Upload: 13.09MB/s
Download: 12.14MB/s
```