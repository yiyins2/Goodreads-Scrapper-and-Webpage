from os import getenv
from pymongo import MongoClient


def get_client():
    """
    Connect client
    """
    return MongoClient(getenv('MONGODB_KEY'))


def get_book_author_id(get_id, book_or_author):
    """
    helper find to return the book or author document based on the id
    """
    client = get_client()
    db = client[getenv('MONGODB_DB')]
    if book_or_author:
        client.close()
        return db['books'].find_one({"book_id": get_id})
    else:
        client.close()
        return db['authors'].find_one({"author_id": get_id})


def get_search(query, book_or_author):
    """
    helper find to return the book or author documents based on search query
    """
    client = get_client()
    db = client[getenv('MONGODB_DB')]
    if book_or_author:
        client.close()
        return db['books'].find(query)
    else:
        client.close()
        return db['authors'].find(query)


def put_book_author_id(put_id, data, book_or_author):
    """
    return the num of modified document (0 - fail, 1 - succeed)
    based on the id and update data
    """
    client = get_client()
    db = client[getenv('MONGODB_DB')]
    if book_or_author:
        result = db['books'].update_one({'book_id': put_id}, {'$set': data})
    else:
        result = db['authors'].update_one({'author_id': put_id}, {'$set': data})
    client.close()
    return result.modified_count


def post_book_author(item, book_or_author):
    """
    return the num of modified document (0 - insert new one, 1 - update one)
    given a book or author document
    """
    client = get_client()
    db = client[getenv('MONGODB_DB')]
    if book_or_author:
        result = db['books'].replace_one({'book_id': item['book_id']}, item, upsert=True)
    else:
        result = db['authors'].replace_one({'author_id': item['author_id']}, item, upsert=True)
    client.close()
    return result.modified_count


def delete_book_author_id(delete_id, book_or_author):
    """
    return the num of deleted document (0 - fail, 1 - succeed)
    given book or author id
    """
    client = get_client()
    db = client[getenv('MONGODB_DB')]
    if book_or_author:
        result = db['books'].delete_one({"book_id": delete_id})
    else:
        result = db['authors'].delete_one({"author_id": delete_id})
    client.close()
    return result.deleted_count == 1
