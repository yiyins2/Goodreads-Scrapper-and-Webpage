from flask import Flask, request, abort
from flask_cors import CORS
from goodreads.db import db_helper
from goodreads.interpreter import parse
from bson.json_util import dumps
from multiprocessing import Process
from goodreads.scrapper.processor import crawl

app = Flask(__name__)
cors = CORS(app)

def check_id(input_id):
    """
    Check if the id is valid, if not abort 400
    """
    try:
        input_id = int(input_id)
        if input_id < 0:
            return "Bad Request: Negative ID", 400
        else:
            return input_id
    except ValueError:
        return "Bad Request: Non-integer ID", 400


@app.route('/book', methods=['GET'])
def get_book_id():
    """
    get book given id
    :return: the book or abort 400 if id not valid or id not found
    """
    if 'id' in request.args:
        input_id = check_id(request.args['id'])
        result = db_helper.get_book_author_id(input_id, True)
        if result is None:
            return "Bad Request: No such book ID is found", 400
        else:
            result.pop('_id')
            return result
    else:
        return "Bad Request: Please enter a book ID", 400


@app.route('/author', methods=['GET'])
def get_author_id():
    """
    get author given id
    :return: the author or abort 400 if id not valid or id not found
    """
    if 'id' in request.args:
        input_id = check_id(request.args['id'])
        result = db_helper.get_book_author_id(input_id, False)
        if result is None:
            return "Bad Request: No such author ID is found", 400
        else:
            result.pop('_id')
            return result
    else:
        return "Bad Request: Please enter an author ID", 400


@app.route('/search', methods=['GET'])
def search():
    """
    search db given query
    :return: search result or abort 400 if invalid query or no query entered
    """
    if 'q' in request.args:
        query = request.args['q']
        try:
            parse_obj, parse_query = parse(query)
        except (TypeError, ValueError):
            return "Bad Request: Invalid query", 400
        if parse_obj == 'book':
            results = db_helper.get_search(parse_query, True)
        else:
            results = db_helper.get_search(parse_query, False)
        return dumps(list(results))
    else:
        return "Bad Request: Please enter a query", 400


def empty_body(data):
    """
    abort 400 if empty body for post and put verbs
    """
    if data is None:
        return "Bad Request: Empty body", 400


@app.route('/book', methods=['PUT'])
def put_book_id():
    """
    update the book given id and query
    :return: Success message or abort 400 if id not found
    """
    if 'id' in request.args:
        book_id = check_id(request.args['id'])
        data = request.json
        if data is None:
            return abort(415, "Body is not JSON")
        empty_body(data)
        result = db_helper.put_book_author_id(book_id, data, True)
        if result != 1:
            return "Bad Request: No such book ID is found or invalid field value", 400
        else:
            return "Successfully updated document with book id: " + str(book_id)


@app.route('/author', methods=['PUT'])
def put_author_id():
    """
    update the author given id and query
    :return: Success message or abort 400 if id not found
    """
    if 'id' in request.args:
        author_id = check_id(request.args['id'])
        data = request.json
        if data is None:
            return abort(415, "Body is not JSON")
        empty_body(data)
        result = db_helper.put_book_author_id(author_id, data, False)
        if result is 1:
            return "Bad Request: No such author ID is found", 400
        else:
            return "Successfully updated document with author id: " + str(author_id)


@app.route('/book', methods=['POST'])
def post_book():
    """
    update the book if the id already exists
    insert a new book if the id does not exist
    abort 400 if no book id
    """
    data = request.json
    if data is None:
        return abort(415, "Body is not JSON")
    empty_body(data)
    book_id = data['book_id']
    if book_id is not None:
        result = db_helper.post_book_author(fill_in_book(data), True)
        if result is 0:
            return "Successfully inserted the new book"
        else:
            return "Successfully modified document with book id: " + str(book_id)
    else:
        return "Bad Request: your book does not have an ID", 400


@app.route('/books', methods=['POST'])
def post_books():
    """
    post each book in the list
    """
    data = request.json
    if data is None:
        return abort(415, "Body is not JSON")
    empty_body(data)
    return post_books_str(data)


def post_books_str(data):
    """
    helper function to return posts books results
    """
    return_str = ''
    for i in range(len(data)):
        item = data[i]
        book_id = item['book_id']
        if book_id is not None:
            result = db_helper.post_book_author(fill_in_book(item), True)
            if result is 0:
                return_str += str(i) + "th input: Successfully inserted the new book with id: " + str(book_id) + "\n"
            else:
                return_str += str(i) + "th input: Successfully modified document with book id: " + str(book_id) + "\n"
        else:
            return_str += str(i) + "th input: Error: your book does not have an ID"
    return return_str


