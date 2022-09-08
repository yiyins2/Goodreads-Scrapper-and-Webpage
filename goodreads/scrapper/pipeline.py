from os import getenv

from goodreads.db.db_helper import get_client


# citation https://docs.scrapy.org/en/latest/topics/item-pipeline.html
class Pipeline:
    collection_name = 'scrapy_items'

    def __init__(self):
        self.client = None
        self.db = None

    @classmethod
    def from_crawler(cls, crawler):
        """
        Create a pipeline instance from the crawler.
        """
        return cls()

    def open_spider(self, spider):
        """
        Connect to the mongodb client and get the collection.
        """
        self.client = get_client()
        self.db = self.client[getenv('MONGODB_DB')]

    def close_spider(self, spider):
        """
        Close the mongodb client.
        """
        self.client.close()

    def process_item(self, item, spider):
        """
        Insert book or author item into the db.
        :param spider: The spider to crawl
        :param item: The item to insert into db
        """
        if 'book_id' in item:
            self.db['books'].replace_one({'book_id': item['book_id']}, item, upsert=True)
        else:
            self.db['authors'].replace_one({'author_id': item['author_id']}, item, upsert=True)
        return item
