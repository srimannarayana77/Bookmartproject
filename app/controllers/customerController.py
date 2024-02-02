from rest_framework import viewsets
from django.contrib.auth import authenticate
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework import serializers
from rest_framework.pagination import PageNumberPagination
from rest_framework_simplejwt.tokens import RefreshToken
from app.models import Customer,User
from app.serializers import CustomerSerializer,CustomercreateSerializer
from app.middlewares.decorators import require_token,verify_customer
from app.helpers.filters import customer_filters
from django.contrib.auth.hashers import check_password
from app.helpers.pagination import  paginationResponse 
from app.helpers.sort import sort_customers
from app.constants.messageConstants import *

class Customerview(viewsets.ViewSet):
    @api_view(['POST'])
    @require_token
    @verify_customer
    def create_customer(request):
        try:

            serializer =CustomercreateSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True): 
                serializer.save()
                return Response({'success': True, 'message': CREATE_CUSTOMER_SUCCESSFULLY, 'data': serializer.data}, status=201)
        except serializers.ValidationError as e:
            return Response({'success': False, 'message': e.detail}, status=422)
        except Customer.DoesNotExist:
            return Response({'success': False, 'message':CUSTOMER_NOT_FOUND}, status=404)
        except Exception as err:
            error_message = str(err)
            return Response({'success': False, 'errors': error_message}, status=500)

    @api_view(['GET'])  
    @require_token
    def list_customers(request):
        try:
            paginator = PageNumberPagination()
            limit = int(request.query_params.get('limit', 2))
            page = int(request.query_params.get('page', 1))
            paginator.page_size = limit
            sortBy = request.query_params.get('sort_by', 'id')
            sortType = request.query_params.get('sort_type', 'desc')

            customers = Customer.objects.all()
            customers= customer_filters(customers, request.query_params)
            customers = sort_customers(sortBy, sortType, customers)
            page_result = paginator.paginate_queryset(customers, request)
            serializer = CustomerSerializer(page_result, many=True)
            response_data = paginationResponse(ALL_CUSTOMERS_RETRIEVED_SUCCESSFULLY, paginator.page.paginator.count, limit, page, serializer.data)
            return Response(response_data, status=200)
        except Exception as err:
            error_message = str(err)
            return Response({'success': False, 'errors': error_message}, status=500)

    @api_view(['GET'])
    @require_token
    def retrieve_customer(request, id):
        try:
            customer_by_id = Customer.objects.get(id=id)
            serializer = CustomerSerializer(customer_by_id)
            return Response({'success': True, 'message':SINGLE_CUSTOMER_RETRIEVED_SUCCESSFULLY, 'data': serializer.data}, status=200)
        except Customer.DoesNotExist:
            return Response({'success': False, 'message': CUSTOMER_NOT_FOUND}, status=404)
        except Exception as err:
            error_message = str(err)
            return Response({'success': False, 'errors': error_message}, status=500)

    @api_view(['PUT'])
    @require_token
    @verify_customer
    def update_customer(request, id):
        try:
            customer_update = Customer.objects.get(id=id)
            serializer = CustomercreateSerializer(customer_update, data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response({'success': True, 'message':UPDATE_CUSTOMER_SUCCESSFULLY, 'data': serializer.data}, status=200)
        except serializers.ValidationError as e:
            return Response({'success': False, 'message': e.detail}, status=422)
        except Customer.DoesNotExist:
            return Response({'success': False, 'message':CUSTOMER_NOT_FOUND}, status=404)
        except Exception as err:
            error_message = str(err)
            return Response({'success': False, 'errors': error_message}, status=500)

    @api_view(['DELETE'])
    @require_token
    @verify_customer
    def delete_customer(request, id):
        try:
            customer_delete =Customer.objects.get(id=id)
            customer_delete.delete()
            return Response({'success': True, 'message': DELETE_CUSTOMER_SUCCESSFULLY}, status=204)
        except Customer.DoesNotExist:
            return Response({'success': False, 'message': CUSTOMER_NOT_FOUND}, status=404)
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
        if authenticated_user is not None and check_password(password, authenticated_user.password):
            customer = Customer.objects.get(user=authenticated_user)
            print("customer=",customer)
            refresh = RefreshToken.for_user(authenticated_user) 
            access_token = str(refresh.access_token)    
            refresh_token = str(refresh)
            return Response({'success':True,'message':'The password is matched','customer_access_token': access_token, 'customer_refresh_token': refresh_token}, status=200)
        else:
            return Response({'success': False, 'message': 'The password you entered is incorrect.'}, status=422)       
     except Customer.DoesNotExist:
          return Response({'success': False, 'message': USER_NOT_FOUND}, status=404)
     except Exception as err:
        return Response({'success': False,'error': str(err)}, status=500)

