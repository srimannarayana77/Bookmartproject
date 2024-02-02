import math
def paginationResponse(message, count, limit, page, Response_Data):
    totalPages = math.ceil(count / int(limit))
    response_data = {
            "success": True,
            "message": message,
            "count": count,
            "totalPages": totalPages,
            "currentPage": page,
            "resultsPerPage": limit,
            "nextPage": page + 1 if page < totalPages else None,
            "previousPage": page - 1 if page > 1 else None,
            "data": Response_Data
            }
    return response_data