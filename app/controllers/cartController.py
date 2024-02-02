from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework import serializers
from rest_framework.pagination import PageNumberPagination
from app.models import Cart,Customer
from app.helpers.filters import cart_filters
from app.helpers.pagination import paginationResponse
from app.helpers.sort import sort_carts
from app.serializers import CartSerializer,CartcreateSerializer
from app.middlewares.decorators import require_token,assign_customer_id
from app.constants.messageConstants import *

class CartView(viewsets.ViewSet):
    @api_view(['POST'])
    @require_token
    @assign_customer_id
    def create_cart(request):
        try:
            serializer = CartcreateSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response({'success': True, 'message':CREATE_CART_SUCCESSFULLY, 'data': serializer.data}, status=201)
        except serializers.ValidationError as e:
            return Response({'success': False, 'message': e.detail}, status=422)
        except Cart.DoesNotExist:
            return Response({'success': False, 'message': CART_NOT_FOUND}, status=404)
        except Exception as err:
            error_message = str(err)
            return Response({'success': False, 'errors': error_message}, status=500)

    @api_view(['GET'])
    @require_token
    @assign_customer_id
    def list_carts(request):
        try:
            paginator = PageNumberPagination()
            limit = int(request.query_params.get('limit', 2))
            page = int(request.query_params.get('page', 1))
            paginator.page_size = limit
            sortBy = request.query_params.get('sort_by', 'id')
            sortType = request.query_params.get('sort_type', 'desc')

            carts = Cart.objects.all()
            carts = cart_filters(carts, request.query_params)
            carts= sort_carts(sortBy, sortType,carts)
            page_result = paginator.paginate_queryset(carts, request)
            serializer = CartSerializer(page_result, many=True)
            response_data = paginationResponse(ALL_CARTS_RETRIEVED_SUCCESSFULLY, paginator.page.paginator.count, limit, page, serializer.data)
            return Response(response_data, status=200) 
        except Exception as err:
            error_message = str(err)
            return Response({'success': False, 'errors': error_message}, status=500)

    @api_view(['GET'])
    @require_token
    def retrieve_cart(request, id):
        try:
            cart_by_id = Cart.objects.get(id=id)
            serializer = CartSerializer(cart_by_id)
            return Response({'success': True, 'message':SINGLE_CART_RETRIEVED_SUCCESSFULLY, 'data': serializer.data}, status=200)
        except Cart.DoesNotExist:
            return Response({'success': False, 'message': CART_NOT_FOUND}, status=404)
        except Exception as err:
            error_message = str(err)
            return Response({'success': False, 'errors': error_message}, status=500)

    @api_view(['PUT'])
    @require_token
    @assign_customer_id
    def update_cart(request, id):
        try:
            cart_update = Cart.objects.get(id=id)
            serializer = CartcreateSerializer(cart_update,data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response({'success': True, 'message': UPDATE_CART_SUCCESSFULLY, 'data': serializer.data}, status=200)
        except serializers.ValidationError as e:
            return Response({'success': False, 'message': e.detail}, status=422)
        except Cart.DoesNotExist:
            return Response({'success': False, 'message': CART_NOT_FOUND}, status=404)
        except Exception as err:
            error_message = str(err)
            return Response({'success': False, 'errors': error_message}, status=500)

    @api_view(['DELETE'])
    @require_token
    @assign_customer_id
    def delete_cart(request, id):
        try:
            cart_delete = Cart.objects.get(id=id)
            cart_delete.delete() 
            return Response({'success': True, 'message': DELETE_CART_SUCCESSFULLY}, status=204)
        except Cart.DoesNotExist:
            return Response({'success': False, 'message': CART_NOT_FOUND}, status=404)
        except Exception as err:
            error_message = str(err)
            return Response({'success': False, 'errors': error_message}, status=500)
