from os import getenv
from bson.json_util import dumps, loads
from dotenv import load_dotenv

from goodreads.db.db_helper import get_client


def import_json(path):
    """
    Import the JSON file and update the db accordingly
    :param path: The path to import from
    """
    load_dotenv()
    client = get_client()
    db = client[getenv('MONGODB_DB')]

    with open(path) as file:
        file_string = file.read()
    try:
        file_data = loads(file_string)
    except ValueError as error:
        raise ValueError('JSON decode error.') from error

    # insert books from JSON file into db
    for book in file_data.get('books'):
        if 'book_id' in book:
            db['books'].replace_one({'book_id': book['book_id']}, book, upsert=True)
        else:
            raise ValueError('No book id.')

    # insert authors from JSON file into db
    for author in file_data.get('authors'):
        if 'author_id' in author:
            db['authors'].replace_one({'author_id': author['author_id']}, author, upsert=True)
        else:
            raise ValueError('No author id.')

    client.close()


# citation https://www.geeksforgeeks.org/convert-pymongo-cursor-to-json/
def export_json(path):
    """
    Export data from db to the given JSON file
    :param path: The path to export to
    """
    load_dotenv()
    client = get_client()
    db = client[getenv('MONGODB_DB')]
    books_cursor = db['books'].find()
    books_list_cur = list(books_cursor)

    authors_cursor = db['authors'].find()
    authors_list_cur = list(authors_cursor)

    json_dict = {'books': books_list_cur, 'authors': authors_list_cur}

    json_data = dumps(json_dict, indent=2)

    with open(path, 'w+') as file:
        file.write(json_data)

    client.close()
