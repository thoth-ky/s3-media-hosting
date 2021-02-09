from fastapi import FastAPI, File, UploadFile, Form, status, Response
from typing import Optional
from pydantic import BaseModel
from decouple import config
# local imports
from utils.upload_file import upload_file_object, create_presigned_url


app = FastAPI()
BUCKET_NAME = config('S3_BUCKET_NAME')


class FileObject(BaseModel):
    key: str
    expiration: int = 3600


@app.get("/")
def read_root():
    return {"message": "I'm up!!"}


@app.post("/upload", status_code=status.HTTP_201_CREATED)
async def upload_file(folder_path: str = Form(...), file: UploadFile = File(...), response: Response = 201):
    filename = file.filename
    key = f"{folder_path}/{filename}"
    response = upload_file_object(file_obj=file.file, bucket=BUCKET_NAME, key=key)
    if response:
        response = {
            "status": "Successfully uploaded!",
            "filename": filename,
            "key": key,
            "link_valid_for_a_day": create_presigned_url(bucket_name=BUCKET_NAME, key=key)
        }
        return response
    else:
        response.status_code = status.HTTP_417_EXPECTATION_FAILED
        return {
            "status": "Upload failed"
        }


@app.post('/object_link')
async def get_presigned_link(file: FileObject):
    key = file.key
    expiration = file.expiration
    link = create_presigned_url(bucket_name=BUCKET_NAME, key=key, expiration=expiration)
    return {
        "link": link
    }
