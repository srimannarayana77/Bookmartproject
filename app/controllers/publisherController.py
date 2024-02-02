from rest_framework import viewsets
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from rest_framework import serializers
from rest_framework.pagination import PageNumberPagination
from app.models import Publisher,User,Company
from app.serializers import PublisherSerializer,PublishercreateSerializer
from app.helpers.filters import publisher_filters
from django.contrib.auth.hashers import check_password
from app.helpers.pagination import  paginationResponse 
from app.helpers.sort import sort_publishers
from app.middlewares.decorators import require_token,verify_publisher
from app.constants.messageConstants import *

class Publisherview(viewsets.ViewSet):
    @api_view(['POST'])
    @require_token
    @verify_publisher
    def create_publisher(request):
        try:
            serializer = PublishercreateSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response({'success': True, 'message': CREATE_PUBLISHER_SUCCESSFULLY, 'data': serializer.data}, status=201)
        except serializers.ValidationError as e:
            return Response({'success': False, 'message': e.detail}, status=422)
        except Publisher.DoesNotExist:
            return Response({'success': False, 'message':PUBLISHER_NOT_FOUND}, status=404)
        except Exception as err:
            error_message = str(err)
            return Response({'success': False, 'errors': error_message}, status=500)
        
    @api_view(['GET'])
    @require_token
    def list_publishers(request):
        try:
            paginator = PageNumberPagination()
            limit = int(request.query_params.get('limit', 2))
            page = int(request.query_params.get('page', 1))
            paginator.page_size = limit
            sortBy = request.query_params.get('sort_by', 'id')
            sortType = request.query_params.get('sort_type', 'desc')

            publishers = Publisher.objects.all()
            publishers = publisher_filters(publishers, request.query_params)
            publishers = sort_publishers(sortBy, sortType, publishers)
            page_result = paginator.paginate_queryset(publishers, request) 
            serializer = PublisherSerializer(page_result, many=True)
            response_data = paginationResponse(ALL_PUBLISHERS_RETRIEVED_SUCCESSFULLY, paginator.page.paginator.count, limit, page, serializer.data)
            return Response(response_data, status=200)
        except Exception as err:
            error_message = str(err)
            return Response({'success': False, 'errors': error_message}, status=500)

    @api_view(['GET'])
    @require_token
    def retrieve_publisher(request, id):
        try:
            publisher_by_id = Publisher.objects.get(id=id)
            serializer = PublisherSerializer(publisher_by_id)
            return Response({'success': True, 'message': SINGLE_PUBLISHER_RETRIEVED_SUCCESSFULLY, 'data': serializer.data}, status=200)
        except Publisher.DoesNotExist:
            return Response({'success': False, 'message': PUBLISHER_NOT_FOUND}, status=404)
        except Exception as err:
            error_message = str(err)
            return Response({'success': False, 'errors': error_message}, status=500)

    @api_view(['PUT'])
    @require_token
    @verify_publisher
    def update_publisher(request, id):
        try:
            publisher_update = Publisher.objects.get(id=id)
            serializer = PublishercreateSerializer(publisher_update, data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response({'success': True, 'message': UPDATE_PUBLISHER_SUCCESSFULLY, 'data': serializer.data}, status=200)
        except serializers.ValidationError as e:
            return Response({'success': False, 'message': e.detail}, status=422)
        except Publisher.DoesNotExist:
            return Response({'success': False, 'message': PUBLISHER_NOT_FOUND}, status=404)
        except Exception as err:
            error_message = str(err)
            return Response({'success': False, 'errors': error_message}, status=500)

    @api_view(['DELETE'])
    @require_token
    @verify_publisher
    def delete_publisher(request, id):
        try:
            publisher_delete = Publisher.objects.get(id=id)
            publisher_delete.delete()
            return Response({'success': True, 'message': DELETE_PUBLISHER_SUCCESSFULLY}, status=204)
        except Publisher.DoesNotExist:
            return Response({'success': False, 'message': PUBLISHER_NOT_FOUND}, status=404)
        except Exception as err:
            error_message = str(err)
            return Response({'success': False, 'errors': error_message}, status=500)
        
    @api_view(['POST'])
    def signinview( request):
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
        if authenticated_user is not None and check_password(password, authenticated_user.password ):
            publisher = Publisher.objects.get(user=authenticated_user)
            print("publisher=",publisher)
            refresh = RefreshToken.for_user(authenticated_user) 
            access_token = str(refresh.access_token) 
            refresh_token = str(refresh)
            return Response({'success':True,'message':'The password is matched','publisher_access_token': access_token, 'publisher_refresh_token': refresh_token}, status=200)
        else:
            return Response({'success': False, 'message': 'The password you entered is incorrect.'}, status=422)       
     except User.DoesNotExist:
          return Response({'success': False, 'message': USER_NOT_FOUND}, status=404)
     except Exception as err:
        return Response({'success': False,'error': str(err)}, status=500)


    