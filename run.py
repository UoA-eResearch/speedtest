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

test_speedtest()
test_unifiles()
test_dropbox()