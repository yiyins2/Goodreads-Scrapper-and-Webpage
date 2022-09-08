import re

OBJECT = ['book', 'author']

# 0 - string, 1 - int, 2 - float
BOOK_FIELDS = {
    'book_url': 0,
    'title': 0,
    'book_id': 1,
    'ISBN': 1,
    'author_url': 0,
    'author': 0,
    'rating': 2,
    'rating_count': 1,
    'review_count': 1,
    'image_url': 0, 
    'similar_books_name' : 0
}
AUTHOR_FIELDS = {
    'name': 0,
    'author_url': 0,
    'author_id': 1,
    'rating': 2,
    'rating_count': 1,
    'review_count': 1,
    'image_url': 0, 
    'author_books_name': 0, 
    'similar_authors_name': 0
}


def parse(target):
    """
    parse object and field of target
    :return object, query based on the target
    """
    search = re.search('(.*)\.(.*)\:(.*)', target)
    if search is None:
        raise ValueError(target, 'No . or : operator')

    search_object = search.group(1)
    if search_object not in OBJECT:
        raise ValueError(search_object, 'Invalid object')

    field = search.group(2)
    if search_object == 'book':
        if field not in BOOK_FIELDS:
            raise ValueError(field, 'Invalid book field')
    else:
        if field not in AUTHOR_FIELDS:
            raise ValueError(field, 'Invalid author field')
    query = parse_query(search.group(3), search_object, field)
    return search_object, query


def parse_query(target, search_object, field):
    """
    parse content in the following order:
    exact search
    and or not operator
    < > operator
    search term
    also check type mismatches and incorrect content format
    :return the query parsed
    """
    if target == '':
        return {field: None}
    # exact search
    target = target.strip()
    if target.count('\"') == 1:
        raise ValueError(target, 'Invalid exact search')
    exact_search = re.search('(.*)\"(.*)\"(.*)', target)
    if exact_search is not None:
        # exact search cannot be combined with other operations
        if exact_search.group(1) != '' or exact_search.group(3) != '':
            raise ValueError(target, 'Invalid exact search')
        exact_search_content = exact_search.group(2)
        if exact_search_content == '':
            raise ValueError(target, 'Empty exact search')
        return {field: check_type(exact_search_content, search_object, field)}
    else:
        # AND
        and_search = re.search('(.*)\sAND\s(.*)', target)
        if and_search is not None:
            if and_search.group(1) == '' or and_search.group(2) == '':
                raise ValueError(target, 'Empty AND block')
            first_and = check_type(and_search.group(1), search_object, field)
            second_and = check_type(and_search.group(2), search_object, field)
            return {'$and': [{field: first_and}, {field: second_and}]}
        # OR
        or_search = re.search('(.*)\sOR\s(.*)', target)
        if or_search is not None:
            if or_search.group(1) == '' or or_search.group(2) == '':
                raise ValueError(target, 'Empty OR block')
            first_or = check_type(or_search.group(1), search_object, field)
            second_or = check_type(or_search.group(2), search_object, field)
            return {'$or': [{field: first_or}, {field: second_or}]}
        # NOT
        not_search = re.search('NOT\s(.*)', target)
        if not_search is not None:
            print()
            after_not = check_type(not_search.group(1), search_object, field)
            return {field: {'$not': after_not}}
        # >
        gt_search = re.search('>\s(.*)', target)
        if gt_search is not None:
            after_gt = check_type(gt_search.group(1), search_object, field)
            return {field: {'$gt': after_gt}}
        # <
        lt_search = re.search('<\s(.*)', target)
        if lt_search is not None:
            after_lt = check_type(lt_search.group(1), search_object, field)
            return {field: {'$lt': after_lt}}
        # search term
        if search_object == 'book':
            field_type = BOOK_FIELDS[field]
        else:
            field_type = AUTHOR_FIELDS[field]
        if field_type == 0:
            return {field: {'$regex': '.*'+target+'.*'}}
        elif field_type == 1:
            if not is_int(target):
                raise TypeError(target, "Type Mismatch: Search field - " + field + " - is int")
            return {field: int(target)}
        else:
            if not is_float(target):
                raise TypeError(target, "Type Mismatch: Search field - " + field + " - is float")
            return {field: float(target)}
        raise ValueError(target, 'Invalid format')


def check_type(content, search_object, field):
    """
    check content matches the field type
    """
    if search_object == 'book':
        field_type = BOOK_FIELDS[field]
    else:
        field_type = AUTHOR_FIELDS[field]
    if field_type == 0:
        return content
    elif field_type == 1:
        if not is_int(content):
            raise TypeError(content, "Type Mismatch: Search field - " + field + " - is int")
        return int(content)
    else:
        if not is_float(content):
            raise TypeError(content, "Type Mismatch: Search field - " + field + " - is float")
        return float(content)


def is_int(search_input):
    """
    check if input can convert to int
    """
    return search_input.isdigit()


def is_float(search_input):
    """
    check if input can convert to float
    """
    return search_input.isdigit() or re.match(r'^-?\d+(?:\.\d+)$', search_input) is not None
