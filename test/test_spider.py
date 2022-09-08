from unittest import TestCase
from goodreads.scrapper import spider


class TestGoodReadsSpider(TestCase):
    def test_find_author_id_and_yield(self):
        spider_new = spider.GoodReadsSpider()
        requests = list(spider_new.find_author_id_and_yield("https://www.goodreads.com/author/show/395812.Yuval_Noah_Harari"))
        self.assertTrue(requests)

    def test_find_book_id_and_yield(self):
        spider_new = spider.GoodReadsSpider()
        requests = list(spider_new.find_book_id_and_yield("https://www.goodreads.com/book/show/142296.The_Anubis_Gates"))
        self.assertTrue(requests)
