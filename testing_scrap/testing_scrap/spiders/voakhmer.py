
from gc import callbacks
import scrapy
from scrapy.crawler import CrawlerProcess

class Voakhmer(scrapy.Spider):
    name = "Voakhmer"
    allowed_domains = ['khmer.voanews.com']

    start_urls = [
                    'https://khmer.voanews.com/z/2277?',
                    # u'https://khmer.voanews.com/z/2291',
                    # u'https://khmer.voanews.com/z/2290',
                    # u'https://khmer.voanews.com/z/7115',
                    # u'https://khmer.voanews.com/z/6941'
                  ][:1]


    # def parse(self, response ):
    #     for post in response.css('div.media-block span::text'):
    #         yield{
    #             'date': post.css('.media-block__content  span::text').get(),
    #             'title': post.css('.media-block__content a h4::text').get(),
    #             'content': post.css('.media-block__content a p::text').get()
    #         }
    #     next_page =response.css('a.link-showMore::attr(href').get()
    #     if next_page is not None:
    #         next_page = response.urljoin(next_page)
    #         yield scrapy.Request(next_page, callback=self.parse)
        
    @staticmethod
    def parse_article(response):
        yield {
            'url': response.url,
            'title': response.css('div.col-title h1::text').get(),
            'action': response.css('figure figcaption span::text').get(),
            'content': response.css('div.wsw p::text').extract(),
            # 'date': response.css('span.date time::text')[1].extract()
        }

    def parse(self, response):
        for each_article in response.css('div.media-block__content a::attr(href)').extract():
            yield response.follow(each_article, self.parse_article)
        print(response.css('div.media-block__content a::attr(href)').extract())
        next_page = response.url.split("=")
        next_page[-1] = str(int(next_page[-1]) + 1)
        next_page = '='.join(next_page)
        yield scrapy.Request(next_page, callback=self.parse)
        
       
        
        
        # next = response.css('p.buttons a::attr(href)').get()
        # if next is not None:
        #     next = response.urljoin(next)
        #     yield scrapy.Request(next, callback=self.parse_article)


if __name__ == '__main__':
    process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
    })

    process.crawl(Voakhmer)
    process.start()
