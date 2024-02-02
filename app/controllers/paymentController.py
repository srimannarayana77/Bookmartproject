from rest_framework import viewsets
from rest_framework import serializers
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from app.models import Payment, Order
from app.serializers import PaymentSerializer,PaymentcreateSerializer
from app.helpers.pagination import paginationResponse
from rest_framework.pagination import PageNumberPagination
from app.helpers.filters import payment_filters
from app.helpers.sort import sort_payments
from app.middlewares.decorators import require_token,assign_customer_id
from app.constants.messageConstants import *


class PaymentView(viewsets.ViewSet):
    @api_view(['POST'])
    @require_token
    @assign_customer_id
    def create_payment(request):
        try:
            serializer = PaymentcreateSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response({'success': True, 'message': CREATE_PAYMENT_SUCCESSFULLY, 'data': serializer.data}, status=201)
        except serializers.ValidationError as e:
            return Response({'success': False, 'message': e.detail}, status=422)
        except Order.DoesNotExist:
            return Response({'success': False, 'message': PAYMENT_NOT_FOUND}, status=404)
        except Exception as err:
            error_message = str(err)
            return Response({'success': False, 'errors': error_message}, status=500)

    @api_view(['GET'])
    @require_token
    def list_payments(request):
        try:
            paginator = PageNumberPagination()
            limit = int(request.query_params.get('limit', 2))
            page = int(request.query_params.get('page', 1))
            paginator.page_size = limit
            sortBy = request.query_params.get('sort_by', 'id')
            sortType = request.query_params.get('sort_type', 'desc')

            payments = Payment.objects.all()
            payments = payment_filters(payments, request.query_params)
            payments= sort_payments(sortBy, sortType,payments)
            page_result = paginator.paginate_queryset(payments, request)
            serializer = PaymentSerializer(page_result, many=True)
            response_data = paginationResponse(ALL_PAYMENTS_RETRIEVED_SUCCESSFULLY, paginator.page.paginator.count, limit, page, serializer.data)
            return Response(response_data, status=200)
        
        except Exception as err:
            error_message = str(err)
            return Response({'success': False, 'errors': error_message}, status=500)

    @api_view(['GET'])
    @require_token
    def retrieve_payment(request, id):
        try:
            payment = Payment.objects.get(id=id)
            serializer = PaymentSerializer(payment)
            return Response({'success': True, 'message': SINGLE_PAYMENT_RETRIEVED_SUCCESSFULLY, 'data': serializer.data}, status=200)
        except Payment.DoesNotExist:
            return Response({'success': False, 'message':PAYMENT_NOT_FOUND}, status=404)
        except Exception as err:
            error_message = str(err)
            return Response({'success': False, 'errors': error_message}, status=500)
        
    @api_view(['DELETE'])
    @require_token
    @assign_customer_id
    def delete_payment(request, id):
        try:
            payment_delete = Payment.objects.get(id=id)
            payment_delete.delete()
            return Response({'success': True, 'message': DELETE_PAYMENT_SUCCESSFULLY}, status=204)
        except Payment.DoesNotExist:
            return Response({'success': False, 'message':PAYMENT_NOT_FOUND}, status=404)
        except Exception as err:
            error_message = str(err)
            return Response({'success': False, 'errors': error_message}, status=500)   

    # @api_view(['PUT'])
    # def update_payment(request, id):
    #     try:
    #         payment = Payment.objects.get(id=id)
    #         serializer = PaymentSerializer(payment, data=request.data)
    #         if serializer.is_valid(raise_exception=True):
    #             serializer.save()
    #             return Response({'success': True, 'message': UPDATE_PAYMENT_SUCCESSFULLY, 'data': serializer.data}, status=200)
    #     except serializers.ValidationError as e:
    #         return Response({'success': False, 'message': e.detail}, status=422)
    #     except Payment.DoesNotExist:
    #         return Response({'success': False, 'message': PAYMENT_NOT_FOUND}, status=404)
    #     except Exception as err:
    #         error_message = str(err)
    #         return Response({'success': False, 'errors': error_message}, status=500)
        