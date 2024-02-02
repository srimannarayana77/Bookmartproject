from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework import serializers
from rest_framework.pagination import PageNumberPagination
from app.models import Book
from app.middlewares.decorators import require_token,assign_publisher_id
from app.serializers import BookSerializer,BookcreateSerializer
from app.helpers.filters import book_filters
from app.helpers.pagination import paginationResponse
from app.helpers.sort import sort_books
from app.constants.messageConstants import *

class BookView(viewsets.ViewSet):
    @api_view(['POST'])
    @require_token
    @assign_publisher_id
    def create_book(request):  
        try:
            serializer = BookcreateSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response({'success': True, 'message':CREATE_BOOK_SUCCESSFULLY, 'data': serializer.data}, status=201)
        except serializers.ValidationError as e:
            return Response({'success': False, 'message': e.detail}, status=422)
        except Book.DoesNotExist:
            return Response({'success': False, 'message': BOOK_NOT_FOUND}, status=404)
        except Exception as err:
            error_message = str(err)
            return Response({'success': False, 'errors': error_message}, status=500)

    @api_view(['GET'])
    @require_token
    def list_books(request):
        try:
            paginator = PageNumberPagination()
            limit = int(request.query_params.get('limit', 2))
            page = int(request.query_params.get('page', 1))
            paginator.page_size = limit
            sortBy = request.query_params.get('sort_by', 'id')
            sortType = request.query_params.get('sort_type', 'desc')
            books = Book.objects.all()
            books = book_filters(books, request.query_params)
            books = sort_books(sortBy, sortType, books)
            page_result = paginator.paginate_queryset(books, request)
            serializer = BookSerializer(page_result, many=True)
            response_data = paginationResponse(ALL_BOOKS_RETRIEVED_SUCCESSFULLY, paginator.page.paginator.count, limit, page, serializer.data)
            return Response(response_data, status=200)
        except Exception as err:
            error_message = str(err)
            return Response({'success': False, 'errors': error_message}, status=500)

    @api_view(['GET'])
    @require_token
    def retrieve_book(request, id):
        try:
            book_by_id = Book.objects.get(id=id)
            serializer = BookSerializer(book_by_id)
            return Response({'success': True, 'message': SINGLE_BOOK_RETRIEVED_SUCCESSFULLY, 'data': serializer.data}, status=200)
        except Book.DoesNotExist:
            return Response({'success': False, 'message':BOOK_NOT_FOUND}, status=404)
        except Exception as err:
            error_message = str(err)
            return Response({'success': False, 'errors': error_message}, status=500)

    @api_view(['PUT'])
    @require_token
    @assign_publisher_id
    def update_book(request, id):
        try:
            book_update = Book.objects.get(id=id)
            serializer = BookcreateSerializer(book_update, data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response({'success': True, 'message': UPDATE_BOOK_SUCCESSFULLY, 'data': serializer.data}, status=200)
        except serializers.ValidationError as e:
            return Response({'success': False, 'message': e.detail}, status=422)
        except Book.DoesNotExist:
            return Response({'success': False, 'message':BOOK_NOT_FOUND}, status=404)
        except Exception as err:
            error_message = str(err)
            return Response({'success': False, 'errors': error_message}, status=500)

    @api_view(['DELETE'])
    @require_token
    @assign_publisher_id
    def delete_book(request, id):
        try:
            book_delete = Book.objects.get(id=id)
            book_delete.delete()
            return Response({'success': True, 'message': DELETE_BOOK_SUCCESSFULLY}, status=204)
        except Book.DoesNotExist:
            return Response({'success': False, 'message': BOOK_NOT_FOUND}, status=404)
        except Exception as err:
            error_message = str(err)   
            return Response({'success': False, 'errors': error_message}, status=500) 