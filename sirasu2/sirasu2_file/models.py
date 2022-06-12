from datetime import datetime
from pydantic import BaseModel

class FileModel(BaseModel):
  id: str
  filename: str
  media_type: str
  path: str
  created_at: datetime
  updated_at: datetime
