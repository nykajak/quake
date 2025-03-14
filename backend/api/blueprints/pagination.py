from flask import jsonify
def pagination_validation(page, per_page):
    # Validation - Check if page and per_page are integers
    try:
        page = int(page)

    except ValueError as e:
        return jsonify(msg = "Bad request - page should be a postive integer"), 400

    try:
        per_page = int(per_page)

    except ValueError as e:
        return jsonify(msg = "Bad request - per_page should be a postive integer"), 400
    
    # Validation - Check if page and per_page are non-zero and positive integers
    if page <= 0:
        return jsonify(msg = "Bad request - page should be a postive integer"), 400

    if per_page <= 0:
        return jsonify(msg = "Bad request - per_page should be a postive integer"), 400
    
    return ((page,per_page),200)