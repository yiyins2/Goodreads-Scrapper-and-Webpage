"""
Command line runner
"""
import argparse
import sys
import warnings
import os
from pathlib import Path
from dotenv import load_dotenv

from goodreads.api import fill_in_book, fill_in_author, post_books_str, post_authors_str
from goodreads.db import db_helper
from goodreads.scrapper.processor import crawl
from goodreads.json_handler import export_json, import_json
from bson.json_util import loads, dumps
from goodreads.interpreter import parse
from multiprocessing import Process


def extension_start():
    """
    start the extension and get the action
    """
    while True:
        print('Which action do you want to perform next? GET, PUT, POST, DELETE')
        action_input = input('Action:')
        if action_input == 'PUT':
            ext_put()
        elif action_input == 'POST':
            ext_post()
        elif action_input == 'GET':
            ext_get()
        elif action_input == 'DELETE':
            ext_delete()
        else:
            print("Invalid action!")
            extension_start()


def get_id(book_or_author):
    """
    keep asking for id until valid
    """
    if book_or_author:
        print('Please enter the book id:')
    else:
        print('Please enter the author id:')
    input_id = input('id:')
    try:
        input_id = int(input_id)
        if input_id < 0:
            print("ID cannot be negative!")
            get_id(book_or_author)
        else:
            return input_id
    except ValueError:
        print("Non-integer ID!")
        get_id(book_or_author)


def get_json():
    """
    asking for JSON until valid
    """
    print('Please enter the query:')
    query = input('query:')
    try:
        data = loads(query)
        return data
    except ValueError:
        print("Invalid JSON")
        get_json()


def ext_put():
    """
    run the put action
    """
    while True:
        print('Which PUT command do you want to perform next? book_id, author_id')
        command_input = input('command:')
        if command_input == 'book_id':
            input_id = get_id(True)
            data = get_json()
            result = db_helper.put_book_author_id(input_id, data, True)
            if result is None:
                print("No such book ID is found!")
            else:
                print("Successfully updated document with book id: " + str(input_id))
            restart()
        elif command_input == 'author_id':
            input_id = get_id(False)
            data = get_json()
            result = db_helper.put_book_author_id(input_id, data, False)
            if result is None:
                print("No such author ID is found!")
            else:
                print("Successfully updated document with author id: " + str(input_id))
            restart()
        else:
            print("Invalid command!")
            ext_put()


def ext_post():
    """
    run the post action
    """
    print('Which POST command do you want to perform next? book, books, author, authors, scrape')
    command_input = input('command:')
    if command_input == 'book':
        data = get_json()
        book_id = data['book_id']
        if book_id is not None:
            result = db_helper.post_book_author(fill_in_book(data), True)
            if result is 0:
                print("Successfully inserted the new book")
            else:
                print("Successfully modified document with book id: " + str(book_id))
            restart()
        else:
            print("Your book does not have an ID")
            ext_post()
    elif command_input == 'books':
        data = get_json()
        print(post_books_str(data))
        restart()
    elif command_input == 'books':
        data = get_json()
        author_id = data['author_id']
        if author_id is not None:
            result = db_helper.post_book_author(fill_in_author(data), False)
            if result is 0:
                print("Successfully inserted the new author")
            else:
                print("Successfully modified document with author id: " + str(author_id))
                restart()
        else:
            print("Your author does not have an ID")
            ext_post()
    elif command_input == 'authors':
        data = get_json()
        print(post_authors_str(data))
        restart()
    elif command_input == 'scrape':
        start_url = get_url()
        p = Process(target=crawl, kwargs={'start_url': start_url, 'max_books': 1, 'max_authors': 1})
        p.start()
        p.join()
        return "Successfully crawled the URL: " + start_url
    else:
        print("Invalid command!")
        ext_post()


def get_url():
    """
    keep asking for url until valid
    """
    print('Please enter the URL:')
    start_url = input('URL:')
    if not start_url.startswith('https://www.goodreads.com/book/show/') and \
            not start_url.startswith('https://www.goodreads.com/author/show/'):
        print("Invalid URL")
        get_url()
    return start_url


