import scrapy

class PostsSpider(scrapy.Spider):
    name = "posts"
    start_urls = [
        'https://books.toscrape.com/catalogue/page-1.html'
    ]

    def parse(self, response):
        book_titles = response.xpath('//*[@id="default"]/div/div/div/div/section/div[2]/ol/li/article/h3/a/@title').getall()
        book_ratings = response.xpath('//*[@id="default"]/div/div/div/div/section/div[2]/ol/li/article/p/@class').getall()
        book_prices = response.xpath('//*[@id="default"]/div/div/div/div/section/div[2]/ol/li/article/div[2]/p[1]//text()').getall()
        book_availability = response.xpath('//*[@id="default"]/div/div/div/div/section/div[2]/ol/li/article/div[2]/p[2]/text()').re('[^ ^\n].*')
        books = []
        
        for i in range(len(book_titles)):
            book = {
                'title': book_titles[i], 
                'rating': book_ratings[i], 
                'price': book_prices[i], 
                'availability': book_availability[i]
            }
            books.append(book)
        
        yield {
            'books': books
        }
        
        next_page = response.css('li.next a::attr(href)').get()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)
