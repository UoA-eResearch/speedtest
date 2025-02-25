#!/usr/bin/env python3

import os
import time
import smbclient
import pandas as pd
from dotenv import load_dotenv
load_dotenv()

# 100MB test file
testfile = os.urandom(1024 * 1024 * 100)

smbclient.ClientConfig(username=os.getenv("SMB_USERNAME"), password=os.getenv("SMB_PASSWORD"))
filepath = r"\\files.auckland.ac.nz\myhome\testfile"
s = time.time()
with smbclient.open_file(filepath, mode="wb") as f:
    f.write(testfile)
upload = 100 / (time.time() - s)
print(f"Upload: {round(upload, 2)}MB/s")
s = time.time()
with smbclient.open_file(filepath, mode="rb") as f:
    f.read()
download = 100 / (time.time() - s)
print(f"Download: {round(download, 2)}MB/s")
smbclient.remove(filepath)

df = pd.DataFrame({"upload": [upload], "download": [download], "timestamp": pd.Timestamp.now()})

if os.path.isfile("results.parquet"):
    existing_df = pd.read_parquet("results.parquet")
    pd.concat((existing_df, df)).to_parquet("results.parquet")
else:
    df.to_parquet("results.parquet")