#!/usr/bin/env python3
# pylint: disable=missing-module-docstring,missing-function-docstring,import-outside-toplevel
# type: ignore
import argparse
import os
import time

import passpy
from dotenv import load_dotenv

GPG_BIN = (
    "/opt/homebrew/bin/gpg"  # Note this is for my mac and needs to point to GPG binary
)
store = passpy.Store(gpg_bin=GPG_BIN)
load_dotenv()

# 100MB test file
testfile = os.urandom(1024 * 1024 * 100)
# Include a 10GB file for S3 multipart
# bigtestfile = os.urandom(1024 * 1024 * 1024 * 10)


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
    if r["ping"] != 1800000.0:
        print(f"Ping: {r['ping']}ms")


def test_unifiles():
    print("Testing Unifiles")
    import smbclient

    smbclient.ClientConfig(
        username=os.getenv("SMB_USERNAME"), password=store.get_key("SMB_password")
    )
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
        dbx.files_upload(testfile, filepath, mode=WriteMode("overwrite"))
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
    file = drive.CreateFile({"title": "100MB"})
    file.SetContentString(str(testfile))
    file.Upload()
    print(f"Upload: {round(100 / (time.time() - s), 2)}MB/s")
    s = time.time()
    file = drive.CreateFile({"id": file["id"]})
    file.GetContentString()
    print(f"Download: {round(100 / (time.time() - s), 2)}MB/s")
    file.Delete()


def test_onedrive():
    print("Testing OneDrive")
    import onedrivesdk

    redirect_uri = "http://localhost:8000/callback"
    client_secret = "86l7Q~zwmQ2Qc5zWHf9pWWUGBW2-6RxYP.r.p"
    client_id = "0cda2cfb-622f-49c4-b48c-9a772db82f27"
    api_base_url = "https://api.onedrive.com/v1.0/"
    scopes = ["onedrive.readwrite"]

    http_provider = onedrivesdk.HttpProvider()
    auth_provider = onedrivesdk.AuthProvider(
        http_provider=http_provider, client_id=client_id, scopes=scopes
    )

    client = onedrivesdk.OneDriveClient(api_base_url, auth_provider, http_provider)
    try:
        auth_provider.load_session()
        client.item(drive="me", id="root").children.get()
    except Exception:
        auth_url = auth_provider.get_auth_url(redirect_uri)
        # Ask for the code
        print("Paste this URL into your browser, approve the app's access.")
        print('Copy everything in the address bar after "code=", and paste it below.')
        print(auth_url)
        code = input("Paste code here: ")
        auth_provider.authenticate(code, redirect_uri, client_secret)
        auth_provider.save_session()
    with open("100MB", "wb") as f:
        f.write(testfile)
    s = time.time()
    file = client.item(drive="me", id="root").children["100MB"].upload("100MB")
    print(f"Upload: {round(100 / (time.time() - s), 2)}MB/s")
    s = time.time()
    client.item(drive="me", id=file.id).download("100MB")
    print(f"Download: {round(100 / (time.time() - s), 2)}MB/s")
    client.item(id=file.id).delete()
    os.unlink("100MB")


def test_localdisk():
    print("Testing local disk")
    s = time.time()
    with open("100MB", "wb") as f:
        f.write(testfile)
    print(f"Write speed: {round(100 / (time.time() - s), 2)}MB/s")
    s = time.time()
    with open("100MB", "rb") as f:
        f.read()
    print(f"Read speed: {round(100 / (time.time() - s), 2)}MB/s")
    os.unlink("100MB")


def test_s3():
    import uuid

    import boto3

    print("Testing S3 buckets")
    with open("smallfile", "wb") as f:
        f.write(testfile)
    # with open("bigfile", "wb") as f:
    #    f.write(bigtestfile)
    s3_user = store.get_key("VAST_test/user")
    s3_user = s3_user.replace("\n", "")
    s3_password = store.get_key("VAST_test/password")
    s3_password = s3_password.replace("\n", "")
    s3_endpoint = os.getenv("S3_ENDPOINT")
    s3_port = os.getenv("S3_PORT")
    test_bucket = f'{os.getenv("S3_BUCKET")}{str(uuid.uuid4())}'
    client = boto3.client(
        "s3",
        aws_access_key_id=s3_user,
        aws_secret_access_key=s3_password,
        enpoint_url=f"{s3_endpoint}:{s3_port}",
    )
    print(f"Creating bucket: {test_bucket}")
    bucket = client.create_bucket(test_bucket)
    print("Testing with 100MB file")
    s = time.time()
    client.upload_file(Filename="smallfile", Bucket=bucket, Key="Small_Test.dat")
    print(f"Upload Speed: {round(100 / (time.time() - s, 2))}MB/s")
    s = time.time()
    client.download_file(bucket, "Small_Test.dat", "smallfile")
    print(f"Download Speed: {round(100 / (time.time() - s, 2))}MB/s")
    os.unlink("smallfile")
    # os.unlink("bigfile")


parser = argparse.ArgumentParser(
    description="Scripts to test the performance of UoA services."
)
parser.add_argument(
    "-u",
    "--unifiles",
    help="Test file transfer speed on UniFiles",
    action="store_true",
    default=False,
)
parser.add_argument(
    "-d",
    "--dropbox",
    help="Test file transfer speed on DropBox",
    action="store_true",
    default=False,
)
parser.add_argument(
    "-g",
    "--gdrive",
    help="Tests file transfer speed on Google Drive",
    action="store_true",
    default=False,
)
parser.add_argument(
    "-o",
    "--onedrive",
    help="Test file transfer speed on OneDrive",
    action="store_true",
    default=False,
)
parser.add_argument(
    "-s",
    "--s3",
    help="Test file transfer speed on an S3 bucket",
    action="store_true",
    default=False,
)

args = parser.parse_args()

if args.s3:
    test_s3()
# test_localdisk()
# test_speedtest()
# test_unifiles()
# test_dropbox()
# test_gdrive()
# test_onedrive()