@app.route('/author', methods=['POST'])
def post_author():
    """
    update the author if the id already exists
    insert a new author if the id does not exist
    abort 400 if no author id
    """
    data = request.json
    if data is None:
        return abort(415, "Body is not JSON")
    empty_body(data)
    author_id = data['author_id']
    if author_id is not None:
        result = db_helper.post_book_author(fill_in_author(data), False)
        if result is 0:
            return "Successfully inserted the new author with id: " + str(author_id)
        else:
            return "Successfully modified document with author id: " + str(author_id)
    else:
        return "Error: your author does not have an ID"


@app.route('/authors', methods=['POST'])
def post_authors():
    """
    post each author in the list
    """
    data = request.json
    if data is None:
        return abort(415, "Body is not JSON")
    empty_body(data)
    return post_authors_str(data)


def post_authors_str(data):
    """
    helper function to return posts books results
    """
    return_str = ''
    for i in range(len(data)):
        item = data[i]
        author_id = item['author_id']
        if author_id is not None:
            result = db_helper.post_book_author(fill_in_author(item), False)
            if result is 0:
                return_str += str(i) + "th input: Successfully inserted the new author with id: " + str(
                    author_id) + "\n"
            else:
                return_str += str(i) + "th input: Successfully modified document with author id: " + str(
                    author_id) + "\n"
        else:
            return_str += str(i) + "th input: Error: your author does not have an ID"
    return return_str


@app.route('/scrape', methods=['POST'])
def scrape():
    """
    scrape the given url
    :return: success message or abort 400 if invalid url
    """
    data = request.json
    if data is None:
        return abort(415, "Body is not JSON")
    if 'start_url' not in data:
        return 400, "Please enter a URL", 400
    start_url = data['start_url']
    if not start_url.startswith('https://www.goodreads.com/book/show/') and \
            not start_url.startswith('https://www.goodreads.com/author/show/'):
        return "Invalid URL", 400
    p = Process(target=crawl, kwargs={'start_url': start_url, 'max_books': 1, 'max_authors': 1})
    p.start()
    p.join()
    return "Successfully crawled the URL: " + start_url


@app.route('/book', methods=['DELETE'])
def delete_book_id():
    """
    delete book given id
    :return: success message or abort 400 if no id or id not found
    """
    if 'id' in request.args:
        input_id = check_id(request.args['id'])
        result = db_helper.delete_book_author_id(input_id, True)
        if result:
            return "Successfully deleted document with book ID: " + request.args['id']
        else:
            return "Bad Request: No such book ID is found", 400
    else:
        return "Bad Request: Please enter a book ID", 400


@app.route('/author', methods=['DELETE'])
def delete_author_id():
    """
    delete author given id
    :return: success message or abort 400 if no id or id not found
    """
    if 'id' in request.args:
        input_id = check_id(request.args['id'])
        result = db_helper.delete_book_author_id(input_id, False)
        if result:
            return "Successfully deleted document with author ID: " + str(input_id)
        else:
            return "Bad Request: No such author ID is found" + str(input_id), 400
    else:
        return "Bad Request: Please enter an author ID", 400 


def data_or_none(key, data):
    return data[key] if key in data else None


def fill_in_book(data):
    """
    initialize a book document given some or all of the values
    also convert the values into correct type
    :return: the document
    """
    return {
        'book_url': data_or_none('book_url', data),
        'title': data_or_none('title', data),
        'book_id': int(data['book_id']) if 'book_id' in data else None,
        'ISBN': int(data['ISBN']) if 'ISBN' in data else None,
        'author_url': data_or_none('author_url', data),
        'author': data_or_none('author', data),
        'rating': float(data['rating']) if 'rating' in data else None,
        'rating_count': int(data['rating_count']) if 'rating_count' in data else None,
        'review_count': int(data['review_count']) if 'review_count' in data else None,
        'image_url': data_or_none('image_url', data),
        'similar_books': data['similar_books'] if 'similar_books' in data else [], 
        'similar_books_name': data['similar_books_name'] if 'similar_books_name' in data else []
    }


def fill_in_author(data):
    """
    initialize a author document given some or all of the values
    also convert the values into correct type
    :return: the document
    """
    return {
        'name': data_or_none('name', data),
        'author_url': data_or_none('author_url', data),
        'author_id': int(data['author_id']),
        'rating': float(data['rating']) if 'rating' in data is not None else None,
        'rating_count': int(data['rating_count']) if 'rating_count' in data is not None else None,
        'review_count': int(data['review_count']) if 'review_count' in data is not None else None,
        'image_url': data_or_none('image_url', data),
        'author_books': data['author_books'] if 'author_books' in data else [],
        'author_books_name': data['author_books_name'] if 'author_books_name' in data else [],
        'similar_authors': data['similar_authors'] if 'similar_authors' in data else [], 
        'similar_authors_name': data['similar_authors_name'] if 'similar_authors_name' in data else []
    }


if __name__ == "__main__":
    app.run()
