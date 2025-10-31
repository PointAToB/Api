from http import HTTPStatus
from ninja_jwt.authentication import JWTAuth
from django.http import HttpRequest, HttpResponse
from ninja import Router
import base64
import numpy as np
import cv2


ai_core_router = Router()


@ai_core_router.post('image', auth=JWTAuth())
def post(request: HttpRequest):
    print(request.body)
    arr = np.asarray(bytearray(base64.b64decode(request.body)), dtype=np.uint8)

    img = cv2.imdecode(arr, cv2.IMREAD_COLOR)
    cv2.imwrite('test.jpg', img)


