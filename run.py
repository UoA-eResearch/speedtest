#!/usr/bin/env python3

import os
import time
from dotenv import load_dotenv
load_dotenv()

# 100MB test file
testfile = os.urandom(1024 * 1024 * 100)

def test_speedtest():
    print("Running speedtest")
    import speedtest
    s = speedtest.Speedtest()
    s.get_servers()
    s.get_best_server()
    s.download()
    s.upload()
    r = s.results.dict()
    print(f"Upload: {round(r['upload'] / 1024 / 1024 / 8, 2)} MB/s")
    print(f"Download: {round(r['download'] / 1024 / 1024 / 8, 2)} MB/s")
    s.download(threads=1)
    s.upload(threads=1)
    r = s.results.dict()
    print(f"Single-threaded upload: {round(r['upload'] / 1024 / 1024 / 8, 2)} MB/s")
    print(f"Single-threaded download: {round(r['download'] / 1024 / 1024 / 8, 2)} MB/s")
    if r['ping'] != 1800000.0:
        print(f"Ping: {r['ping']}ms")

def test_unifiles():
    print("Testing Unifiles")
    import smbclient
    smbclient.ClientConfig(username=os.getenv("SMB_USERNAME"), password=os.getenv("SMB_PASSWORD"))
    filepath = r"\\files.auckland.ac.nz\myhome\100MB"
    s = time.time()
    with smbclient.open_file(filepath, mode="wb") as f:
        f.write(testfile)
    print(f"Upload: {round(100 / (time.time() - s), 2)}MB/s")
    s = time.time()
    with smbclient.open_file(filepath, mode="rb") as f:
        f.read()
    print(f"Download: {round(100 / (time.time() - s), 2)}MB/s")
    smbclient.remove(filepath)

def test_dropbox():
    print("Testing Dropbox")
    import dropbox
    from dropbox.files import WriteMode
    with dropbox.Dropbox(os.getenv("DROPBOX_TOKEN")) as dbx:
        s = time.time()
        filepath = "/100MB"
        dbx.files_upload(testfile, filepath, mode=WriteMode('overwrite'))
        print(f"Upload: {round(100 / (time.time() - s), 2)}MB/s")
        s = time.time()
        dbx.files_download_to_file("100MB", filepath)
        print(f"Download: {round(100 / (time.time() - s), 2)}MB/s")
        dbx.files_delete(filepath)
        os.unlink("100MB")

def test_gdrive():
    print("Testing Google Drive")
    from pydrive2.auth import GoogleAuth
    from pydrive2.drive import GoogleDrive
    gauth = GoogleAuth()
    gauth.CommandLineAuth()
    drive = GoogleDrive(gauth)
    s = time.time()
    file = drive.CreateFile({'title': '100MB'})
    file.SetContentString(str(testfile))
    file.Upload()
    print(f"Upload: {round(100 / (time.time() - s), 2)}MB/s")
    s = time.time()
    file = drive.CreateFile({'id': file["id"]})
    file.GetContentString()
    print(f"Download: {round(100 / (time.time() - s), 2)}MB/s")
    file.Delete()

test_speedtest()
test_unifiles()
test_dropbox()
test_gdrive()