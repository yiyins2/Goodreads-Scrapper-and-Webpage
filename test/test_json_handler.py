from os import getenv
from unittest import TestCase

from dotenv import load_dotenv

from goodreads.db.db_helper import get_client
from goodreads.json_handler import import_json


class TestJSONHandler(TestCase):
    def test_wrong_import(self):
        self.assertRaises(ValueError, import_json, path="test_json_files/no_book_id.json")

    def test_wrong_import(self):
        self.assertRaises(ValueError, import_json, path="test_json_files/no_author_id.json")

    def test_invalid_import(self):
        self.assertRaises(ValueError, import_json, path="test_json_files/invalid.json")

    def test_duplicate_book_import(self):
        import_json("test_json_files/duplicate.json")
        import_json("test_json_files/duplicate.json")
        load_dotenv()
        client = get_client()
        db = client[getenv('MONGODB_DB')]
        self.assertEqual(1, db["books"].count_documents({"book_id": 3735293}))
        client.close()
