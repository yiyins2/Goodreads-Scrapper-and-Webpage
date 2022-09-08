import scrapy
from scrapy import spiders


class GoodReadsSpider(spiders.Spider):
    """
    goodreads spider to parse the author page and book page
    """
    name = 'scrapper'
    author_id_set = set()
    book_id_set = set()

    start_urls = []

    BOOK_SHOW_STR_LEN = 10
    AUTHOR_SHOW_STR_LEN = 12

    def __init__(self, max_authors=50, max_books=200,
                 start_urls='https://www.goodreads.com/book/show/3735293-clean-code', **kwargs):
        super().__init__(**kwargs)
        self.max_authors = max_authors
        self.max_books = max_books
        self.start_urls.append(start_urls)

    def parse(self, response, **kwargs):
        if self.start_urls[-1].startswith('https://www.goodreads.com/book/show/'):
            yield from self.books_parse(response=response)
        if self.start_urls[-1].startswith('https://www.goodreads.com/author/show/'):
            yield from self.authors_parse(response=response)

    def books_parse(self, response, **kwargs):
        """
        Parse a book page and yield this item.
        Call author_parse for the author of this book.
        Call similar_books_parse to parse similar books.
        """
        book_id = int(response.xpath('//*[@id="book_id"]/@value').get())

        # parse isbn
        info_box = response.xpath('//div[@class="infoBoxRowTitle"]/text()').extract()
        try:
            isbn_idx = info_box.index('ISBN')
        except ValueError:
            isbn_idx = -1
        isbn = ''
        if isbn_idx >= 0:
            isbn = response.xpath('//div[@class="infoBoxRowItem"]/text()').\
                extract()[isbn_idx].strip()
            isbn = ''.join(c for c in isbn if c.isdigit())

        author_url = response.xpath('//*[@id="bookAuthors"]/span[2]/div/a/@href').get(default='')
        data = {
            'book_url':         response.url,
            'title':            response.xpath('//*[@id="bookTitle"]/text()').get().strip(),
            'book_id':          book_id,
            'ISBN':             isbn,
            'author_url':       author_url,
            'author':
                response.xpath('//*[@id="bookAuthors"]/span[2]/div/a/span/text()').get(default=''),
            'rating':
                float(response.xpath('//*[@id="bookMeta"]/span[2]/text()').get(default='')),
            'rating_count':
                int(response.xpath('//*[@id="bookMeta"]/a[2]/meta/@content').get(default='')),
            'review_count':
                int(response.xpath('//*[@id="bookMeta"]/a[3]/meta/@content').get(default='')),
            'image_url':
                response.xpath('//*[@id="coverImage"]/@src').get(default='')}

        # parse this author
        yield from self.find_author_id_and_yield(author_url)

        # parse similar books
        similar_books_url = \
            response.xpath('//*[@class="actionLink right seeMoreLink"]/@href').get(default='')
        if similar_books_url.startswith('https://www.goodreads.com/book/similar/'):
            yield scrapy.Request(similar_books_url,
                                 callback=self.similar_books_parse, meta={'data': data})

    def similar_books_parse(self, response, **kwargs):
        """
        Parse the list of similar books and return the results to book_parse.
        Call book_parse on the list of similar books.
        """
        data = response.meta['data']
        similar_books = []
        similar_books_name = []
        hrefs = response.xpath('//a[@class="gr-h3 gr-h3--serif gr-h3--noMargin"]/@href').extract()
        names = response.xpath('//span[@itemprop="name"]/text()').extract()
        if len(hrefs) <= 1:
            data['similar_books'] = similar_books
            data['similar_books_name'] = similar_books_name
        else:
            # parse all similar books
            for i in range(1, len(hrefs)):
                full_href = response.urljoin(hrefs[i])
                similar_books.append(full_href)
                similar_books_name.append(names[i])
                yield from self.find_book_id_and_yield(full_href)
            data['similar_books'] = similar_books
            data['similar_books_name'] = similar_books_name
        yield data

    def authors_parse(self, response, **kwargs):
        """
        Parse an author page and yield this item.
        Call books_parse for all books written by the author.
        Call similar_authors_parse to parse similar authors.
        """
        author_id = response.meta['author_id']
        data = {
            'name': 
                response.xpath('//span[@itemprop="name"]/text()').get(default=''),
            'author_url':       response.url,
            'author_id':        author_id,
            'rating':
                float(response.xpath('//span[@itemprop="ratingValue"]/text()').get(default='')),
            'rating_count':
                int(response.xpath('//span[@itemprop="ratingCount"]/@content').get(default='')),
            'review_count':
                int(response.xpath('//span[@itemprop="reviewCount"]/@content').get(default='')),
            'image_url':
                response.xpath(
                    '/html/body/div[2]/div[3]/div[1]/div[2]/div[3]/div[1]/a/img/@src').get(default='')
        }
        author_books = []
        author_books_name = []
        hrefs = response.xpath('//a[@class="bookTitle"]/@href').extract()
        names = response.xpath('//span[@itemprop="name" and @role="heading"]/text()').extract()

        # parse all books written by this author
        
        for i in range(1, len(hrefs)):
            author_books_name.append(names[i])
            full_href = response.urljoin(hrefs[i])
            author_books.append(full_href)
            yield from self.find_book_id_and_yield(full_href)

        data['author_books'] = author_books
        data['author_books_name'] = author_books_name

        # parse similar authors
        similar_authors_url = response.urljoin('/author/similar/' + str(data["author_id"]))
        yield scrapy.Request(similar_authors_url,
                             callback=self.similar_authors_parse, meta={'data': data})

    def similar_authors_parse(self, response, **kwargs):
        """
        Parse the list of similar authors and return the results to authors_parse.
        Call authors_parse on the list of similar authors.
        """
        data = response.meta['data']
        similar_authors = []
        similar_authors_name = []
        hrefs = response.xpath('//a[@class="gr-h3 gr-h3--serif gr-h3--noMargin"]/@href').extract()
        names = response.xpath('//span[@itemprop="name"]/text()').extract()
        if len(hrefs) <= 1:
            data['similar_authors'] = similar_authors
            data['similar_authors_name'] = similar_authors_name
        else:
            # parse all similar authors
            for i in range(1, len(hrefs)):
                full_href = response.urljoin(hrefs[i])
                similar_authors.append(full_href)
                similar_authors_name.append(names[i])
                yield from self.find_author_id_and_yield(full_href)

            data['similar_authors'] = similar_authors
            data['similar_authors_name'] = similar_authors_name
        yield data

    def find_author_id_and_yield(self, full_href):
        """
        help function to find the author_id given the URL, and call authors_parse on the URL.
        :param full_href: the author page URL
        """
        author_id_start = full_href.find('author/show/') + self.AUTHOR_SHOW_STR_LEN
        if author_id_start == self.AUTHOR_SHOW_STR_LEN - 1:
            return
        author_id_end = max(full_href.find('.', author_id_start),
                            full_href.find('-', author_id_start))
        author_id_str = full_href[author_id_start:author_id_end]
        if author_id_str != '':
            author_id = int(author_id_str)
            if len(self.author_id_set) <= self.max_authors and author_id not in self.author_id_set:
                self.author_id_set.add(author_id)
                yield scrapy.Request(full_href,
                                     callback=self.authors_parse, meta={'author_id': author_id})

    def find_book_id_and_yield(self, full_href):
        """
        help function to find the book_id given the URL, and call books_parse on the URL.
        :param full_href: the book page URL
        """
        book_id_start = full_href.find('book/show/') + self.BOOK_SHOW_STR_LEN
        if book_id_start == self.BOOK_SHOW_STR_LEN - 1:
            return
        book_id_end = max(full_href.find('.', book_id_start), full_href.find('-', book_id_start))
        book_id = int(full_href[book_id_start:book_id_end])
        if len(self.book_id_set) <= self.max_books:
            if book_id not in self.book_id_set:
                self.book_id_set.add(book_id)
                yield scrapy.Request(full_href, callback=self.books_parse)
