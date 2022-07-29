import scrapy
from scrapy.crawler import CrawlerProcess

# from src.setting import ROOT_DIR

# https://www.postkhmer.com/p?=id

class PostKhmer(scrapy.Spider):
    name = "PostKhmer"

    start_urls = [u'https://www.postkhmer.com/ព័ត៌មានជាតិ?page=0',
                  u'https://www.postkhmer.com/អន្តរជាតិ?page=0',
                  u'https://www.postkhmer.com/ជីវិតកម្សាន្ត?page=0',
                  u'https://www.postkhmer.com/ទេសចរណ៍?page=0',
                  u'https://www.postkhmer.com/កីឡា?page=0',
                  
                  ][:1]

    # custom_settings = {
    #     'FEED_FORMAT': 'pickle',.
    #     'FEED_URI': str(ROOT_DIR / 'postkhmer.pickle'),
    # }

    @staticmethod
    def parse_article(response):
        yield {
            'url': response.url,
            'title': response.css('div.single-article-header h2::text').get(),
            'content': '\n\n'.join(response.css('div.paragraph-style p::text').extract()),
            'date': response.css('div.article-author-wrapper p::text')[1].extract()
        }

    def parse(self, response):
        for each_article in response.css('div.article-image a::attr(href)').extract():
            yield response.follow(each_article, self.parse_article)

        # next_page = response.url.split('=')
        # next_page[-1] = str(int(next_page[-1]) + 1)
        # next_page = '='.join(next_page)
        # yield scrapy.Request(next_page, callback=self.parse)


if __name__ == '__main__':
    process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
    })

    process.crawl(PostKhmer)
    process.start()
