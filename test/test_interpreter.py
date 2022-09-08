from unittest import TestCase
from goodreads.interpreter import parse


class TestInterpreter(TestCase):
    def test_not(self):
        obj, query = parse('book.rating_count:NOT 123')
        self.assertEqual(obj, 'book')
        self.assertTrue('rating_count' in query)
        self.assertTrue('$not' in query['rating_count'])
        self.assertEqual(123, query['rating_count']['$not'])

    def test_and(self):
        obj, query = parse('author.rating: 4.0 AND 3.5')
        self.assertEqual(obj, 'author')
        self.assertTrue('$and' in query)
        self.assertTrue('rating' in query['$and'][0])
        self.assertEqual(4.0, query['$and'][0]['rating'])

    def test_or(self):
        obj, query = parse('book.review_count: 4 OR 100')
        self.assertEqual(obj, 'book')
        self.assertTrue('$or' in query)
        self.assertTrue('review_count' in query['$or'][1])
        self.assertEqual(100, query['$or'][1]['review_count'])

    def test_ge(self):
        obj, query = parse('book.ISBN: > 100')
        self.assertTrue('ISBN' in query)
        self.assertTrue('$gt' in query['ISBN'])
        self.assertEqual(100, query['ISBN']['$gt'])

    def test_ge(self):
        obj, query = parse('author.rating: < 4.8')
        self.assertTrue('rating' in query)
        self.assertTrue('$lt' in query['rating'])
        self.assertEqual(4.8, query['rating']['$lt'])

    def test_exact_search(self):
        obj, query = parse('book.rating: "4.1"')
        self.assertTrue('rating' in query)
        self.assertEqual(4.1, query['rating'])

    def test_search_term(self):
        obj, query = parse('book.image_url: moon')
        self.assertTrue('image_url' in query)
        self.assertTrue('$regex' in query['image_url'])
        self.assertEqual('.*moon.*', query['image_url']['$regex'])

    def test_empty_and_block(self):
        self.assertRaises(TypeError, parse, target='author.rating: AND')

    def test_empty_query(self):
        obj, query = parse('book.image_url:')
        self.assertTrue('image_url' in query)
        self.assertEqual(None, query['image_url'])

    def test_invalid_object(self):
        self.assertRaises(ValueError, parse, target='xxx.xxx:')

    def test_invalid_field(self):
        self.assertRaises(ValueError, parse, target='book.xxx:')

    def test_exact_extra(self):
        self.assertRaises(ValueError, parse, target='book.author: x"rob"')

    def test_type_mismatch(self):
        self.assertRaises(TypeError, parse, target='book.rating:xx')

    def test_type_mismatch_with_operator(self):
        self.assertRaises(TypeError, parse, target='book.rating:<xx')

