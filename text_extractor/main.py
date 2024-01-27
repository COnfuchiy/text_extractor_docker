import http
import os

from docx2txt import docx2txt
from fastapi import FastAPI, File, UploadFile
from fastapi import Response

from pdf_extract import PDFTextExtractor

app = FastAPI()


@app.post("/uploadfile/")
async def create_upload_file(response: Response, file: UploadFile = File(...)):
    with open(file.filename, "wb+") as file_object:
        file_object.write(file.file.read())
    _, file_ext = os.path.splitext(file.filename)
    match file_ext:
        case '.pdf':
            pdf_extractor = PDFTextExtractor(file.filename)
            file_text = pdf_extractor.extract()
        case '.docx':
            file_text = docx2txt.process(file.filename)
        case _:
            os.remove(file.filename)
            response.status_code = 400
            return {"file text": "", "success": False, "error": "file is not a word or pdf file"}
    os.remove(file.filename)
    return {"file text": file_text, "success": True, "error": ""}

