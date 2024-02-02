from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework import serializers
from rest_framework.pagination import PageNumberPagination
from app.models import Company  
from app.helpers.pagination import paginationResponse
from app.serializers import CompanySerializer 
from app.helpers.filters import company_filters
from app.helpers.sort import sort_companies
from app.constants.messageConstants import *

class CompanyView(viewsets.ViewSet):
    @api_view(['POST'])
    def create_company(request):
        try:
            serializer = CompanySerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response({'success': True, 'message': CREATE_COMPANY_SUCCESSFULLY, 'data': serializer.data}, status=201)
        except serializers.ValidationError as e:
            return Response({'success': False, 'message': e.detail}, status=422)
        except Exception as err:
            error_message = str(err)
            return Response({'success': False, 'errors': error_message}, status=500)

    @api_view(['GET'])
    def list_companies(request):
        try:
            paginator = PageNumberPagination()
            limit = int(request.query_params.get('limit', 2))
            page = int(request.query_params.get('page', 1))
            paginator.page_size = limit
            sortBy = request.query_params.get('sort_by', 'id')
            sortType = request.query_params.get('sort_type', 'desc')
            companies = Company.objects.all()
            companies = company_filters(companies, request.query_params)
            companies = sort_companies(sortBy, sortType, companies)
            page_result = paginator.paginate_queryset(companies, request)
            serializer = CompanySerializer(companies, many=True)
            response_data = paginationResponse(ALL_COMPANIES_RETRIEVED_SUCCESSFULLY, paginator.page.paginator.count, limit, page, serializer.data)
            return Response(response_data, status=200)
        except Exception as err:
            error_message = str(err)
            return Response({'success': False, 'errors': error_message}, status=500)

    @api_view(['GET'])
    def retrieve_company(request, id):
        try:
            company_by_id = Company.objects.get(id=id)
            serializer = CompanySerializer(company_by_id)
            return Response({'success': True, 'message': SINGLE_COMPANY_RETRIEVED_SUCCESSFULLY, 'data': serializer.data}, status=200)
        except Company.DoesNotExist:
            return Response({'success': False, 'message': COMPANY_NOT_FOUND}, status=404)
        except Exception as err:
            error_message = str(err)
            return Response({'success': False, 'errors': error_message}, status=500)

    @api_view(['PUT'])
    def update_company(request, id):
        try:
            company_update = Company.objects.get(id=id)
            serializer = CompanySerializer(company_update, data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response({'success': True, 'message':UPDATE_COMPANY_SUCCESSFULLY, 'data': serializer.data}, status=200)
        except serializers.ValidationError as e:
            return Response({'success': False, 'message': e.detail}, status=422)
        except Company.DoesNotExist:
            return Response({'success': False, 'message':COMPANY_NOT_FOUND}, status=404)
        except Exception as err:
            error_message = str(err)
            return Response({'success': False, 'errors': error_message}, status=500)

    @api_view(['DELETE'])
    def delete_company(request, id):
        try:
            company_delete = Company.objects.get(id=id)
            company_delete.delete()
            return Response({'success': True, 'message': DELETE_COMPANY_SUCCESSFULLY}, status=204)
        except Company.DoesNotExist:
            return Response({'success': False, 'message': COMPANY_NOT_FOUND}, status=404)
        except Exception as err:
            error_message = str(err)
            return Response({'success': False, 'errors': error_message}, status=500)
