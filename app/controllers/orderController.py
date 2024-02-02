from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework import serializers
from rest_framework.pagination import PageNumberPagination
from app.models import Order,Cart
from app.serializers import OrderSerializer,OrdercreateSerializer
from app.helpers.filters import order_filters
from app.middlewares.decorators import require_token,assign_customer_id
from app.helpers.pagination import paginationResponse
from app.helpers.sort import sort_orders
from app.constants.messageConstants import *

class OrderView(viewsets.ViewSet):
    @api_view(['POST'])
    @require_token
    @assign_customer_id
    def create_order(request):
        try:
            serializer = OrdercreateSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response({'success': True, 'message': CREATE_ORDER_SUCCESSFULLY, 'data': serializer.data}, status=201)
        except serializers.ValidationError as e:
            return Response({'success': False, 'message': e.detail}, status=422)
        except Order.DoesNotExist:
            return Response({'success': False, 'message': ORDER_NOT_FOUND}, status=404)
        except Exception as err:
            error_message = str(err)
            return Response({'success': False, 'errors': error_message}, status=500)

    @api_view(['GET'])
    @require_token
    def list_orders(request):
        try:
            paginator = PageNumberPagination()
            limit = int(request.query_params.get('limit', 2))
            page = int(request.query_params.get('page', 1))
            paginator.page_size = limit
            sortBy = request.query_params.get('sort_by', 'id')
            sortType = request.query_params.get('sort_type', 'desc')

            orders = Order.objects.all()
            orders = order_filters(orders, request.query_params)
            orders = sort_orders(sortBy, sortType, orders)

            page_result = paginator.paginate_queryset(orders, request)
            serializer = OrderSerializer(page_result, many=True)
            response_data = paginationResponse(ALL_ORDERS_RETRIEVED_SUCCESSFULLY, paginator.page.paginator.count, limit, page, serializer.data)
            return Response(response_data, status=200)
        except Exception as err:
            error_message = str(err)
            return Response({'success': False, 'errors': error_message}, status=500)

    @api_view(['GET'])
    @require_token
    def retrieve_order(request, id):
        try:
            order_by_id = Order.objects.get(id=id)
            serializer = OrderSerializer(order_by_id)
            return Response({'success': True, 'message': SINGLE_ORDER_RETRIEVED_SUCCESSFULLY, 'data': serializer.data}, status=200)
        except Order.DoesNotExist:
            return Response({'success': False, 'message':ORDER_NOT_FOUND}, status=404)
        except Exception as err:
            error_message = str(err)
            return Response({'success': False, 'errors': error_message}, status=500)

    @api_view(['PUT'])
    @require_token
    @assign_customer_id
    def update_order(request, id):
        try:
            order_update = Order.objects.get(id=id)
            serializer = OrdercreateSerializer(order_update, data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response({'success': True, 'message':UPDATE_ORDER_SUCCESSFULLY, 'data': serializer.data}, status=200)
        except serializers.ValidationError as e:
            return Response({'success': False, 'message': e.detail}, status=422)
        except Order.DoesNotExist:
            return Response({'success': False, 'message': ORDER_NOT_FOUND}, status=404)
        except Exception as err:
            error_message = str(err)
            return Response({'success': False, 'errors': error_message}, status=500)

    @api_view(['DELETE'])
    @require_token
    @assign_customer_id
    def delete_order(request, id):
        try:
            order_delete = Order.objects.get(id=id)
            order_delete.delete()
            return Response({'success': True, 'message': DELETE_ORDER_SUCCESSFULLY}, status=204)
        except Order.DoesNotExist:
            return Response({'success': False, 'message': ORDER_NOT_FOUND}, status=404)
        except Exception as err:
            error_message = str(err)
            return Response({'success': False, 'errors': error_message}, status=500)
        
