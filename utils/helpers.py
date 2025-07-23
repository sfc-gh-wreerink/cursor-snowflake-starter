def format_query_result(result, columns):
    return [dict(zip(columns, row)) for row in result]
