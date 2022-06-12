import jwt
from pydantic import parse_obj_as

from .repositories import AuthRepositoryBase

from .models import (
  UserModel,
  UserTokenPayloadModel,
)


class Auth:
  def __init__(self, secret: str, repository: AuthRepositoryBase):
    self.secret = secret
    self.repository = repository

  def decode_user_token(self, encoded_jwt: str) -> UserModel:
    secret = self.secret
    repository = self.repository

    payload_obj = jwt.decode(encoded_jwt, secret, algorithms=['HS256'])
    payload = parse_obj_as(UserTokenPayloadModel, payload_obj)

    user = repository.from_payload(payload=payload)
    return user

  def encode_user_token(self, user: UserModel) -> str:
    secret = self.secret
    repository = self.repository

    payload = repository.to_payload(user=user)
    payload_obj = payload.dict()

    token = jwt.encode(payload_obj, secret, algorithm='HS256')
    return token
