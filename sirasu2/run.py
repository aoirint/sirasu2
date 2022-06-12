from datetime import datetime
from typing import List
from uuid import UUID
import uuid
from fastapi import FastAPI, Response, UploadFile
from sirasu2_file.models import (
  FileModel,
)
from sirasu2_auth.auth import Auth
import os

import dotenv
dotenv.load_dotenv()

UPLOAD_ROOT = os.environ['UPLOAD_ROOT']
JWT_SECRET = os.environ['JWT_SECRET']

app = FastAPI(
  title='sirasu mock',
  version='0.0.0',
)

auth = Auth(secret=JWT_SECRET)

@app.get('/files', response_model=List[FileModel])
async def get_files():
  pass

@app.get('/files/raw/{file_id}')
async def get_file_raw_by_id(file_id: UUID):
  # TODO:
  content = b''
  return Response(content=content, media_type='application/octet-stream')

@app.get('/files/{file_id}', response_model=FileModel)
async def get_file_by_id(file_id: UUID):
  pass

@app.post('/files', response_model=FileModel)
async def post_file(file: UploadFile):
  file_id = uuid.uuid4()
  now = datetime.now()
  pass
