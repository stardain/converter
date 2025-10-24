# file converter app

A simple converter I've built to get a grasp of fullstack application development. 
All processing is done by libraries listed below. 

<br>

## description

### converting capabilities
- CSV to XLSX (+ vica verca) — done by standard **csv** and **openpyxl**
- JPG to PNG, for creating transparent elements later — done by **PIL**
- MP4 to MP3, for illegal music listening — done by **ffmpeg**
- DOCX to PDF (+ vica verca) — done by **pdf2docx** and **docx2pdf**

### development notes

- I used FASTAPI.
- Most endpoints strictly depend on other endpoints' results. Part of the realization depend on JS' synchronous nature, part is synchronized by awaiting asyncio' event, part waits for client side to send a callback.
  
### roadmap
- client sends an original file and the choosen format (that triggers correct convertation later) —>
- format is validated by checking an actual format alongside a choosen format —>
- an original file is temporarily saved, since it's the easiest way to convert without workarounds —>
- the convertation happens, a converted file is also temporarily saved —>
- the moment converting is done, a converted file is pushed to client side and autodownloads, by using a blob for imitating user activity —>
- when downloading is done, server side receives a callback and cleans up the folder both files were temporarily saved at.

### client side ~baby~ implementation includes
-   second dropdown options changing depending on first dropdown' choice
-   load button changing text on file's filename when the file is selected, and changing color and text when the wrong format file is selected, making a way to reselect a file not impossible to find
-   roses and emoji. 

 <br>

## how to install and run

0. The Docker image is on Docker Hub, at "stardain/converter-app" repository.
1. Pull an image with any open port on your machine by using `docker run -dp 0.0.0.0:yourport:8000 stardain/converter-app`.
2. Run a container by using `docker run stardain/converter-app:latest`.
