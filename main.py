import io
import json
import os
from datetime import datetime
from io import BytesIO
from typing import Union

import pandas as pd
from fastapi import FastAPI, File, UploadFile
from mockpyroclient.utils import convertFromNumber
from PIL import Image

app = FastAPI()

os.makedirs(f"data/heartbeat/", exist_ok=True)
os.makedirs(f"data/medias/", exist_ok=True)

if not os.path.isfile("data/data.csv"):
    df = pd.DataFrame(
        columns=["device_id", "media_id", "is_alert", "file_path", "date"]
    )
    df.to_csv("data/data.csv")


@app.get("/")
def read_root():
    return {"Mock": "Pyro-api"}


@app.put("/device/heartbeat/{device_id}")
def heartbeat(device_id: int):

    with open(f"data/heartbeat/{device_id}.txt", "a") as f:
        f.write(str(datetime.utcnow()) + "\n")
    return {"device_id": device_id}


@app.post("/device/create_media_from_device/{device_id}")
def create_media_from_device(device_id: int):

    df = pd.read_csv("data/data.csv", index_col=0)
    media_id = len(df)
    new_row = pd.DataFrame(
        {
            "device_id": convertFromNumber(int(device_id)),
            "media_id": media_id,
            "is_alert": 0,
            "file_path": None,
            "date": str(datetime.utcnow()),
        },
        index=[0],
    )
    df = pd.concat([df.loc[:], new_row]).reset_index(drop=True)
    df.to_csv("data/data.csv")
    return {"id": media_id}


@app.post("/device/send_alert_from_device/{media_id}")
def send_alert_from_device(media_id: int):

    df = pd.read_csv("data/data.csv", index_col=0)
    df.at[media_id,"is_alert"]=1
    df.to_csv("data/data.csv")
    return {"id": media_id}


@app.post("/device/upload_media/{media_id}")
def upload_media(
    media_id: int,
    file: UploadFile = File(...),
):

    df = pd.read_csv("data/data.csv", index_col=0)
    row = df.iloc[media_id]
    device_id = row["device_id"]
    im = Image.open(BytesIO(file.file.read()))
    os.makedirs(f"data/medias/{device_id}", exist_ok=True)
    file_path = f"data/medias/{device_id}/{str(row['media_id']).zfill(8)}.jpg"
    im.save(file_path)
    df.at[media_id,"file_path"]=file_path
    df.to_csv("data/data.csv")
    return {"id": media_id}
