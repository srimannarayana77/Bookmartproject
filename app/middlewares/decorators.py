import jwt
from django.conf import settings
from rest_framework.response import Response
from functools import wraps
from app.models import User,Customer,Cart
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from app.constants.messageConstants import *

def require_token(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        auth_header = request.META.get('HTTP_AUTHORIZATION')
        print('auth=', auth_header)
        try:
            decoded_data = jwt.decode(jwt=auth_header, key=settings.SECRET_KEY,algorithms=["HS256"])
            print('decode=',decoded_data)
            user_id = decoded_data['user_id'] 
            print("user_id=",user_id)
            request.user_id = user_id 
            user_details = User.objects.filter(id=decoded_data['user_id']).values()
            print('user_details=', user_details)
            print(type(user_details))
            if user_details: 
             user_type = user_details[0].get('user_type')
             print('usertype=', user_type)
             request.user_type = user_type  
             return view_func(request, *args, **kwargs)
            else:
                return Response({'success': False, 'message': 'User details not found'}, status=404)
        except jwt.ExpiredSignatureError:
            return Response({'success': False, 'message': 'Token has expired'}, status=401)
        except jwt.DecodeError:
            return Response({'success': False, 'message': 'Require Token'}, status=422)     
    return _wrapped_view

def assign_customer_id(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        user_id = request.user_id
        user_type = request.user_type  

        try:
            if user_type == 'CUSTOMER':
                customer = Customer.objects.get(user_id=user_id)
                request.customer_id = customer.id
                request.data['customer'] = request.customer_id
            else:
               
                return JsonResponse({'success': False, 'message': 'You do not have permission to access this resource.'}, status=403)
        except ObjectDoesNotExist:
            return JsonResponse({'success': False, 'message': 'Customer not found for the given user ID'}, status=404)

        return view_func(request, *args, **kwargs)

    return _wrapped_view

def assign_publisher_id(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        user_type = request.user_type  

        try:
            if user_type == 'PUBLISHER':
                publisher_id = request.user_id
                request.data['publisher'] = publisher_id
            else:
               
                return JsonResponse({'success': False, 'message': 'You do not have permission to access this resource.'}, status=403)
        except ObjectDoesNotExist:
            return JsonResponse({'success': False, 'message': 'Publisher not found for the given user ID'}, status=404)

        return view_func(request, *args, **kwargs)

    return _wrapped_view


def verify_publisher(view_func):  
  def _wrapped_view(request, *args, **kwargs):
        decoded_data = require_token(request)
        print('decoded=',decoded_data)
        user_type = decoded_data.__getattribute__('user_type')
        if user_type == 'PUBLISHER':
            return view_func(request, *args, **kwargs)
        else:
            return Response({'success': False, 'message': 'You do not have permission to create publishers.'}, status=401)
        
  return _wrapped_view   

def verify_customer(view_func):   
  def _wrapped_view(request, *args, **kwargs):
        decoded_data = require_token(request)
        print('decoded=',decoded_data)
        user_type = decoded_data.__getattribute__('user_type')
        if user_type == 'CUSTOMER':
            return view_func(request, *args, **kwargs)
        else:
            return Response({'success': False, 'message': 'You do not have permission to create customers.'}, status=401)
  return _wrapped_view 

