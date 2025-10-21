"""
Controller.

ЧТО ДАЛЬШЕ:
--- 1. загрузить РАБОТАЮЩИЙ код на гитхаб ---
-- 2. почистить ненужные импорты, комментарии, костыли --
-- 3. сделать относительные ссылки для дальнейшей транспортации в докер --
-- 4. написать тесты (end-to-end) и отредактировать код для учёта всех случаев --
-- 5. написать уместные комментарии в код --
6. запаковать всё в докер и обновить на гитхабе
7. написать readme для гитхаба

"""

import os
import shutil
import asyncio
from fastapi import FastAPI, UploadFile, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from format_change.all_processing import process

app = FastAPI()

picked_format = "EMPTY"
name = "EMPTY"
data = {
            "pdf": "docx",
            "docx": "pdf",
            "mp4": "mp3",
            "jpg": "png",
            "csv": "xlsx",
            "xlsx": "csv"
        }
file_processed_event = asyncio.Event()


@app.get("/")
def root():

    """
    Program's front.
    """

    return FileResponse("statics/index.html")


@app.post("/uploadformat")
async def format_save(selection: dict):
    """
    Endpoint that:
    1. receives original file format, selected by user manually, 
    2. saves a format globally for reusage in other endpoints. 
    """

    global picked_format

    try:
        picked_format = selection["choice"]
    except ValueError:
        print("Error SAVING FORMAT: data lost on client-side.")
    else:
        print("Successful FORMAT SAVE.")


@app.post("/uploadfile")
async def upload_and_convert(document: UploadFile):
    """
    Endpoint that:
    1. receives a file uploaded by user,
    2. saves its name for reusage in other endpoints,
    3. validates file' format:
    3.1. format should be within program's ability to format,
    3.2. actual format should match the format selection made by user, which triggers converting;
    4. saves file as it is,
    5. converts it ("all_processing" module),
    6. then sets globally declared asyncio event' flag, allowing next endpoint to auto-download (since it becomes possible after converting's done). 
    """

    global name

    name = ''.join(document.filename.rsplit('\\')[-1].rsplit(".")[0].split())
    actual_format = document.filename.rsplit('\\')[-1].rsplit(".")[1]

    path_to_original = f'files_to_process\\{name}.{actual_format}'

    if actual_format not in data or actual_format != picked_format:
        raise HTTPException(
            status_code=400,
            detail={
                "message": "Формат файла не соответствует формату, выбранному в списке. Выберите файл снова.",
                "error_code": "INVALID_VALUE",
                "suggestions": ["Проверьте соответствие форматов."]
            }
        )

    try:
        with open(path_to_original, 'wb') as saved:
            shutil.copyfileobj(document.file, saved)
    except Exception as saving_error:
        print(f"Error SAVING file: {saving_error}")
    
    try:
        process(picked_format, path_to_original)
        file_processed_event.set()
    except Exception as converting_error:
        print(f"Error CONVERTING file: {converting_error}")

    print("Successful file CONVERTING.")


@app.get("/download")
async def autodownload():
    """
    Endpoint that:
    1. awaits until converted file is created, 
    2. instantly sends it to client side' awaiting Javascript function.
    """

    await file_processed_event.wait()

    name_with_format = f"{name}.{data[picked_format]}"
    path_to_final = f"files_to_process\\{name_with_format}"
    print("(Almost) successful DOWNLOADING to client's.")

    return FileResponse(
        path=path_to_final,
        media_type=f"application/{data[picked_format]}",
        filename=name_with_format,
        headers={"Content-Disposition": f"attachment; filename={name_with_format}"}
    )


@app.post("/cleancache")
async def cleanup(callback: dict):
    """
    Endpoint that:
    1. receives a callback from Javascript function that downloads file in browser, once it finishes successfully and the program's objective is reached,
    2. cleans the folder used for temporary file saving, clearing memory. 
    """

    if callback["status"] == "success":
        os.remove(f"files_to_process\\{name}.{picked_format}")
        os.remove(f"files_to_process\\{name}.{data[picked_format]}")

    print("Successful cleanup.")


app.mount("/", StaticFiles(directory="statics", html=True))
