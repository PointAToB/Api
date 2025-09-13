from http import HTTPStatus
from typing import Union

from django.db import IntegrityError
from django.http import HttpRequest
from ninja import Router
from .models import User
from .schema import CreateUser, RetrieveUser, Error, Success, UpdateUser

router = Router()

# Create User
@router.post('user')
def post(request: HttpRequest, user: Union[Error, CreateUser]):
    try:
        user = User(first_name=user.firstName, last_name=user.lastName, email=user.email)
        user.set_password(user.password)
        user.save()
    except IntegrityError: return Error(code=HTTPStatus.CONFLICT, message='Account already exists')


# Retrieve User
@router.get('user/{uid}', response=Union[Error, RetrieveUser])
def get(request: HttpRequest, uid: int):
    try:
        user = User.objects.get(id=uid)
    except User.DoesNotExist: return Error(code=HTTPStatus.NOT_FOUND, message="User not found")

    return user

# Update User
@router.put('user/{uid}', response=Union[Error, Success])
def put(request: HttpRequest, uid: int, fields: UpdateUser):
    try:
        user = User.objects.get(id=uid)
    except User.DoesNotExist: return Error(code=HTTPStatus.NOT_FOUND, message="User not found")

    _fields = { key: val for key, val in fields.dict(exclude_none=True).items() }

    if not _fields: return Error(code=HTTPStatus.BAD_REQUEST, message="No fields provided to update user")

    try:
        User.objects.filter(id=uid).update(**_fields)
    except User.DoesNotExist: return Error(code=HTTPStatus.NOT_FOUND, message="User not found")
    except IntegrityError: return Error(code=HTTPStatus.CONFLICT, message="Account with this email already exists")

