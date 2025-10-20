import csv
import io
import os
from openpyxl import Workbook, load_workbook
from PIL import Image
import ffmpeg
from pdf2docx import Converter
import tempfile
from pathlib import Path
from docx2pdf import convert

def process(FORMAT, file):

    DATA = {
            "pdf": "docx",
            "docx": "pdf",
            "mp4": "mp3",
            "jpg": "png",
            "csv": "xlsx",
            "xlsx": "csv"
        }

    if FORMAT == "csv": # OK!!

        try:
            wb = Workbook()
            worksheet = wb.active

            with open(file, "r", newline="") as input_file:
                reader = csv.reader(input_file, delimiter=',')
                for row in reader:
                    worksheet.append(row)

            wb.save(f"{file.rsplit('.')[0]}.xlsx")
        except Exception:
            print("CONVERTING ERROR (from csv to xlsx).")
        else:
            print("Success converting!!")


    if FORMAT == "xlsx": # OK!!

        try:
            wb = load_workbook(file)
            sh = wb.active

            with open(f"{file.rsplit('.')[0]}.csv", 'w', newline="") as output:
                csv_writer = csv.writer(output)
                for row in sh.iter_rows():
                    csv_writer.writerow([cell.value for cell in row])

        except Exception:
            print("Error CONVERTING excel to csv...")
        else:
            print("SUCCESSFULLY converted to csv!")


    if FORMAT == "jpg": # OK!!

        try:
            im = Image.open(file)
            out = f"{file.rsplit('.')[0]}.png"
            im.save(out)
        except Exception:
            print("Error CONVERTING jpg to png.")
        else:
            print("JPG to PNG convertion successful!!")


    if FORMAT == "mp4": # ОК!!

        output_audio_path = f'{file.rsplit('.')[0]}.mp3'

        try:
            ffmpeg.input(file).output(output_audio_path, acodec='libmp3lame').run(overwrite_output=True)
        except ffmpeg.Error as e:
            print(f"Error EXTRACTING AUDIO: {e.stderr.decode('utf8')}")
        except FileNotFoundError:
            print("Error: ffmpeg not found. Make sure ffmpeg is installed and in your system's PATH.")
        else:
            print("mp 4 TO 3 SUCCESSFULLY!!")


    if FORMAT == "docx": # OK!!

        result = f"{file.rsplit('.')[0]}.pdf"

        try:
            convert(file, result)
        except Exception as e:
            print(f"Error CONVERTING file: {e}")
        else:
            print("Damn it worked!!")


    if FORMAT == "pdf": # OK!!

        result = f"{file.rsplit('.')[0]}.docx"

        try:
            cv = Converter(file)
            cv.convert(result)
            cv.close()
        except Exception:
            print("Error CONVERTING pdf to docx...")
        else:
            print("CONVERTED successfully!!")
