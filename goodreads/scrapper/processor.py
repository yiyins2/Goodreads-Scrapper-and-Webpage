from scrapy.crawler import CrawlerProcess

from goodreads.scrapper.spider import GoodReadsSpider


def crawl(start_url, max_authors, max_books):
    """
    Start a crawler process with the following settings.
    :param start_url: the start goodreads book URL
    :param max_authors: max num of authors to scrap
    :param max_books: max num of books to scrap
    """
    process = CrawlerProcess(settings={
        'BOT_NAME': 'goodreadspider',
        'ROBOTSTXT_OBEY': True,
        'AUTOTHROTTLE_ENABLED': True,
        'HTTPCACHE_ENABLED': True,
        "ITEM_PIPELINES": {
            'goodreads.scrapper.pipeline.Pipeline': 200
        }
    })
    process.crawl(GoodReadsSpider,
                  start_urls=start_url, max_authors=max_authors, max_books=max_books)
    process.start()
