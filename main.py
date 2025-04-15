# import package
from fastapi import FastAPI, HTTPException, Header
import pandas as pd

password = "secret123"

# create FastAPI object
app = FastAPI()

# endpoint -> alamat tertentu yang bisa diakses oleh client
# create endpoint untuk mendapatkan data di halaman awal/utama


@app.get("/")
def getData():  # function handler -> untuk menghandle request dari endpoint tertentu
    return {
        "message": "hello world !!!"
    }

# endpoint untuk ngambil data dari csv


@app.get("/data")
def getCsv():
    # 1. baca data dari csv
    df = pd.read_csv('data.csv')

    # 2. tampilkan response berupa data csv menjadi json.
    return df.to_dict(orient="records")


@app.get("/data/{name}")
def getDataByName(name: str):
    # 1. baca data dari csv
    df = pd.read_csv('data.csv')

    # 2. filter data by name
    result = df[df['name'] == name]

    # check apakah hasil filter (ada)
    if len(result) > 0:
        # 3. tampilkan response berupa data csv menjadi json.
        return result.to_dict(orient="records")
    else:
        # tampilkan pesan error
        raise HTTPException(
            status_code=404, detail="data " + name + " tidak ditemukan")


@app.delete("/data/{name}")
def deleteDataByName(name: str, api_key: str = Header(None)):
    # check auth
    if api_key != None and api_key == password:
        # 1. baca data dari csv
        df = pd.read_csv('data.csv')

        # 2. filter data by name
        result = df[~(df['name'] == name)]

        # 3. replace csv existing -> data yang difilter akan hilang
        result.to_csv('data.csv', index=False)

        # 4. tampilkan response
        return {"message": "data berhasil ditambahkan"}
    else:
        raise HTTPException(status_code=403, detail="password salah!")