def ext_get():
    """
    run the get action
    """
    print('Which GET command do you want to perform next? book_id, author_id, search')
    command_input = input('command:')
    if command_input == 'book_id':
        input_id = get_id(True)
        result = db_helper.get_book_author_id(input_id, True)
        if result is None:
            print("No such author ID is found!")
        else:
            result.pop('_id')
            print(dumps(result))
        restart()
    elif command_input == 'author_id':
        input_id = get_id(True)
        result = db_helper.get_book_author_id(input_id, True)
        if result is None:
            print("No such author ID is found!")
        else:
            result.pop('_id')
            print(dumps(result))
        restart()
    elif command_input == 'search':
        parse_obj, parse_query = get_search_attr()
        if parse_obj == 'book':
            results = db_helper.get_search(parse_query, True)
        else:
            results = db_helper.get_search(parse_query, False)
        print(dumps(list(results)))
        restart()
    else:
        print("Invalid command!")
        ext_get()


def get_search_attr():
    """
    keep asking for search attributes until valid
    """
    print('Please enter the search query:')
    query = input('query:')
    try:
        return parse(query)
    except (TypeError, ValueError):
        print("Invalid query!")
    get_search_attr()


def ext_delete():
    """
    run the delete action
    """
    print('Which DELETE command do you want to perform next? book_id, author_id')
    command_input = input('command:')
    if command_input == 'book_id':
        input_id = get_id(True)
        result = db_helper.delete_book_author_id(input_id, False)
        if result:
            print("Successfully deleted document with book ID: " + str(input_id))
        else:
            print("No such book ID is found!")
        restart()
    elif command_input == 'author_id':
        input_id = get_id(True)
        result = db_helper.delete_book_author_id(input_id, False)
        if result:
            print("Successfully deleted document with author ID: " + str(input_id))
        else:
            print("No such author ID is found!")
        restart()
    else:
        print("Invalid command!")
        ext_delete()


def restart():
    """
    back to extension start
    """
    print("Back to start.")
    extension_start()

class CommandLine:
    """
    Command line class to start a new command, check the arguments, and run the command
    """
    def __init__(self, argv):
        load_dotenv()

        # create all arguments
        self.parser = argparse.ArgumentParser(description='')

        self.parser.add_argument('--extension', action='store_true')
        self.url_arg = self.parser.add_argument('--start_url',
            type=str, default='https://www.goodreads.com/book/show/3735293-clean-code')
        self.max_authors_arg = self.parser.add_argument('--max_authors', type=int, default=50)
        self.max_books_arg = self.parser.add_argument('--max_books', type=int, default=200)
        self.import_json_arg = self.parser.add_argument('--import_json', type=Path, default=None)
        self.export_json_arg = self.parser.add_argument('--export_json', type=Path, default=None)

        self.args = self.parser.parse_args(argv)

    def check_args(self):
        """
        Check arguments are valid, raise error or warning if invalid
        """
        if not self.args.start_url.startswith('https://www.goodreads.com/book/show/') and \
                not self.args.start_url.startswith('https://www.goodreads.com/author/show/'):
            raise argparse.ArgumentError(self.url_arg, 'Invalid URL.')

        if self.args.max_authors < 0:
            raise argparse.ArgumentError(
                self.max_authors_arg, 'Max number of authors cannot be negative.')

        if self.args.max_authors > 50:
            warnings.warn('Max number of authors is too large (> 50).')

        if self.args.max_books < 0:
            raise argparse.ArgumentError(
                self.max_books_arg, 'Max number of books cannot be negative.')

        if self.args.max_books > 200:
            warnings.warn('Max number of books is too large (> 200).')

        if self.args.import_json and not os.path.isfile(self.args.import_json):
            raise argparse.ArgumentError(self.import_json_arg, 'JSON file does not exist.')

    def run(self):
        """
        Run with valid arguments
        """
        if self.args.extension:
            extension_start()
        if self.args.import_json is not None:
            import_json(self.args.import_json)
        elif self.args.export_json is not None:
            export_json(self.args.export_json)
        else:
            print(self.args.start_url)
            crawl(start_url=self.args.start_url,
                  max_authors=self.args.max_authors, max_books=self.args.max_books)


if __name__ == "__main__":
    command_runner = CommandLine(sys.argv[1:])
    command_runner.check_args()
    command_runner.run()
