from http import HTTPStatus

from django.contrib.auth import authenticate
from ninja_jwt.authentication import JWTAuth
from django.http import HttpRequest, HttpResponse
from ninja import Router
from ninja_jwt.tokens import AccessToken, RefreshToken

from .models import User
from .schema import CreateUser, RetrieveUser, UpdateUser, Error, UserLoginIn, UserLoginOut

router = Router()

# Predefined Endpoints: token/pair (Initial Authentication) , token/refresh (Refresh Access Token), token/verify (Verify token is not expired)

# Custom login endpoint
@router.post('login', response={
    HTTPStatus.OK: UserLoginOut,
    HTTPStatus.NOT_FOUND: Error,
    HTTPStatus.BAD_REQUEST: Error,
})
def login(request: HttpRequest, user: UserLoginIn):
    # Verifies user with specified email exists in the database
    try:
        User.objects.get(email=user.email)
    except User.DoesNotExist: return HTTPStatus.NOT_FOUND, Error(message='User not found')

    user = authenticate(email=user.email, password=user.password)
    if user:
        refresh = RefreshToken.for_user(user)
        access = AccessToken.for_user(user)
        return HTTPStatus.OK, UserLoginOut(access=str(access), refresh=str(refresh))

    return HTTPStatus.BAD_REQUEST, Error(message='Invalid credentials')


# Create User
@router.post('user', response={
    HTTPStatus.OK: RetrieveUser,
    HTTPStatus.CONFLICT: Error,
    HTTPStatus.BAD_REQUEST: Error
})
def post(request: HttpRequest, user: CreateUser):
    # Check that none of the value fields are empty strings
    if user.firstName == '' or user.lastName == '' or user.email == '' or user.password == '':
        return HTTPStatus.BAD_REQUEST, Error(message='Fields cannot be an empty string')

    # Check if user with specified email already exists
    try:
        User.objects.get(email=user.email)
    except User.DoesNotExist:
        user = User.objects.create_user(email=user.email, password=user.password, firstName=user.firstName, lastName=user.lastName)
        return HTTPStatus.OK, user

    return HTTPStatus.CONFLICT, Error(message='Account with this email already exists')



# Retrieve User
@router.get('user', auth=JWTAuth(), response={
    HTTPStatus.OK: RetrieveUser,
    HTTPStatus.NOT_FOUND: Error
})
def get(request: HttpRequest):
    try:
        user = request.user
    except User.DoesNotExist: return HTTPStatus.NOT_FOUND, Error(message="User not found")

    return HTTPStatus.OK, user


# Update User
@router.put('user', auth=JWTAuth(), response={
    HTTPStatus.OK: None,
    HTTPStatus.NOT_FOUND: Error,
    HTTPStatus.BAD_REQUEST: Error
})
def put(request: HttpRequest, fields: UpdateUser):
    try:
        user = request.user
    except User.DoesNotExist: return HTTPStatus.NOT_FOUND, Error(message="User not found")

    if not fields: return HTTPStatus.BAD_REQUEST, Error(message="No fields provided to update user")

    for field, value in fields.dict(exclude_unset=True).items():
        setattr(user, field, value)

    user.save()


# Delete User
@router.delete('user', auth=JWTAuth(), response={
    HTTPStatus.OK: None,
    HTTPStatus.NOT_FOUND: Error,
})
def delete(request: HttpRequest):
    try:
        user = request.user
        user.delete()
    except User.DoesNotExist: return Error(message="User not found")

    return None




