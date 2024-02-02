from rest_framework.response import Response
from django.conf import settings
from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework.pagination import PageNumberPagination
from app.helpers.pagination import paginationResponse
from app.helpers.filters import user_filters
from app.helpers.sort import sort_users
from django.contrib.auth.hashers import check_password
from rest_framework.decorators import api_view
from rest_framework_simplejwt.tokens import RefreshToken 
from app.models import User 
from app.serializers import UserSerializer,UsercreateSerializer
from app.constants.messageConstants import *
from rest_framework import viewsets   
 
class UserCreateView(viewsets.ViewSet):
 @api_view(['POST'])
 def post(request):
    try:
        serializer = UsercreateSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
          serializer.save()
          return Response({'success': True, 'message':CREATE_USER_SUCCESSFULLY , 'data':serializer.data}, status=201)
    except serializers.ValidationError as e:
                return Response({'success': False, 'message': e.detail}, status=422)
    except User.DoesNotExist:
          return Response({'success': False, 'message': USER_NOT_FOUND}, status=404)
    except Exception as err:
           error_message = str(err)
           return Response({'success': False, 'errors': error_message}, status=500)
    
 @api_view(['GET']) 
 def get(request):
    try:  
          paginator = PageNumberPagination()
          limit = int(request.query_params.get('limit', 2))
          page = int(request.query_params.get('page', 1))
          paginator.page_size = limit
          sortBy = request.query_params.get('sort_by', 'id')
          sortType = request.query_params.get('sort_type', 'desc')
          
          users = User.objects.all() 
          users= user_filters(users, request.query_params)
          users = sort_users(sortBy, sortType, users)
          page_result = paginator.paginate_queryset(users, request)
          serializer = UserSerializer(page_result, many=True)
          Response_Data = paginationResponse(ALL_USERS_RETRIVE_SUCCESSFULLY ,paginator.page.paginator.count, limit, page, serializer.data)
          return Response(Response_Data,status=200)  
    except Exception as err:
            error_message = str(err)
            return Response({'success': False, 'errors': error_message}, status=500)
    
 @api_view(['GET'])  
 def getSingle(request,id):
    try:              
            user_by_id = User.objects.get(id= id)
            serializer = UserSerializer(user_by_id)
            return Response({'success': True, 'message':SINGLE_USER_RETRIVE_SUCCESSFULLY , 'data':serializer.data},status=200)
    except User.DoesNotExist:
            return Response({'success': False, 'message': USER_NOT_FOUND}, status=404)
    except Exception as err:
            error_message = str(err)
            return Response({'success': False, 'errors': error_message}, status=500)
  
 @api_view(['PUT'])   
 def put(request, id):
    try: 
        user_update = User.objects.get(id=id)
        serializer = UserSerializer(user_update, data=request.data)  
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'success': True, 'message': UPDATE_USER_SUCCESSFULLY, 'data': serializer.data},status=200)
    except serializers.ValidationError as e:
                return Response({'success': False, 'message': e.detail}, status=422)
    except User.DoesNotExist:
        return Response({'success': False, 'message': USER_NOT_FOUND}, status=404)
  
    except Exception as err:
        error_message = str(err)
        return Response({'success': False, 'errors': error_message}, status=500)
      
 @api_view(['DELETE'])     
 def delete(request, id):
      try:
        user_delete = User.objects.get(id=id)
        user_delete.delete() 
        return Response({'success': True, 'message': DELETE_USER_SUCCESSFULLY},status=204)
      except User.DoesNotExist:
            return Response({'success': False, 'message': USER_NOT_FOUND}, status=404)
      except Exception as err:
            error_message = str(err)
            return Response({'success': False, 'errors': error_message}, status=500)   

    
 @api_view(['POST'])
 def signin(request):
    try:   
        email = request.data.get('email')
        password = request.data.get('password')
        if not email:
         return Response({'success': False, 'message': 'Email is a required field.'}, status=422)
        if not password:
         return Response({'success': False, 'message': 'Password is a required field.'}, status=422)
        authenticated_user = User.objects.get(email=email)
        authenticated_user == authenticate(request, email=email, password=password)
        print('auth_user=',authenticated_user)     
        if authenticated_user is not None and check_password(password, authenticated_user.password):
            refresh = RefreshToken.for_user(authenticated_user)
            access_token = str(refresh.access_token) 
            refresh_token = str(refresh)
            return Response({'success':True,'message':'password is matched','access_token': access_token, 'refresh_token': refresh_token}, status=200)
        else:
            return Response({'success': False, 'message': 'The password you entered is incorrect.'}, status=422)       
    except User.DoesNotExist:
          return Response({'success': False, 'message': USER_NOT_FOUND}, status=404)
    except Exception as err:
        return Response({'success': False,'error': str(err)}, status=500)

                 

                 