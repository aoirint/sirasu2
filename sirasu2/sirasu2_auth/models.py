from datetime import datetime
from typing import List
from pydantic import BaseModel


class UserModel(BaseModel):
  id: str
  group_ids: List[str]
  created_at: datetime
  updated_at: datetime

class GroupModel(BaseModel):
  id: str
  created_at: datetime
  updated_at: datetime

class UserTokenPayloadModel(BaseModel):
  user_id: str
  group_ids: List[str]
