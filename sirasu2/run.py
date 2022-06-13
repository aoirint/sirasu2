from datetime import datetime, timezone
import time
from typing import List
from uuid import UUID, uuid4
import uuid
from fastapi import FastAPI, Response, UploadFile
import jwt
from pydantic import BaseModel, parse_obj_as
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

# 認証付きVODサーバ
# Database
class Video(BaseModel):
  id: UUID

# Request/Response Model
class UploadingVideoTicket(BaseModel):
  video_id: UUID

class Token(BaseModel):
  sub: UUID # user id
  # int is parsed as UNIX time, but ambiguous (https://pydantic-docs.helpmanual.io/usage/types/#datetime-types)
  iat: int # issued_at UTC seconds
  exp: int # expiration UTC seconds

  @property
  def iat_datetime(self):
    return datetime.fromtimestamp(self.iat, timezone.utc)
  @property
  def exp_datetime(self):
    return datetime.fromtimestamp(self.exp, timezone.utc)

def decode_token(encoded_token: str, secret: str) -> Token:
  obj = jwt.decode(encoded_token, secret, algorithms=['HS256'])
  token = parse_obj_as(Token, obj)

  utc_now = datetime.now(timezone.utc)

  if token.exp < utc_now:
    raise Exception('Token expired')

  return token

@app.get('/videos/{video_id}/playlist.m3u8')
async def get_vod_playlist_file(video_id: UUID):
  return Response(content=content, media_type='application/vnd.apple.mpegurl')

@app.get('/videos/{video_id}/{stream_index}.ts')
async def get_vod_stream_file(video_id: UUID, stream_index: str):
  return Response(content=content, media_type='video/MP2T')

@app.get('/videos/{video_id}/video.mp4')
async def get_video_file(video_id: UUID, stream_index: str):
  return Response(content=content, media_type='video/mp4')

@app.post('/videos/upload', response_model=UploadingVideoTicket)
async def upload_video(file: UploadFile):
  video_id = uuid4()
  now = datetime.now()

  return UploadingVideoTicket(
    video_id=video_id,
  )
