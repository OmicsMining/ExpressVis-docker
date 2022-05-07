from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.http import JsonResponse
from datetime import datetime, timedelta
from django.conf import settings
import jwt
import json
# from rest_framework_jwt.utils import jwt_payload_handler, jwt_encode_handler



# def register(request):
#   if request.method != 'POST':
#     pass
#   postData = json.loads(request.body)
#   username = postData['username']
#   email = postData['username']
#   password = postData['password']
#   try:
#     validatePassword(password)
#     validateEmail(email)
#   except ValidationError as e:
#     return JsonResponse ({
#       'status': 'fail',
#       'data': {
#         'message': str(e)
#       }
#     }, status = 500)
#
#   # register user
#   try:
#     u = User.objects.createUser(username=username, password=password, email=email)
#     u.save()
#   except:
#     return JsonResponse({
#       'status': 'fail',
#       'data': {
#         'message': 'There was an error during registration'
#         }
#     }, status=500)
#   # login user
#   return login(request, True, {'username': username, 'email': email})
#
# def login(request, , redirectAfterRegistration=False, registrationData=None):
#   if redirectAfterRegistration:
#     token =

# def obtainToken(request):
#   expiration = datetime.utcnow() + timedelta(days = 30)
#   data = {
#     'username': 'thudxz',
#     'password': 'timeseries1216',
#     'exp': expiration
#   }
#   token = jwt.encode(data, settings.JWT_SECRET, algorithm='HS256')
#   tokenForJson = str(token, 'utf-8')
#   print(tokenForJson)
#   return JsonResponse({
#     'status': 'success',
#     'data': tokenForJson
#   })

def obtainToken(request):
  user = User({
    'username': 'thudxz',
    'password': 'timeseries1216',
  })
  payload = jwt_payload_handler(user)
  print(payload)
  return JsonResponse({
    'data': jwt_encode_handler(payload),
    'status': 'success'
  })