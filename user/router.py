from http import HTTPStatus
from typing import Union
from ninja_jwt.authentication import JWTAuth
from django.db import IntegrityError
from django.http import HttpRequest
from ninja import Router
from .models import User
from .schema import CreateUser, RetrieveUser, UpdateUser, Error


router = Router()

# Predefined Endpoints: token/pair (Initial Authentication) , token/refresh (Refresh Access Token), token/verify (Verify token is not expired)

# Create User
@router.post('user', response={
    HTTPStatus.OK: CreateUser,
    HTTPStatus.CONFLICT: Error
})
def post(request: HttpRequest, user: CreateUser):
    try:
        user = User(first_name=user.firstName, last_name=user.lastName, email=user.email)
        user.set_password(user.password)
        user.save()
    except IntegrityError: return Error(message='Account already exists')


# Retrieve User
@router.get('user/{uid}', auth=JWTAuth(), response={
    HTTPStatus.OK: RetrieveUser,
    HTTPStatus.NOT_FOUND: Error
})
def get(request: HttpRequest, uid: int):
    try:
        user = User.objects.get(id=uid)
    except User.DoesNotExist: return Error(message="User not found")

    return user


# Update User
@router.put('user/{uid}', auth=JWTAuth(), response={
    HTTPStatus.OK: None,
    HTTPStatus.NOT_FOUND: Error,
    HTTPStatus.CONFLICT: Error,
    HTTPStatus.BAD_REQUEST: Error
})
def put(request: HttpRequest, uid: int, fields: UpdateUser):
    try:
        user = User.objects.get(id=uid)
    except User.DoesNotExist: return Error(message="User not found")

    _fields = { key: val for key, val in fields.dict(exclude_none=True).items() }

    if not _fields: return Error(message="No fields provided to update user")

    try:
        User.objects.filter(id=uid).update(**_fields)
    except IntegrityError: return Error(message="Account with this email already exists")


# Delete User
@router.delete('user/{uid}', auth=JWTAuth(), response={
    HTTPStatus.OK: None,
    HTTPStatus.NOT_FOUND: Error,
})
def delete(request: HttpRequest, uid: int):
    try:
        user = User.objects.get(id=uid)
        user.delete()
    except User.DoesNotExist: return Error(message="User not found")

    return None




