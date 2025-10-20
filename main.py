"""
main file duh

ЧТО ДАЛЬШЕ:
--- 1. загрузить РАБОТАЮЩИЙ код на гитхаб ---
2. почистить ненужные импорты, комментарии, костыли
3. сделать относительные ссылки для дальнейшей транспортации в докер
-- 4. написать тесты (end-to-end) и отредактировать код для учёта всех случаев --
5. написать уместные комментарии в код
6. запаковать всё в докер и обновить на гитхабе
7. написать readme для гитхаба

"""

from typing import Annotated
import os
import shutil
import asyncio
import time
import shutil
import json
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from format_change.all_processing import process

app = FastAPI()

user = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

UPLOAD_DIRECTORY = r"D:\Desktop\projects\fileconv\files_to_process"
FORMAT = "EMPTY"
NAME = "EMPTY"

file_processed_event = asyncio.Event()

DATA = {
            "pdf": "docx",
            "docx": "pdf",
            "mp4": "mp3",
            "jpg": "png",
            "csv": "xlsx",
            "xlsx": "csv"
        }

origins = [
        "http://localhost:8000", # Example origin, adjust as needed
        # Add other origins if your frontend is hosted elsewhere
    ]

app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

@app.get("/")
def root():

    """just a root"""

    return FileResponse("statics/index.html")


@app.post("/format/")
async def transfer_format(extention: dict):
    """
    Endpoint to receive a format for a file and make it into a global variable.
    """

    # сохранение эксекьютит быстрее чем обновляется нужный формат файла

    global FORMAT

    try:
        #format_info = json.loads(extention)
        FORMAT = extention["choice"]
    except Exception:
        print("Something went wrong with changing FORMAT...")
    else:
        print(f"Stage 1, FORMAT TRANSFER, successful.")
        return {"format": FORMAT}


@app.post("/uploadfile/")
async def create_upload_file(
    document: Annotated[UploadFile, File()]):
    """
    Endpoint to receive an uploaded and processed file.
    """

    global FORMAT
    global NAME

    NAME = document.filename.rsplit('\\')[-1].rsplit(".")[0]
    real_format = document.filename.rsplit('\\')[-1].rsplit(".")[1]

    #while FORMAT == "EMPTY":
    #    time.sleep(0.5)

    address_before = f'D:\\Desktop\\projects\\fileconv\\files_to_process\\{''.join(document.filename.split())}'

    print(real_format, FORMAT, DATA[FORMAT])

    if real_format not in DATA or real_format != FORMAT:
        raise HTTPException(
            status_code=400,
            detail={
                "message": "Формат файла не соответствует формату, выбранному в списке. Выберите файл снова.",
                "error_code": "INVALID_VALUE",
                "suggestions": ["Проверьте соответствие форматов."]
            }
        )


    try:
        
        with open(address_before, 'wb') as saved:
            shutil.copyfileobj(document.file, saved)

        process(FORMAT, address_before)
        file_processed_event.set()
        
    except Exception as e:
        print(f"Error SAVING file: {e}")
    else:
        print("Stage 2, CONVERT AND SAVE, successful.")
        return {"address": address_before}


@app.get("/download-processed-file")
async def download_processed_file():
    """
    Downloads converted file to client's. 
    """

    await file_processed_event.wait()

    file_name = f"{''.join(NAME.split())}.{DATA[FORMAT]}"
    for_sending = f"D:\\Desktop\\projects\\fileconv\\files_to_process\\{file_name}"

    if not os.path.exists(for_sending):
        return {"message": f"File {for_sending} not found"}, 404

    print("Stage 3, DOWNLOADING TO CLIENT'S, successful.")

    return FileResponse(
        path=for_sending,
        media_type=f"application/{DATA[FORMAT]}",
        filename=file_name,
        headers={"Content-Disposition": f"attachment; filename={file_name}"}
    )

@app.post("/cleancache")
async def cleanup(callback: dict):
    """
    Clean a working folder afterwards.
    """

    name_actual = ''.join(NAME.split())

    if callback["status"] == "success":
        os.remove(f"D:\\Desktop\\projects\\fileconv\\files_to_process\\{name_actual}.{FORMAT}")
        os.remove(f"D:\\Desktop\\projects\\fileconv\\files_to_process\\{name_actual}.{DATA[FORMAT]}")
        # D:\Desktop\projects\fileconv\files_to_process\tududu.jpg

app.mount("/", StaticFiles(directory="statics", html=True), name="design")
