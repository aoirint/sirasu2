from abc import ABC, abstractmethod
from typing import List, Optional

from .models import (
  UserModel,
  UserTokenPayloadModel,
)


class AuthRepositoryBase(ABC):
  @abstractmethod
  def migrate(self):
    """
      冪等性のある操作
    """
    pass

  @abstractmethod
  def to_payload(self, user: UserModel) -> UserTokenPayloadModel:
    pass

  @abstractmethod
  def from_payload(self, payload: UserTokenPayloadModel) -> Optional[UserModel]:
    pass


class AuthRepositoryMemory(AuthRepositoryBase):
  inited: bool = False
  users: List[UserModel] = None

  def migrate(self):
    assert not self.inited
    self.users = []
    self.inited = True

  def to_payload(self, user: UserModel) -> UserTokenPayloadModel:
    assert self.inited
    self.users.append(user.copy())

  def from_payload(self, payload: UserTokenPayloadModel) -> Optional[UserModel]:
    assert self.inited
    id = payload.user_id

    for user in self.users:
      if user.id == id:
        return user

    return None


class AuthRepositoryMySQL(AuthRepositoryBase):
  def __init__(self, database_uri: str):
    """
      Args:
        database_uri (str): mysql://user:password@hostname:3306/database
    """
    self.database_uri = database_uri

  def migrate(self):
    pass

  def to_payload(self, user: UserModel) -> UserTokenPayloadModel:
    pass

  def from_payload(self, payload: UserTokenPayloadModel) -> Optional[UserModel]:
    pass
