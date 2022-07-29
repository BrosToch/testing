import re

import requests
import scrapy
from scrapy.crawler import CrawlerProcess

# from src.setting import ROOT_DIR

HEADER = {
    'Referer': 'https://kohsantepheapdaily.com.kh/category/religious',
    'X-Requested-With': 'XMLHttpRequest',
    'Origin': 'https://kohsantepheapdaily.com.kh',
    'TE': 'Trailers',
    'DNT': '1',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Host': 'kohsantepheapdaily.com.kh',
    'Content-Length': '73'
}
URL = "https://kohsantepheapdaily.com.kh/wp-admin/admin-ajax.php"


class KohsantipheapSpider(scrapy.Spider):
    name = "Kohsantepheap Daily"

    start_urls = ['https://kohsantepheapdaily.com.kh/category/politic',
                #   'https://kohsantepheapdaily.com.kh/category/economic',
                #   'https://kohsantepheapdaily.com.kh/category/religious',
                #   'https://kohsantepheapdaily.com.kh/category/life-social',
                #   'https://kohsantepheapdaily.com.kh/category/entetaintment',
                #   'https://kohsantepheapdaily.com.kh/category/technology',
                  ]

    # custom_settings = {
    #     'FEED_FORMAT': 'pickle',
    #     'FEED_URI': str(ROOT_DIR / 'kohsantepheap.pickle'),
    # }

    @staticmethod
    
    def parse_article(response):
        yield {
            'url': response.url,
            'title': response.css('div.article-recap h1::text').get(),
            'content': '\n\n'.join(response.css('div.content-text p::text').extract()),
            'date': response.css('time.entry-date::text').extract()[0],
        }

    def parse(self, response):
        for each_article in response.css('h3.title a::attr(href)')[:2]:
            yield response.follow(each_article.get(), self.parse_article)

        for i in range(2, 10000):
            payload = f"action=kspg_ajax_category_load_more&paged={i}&terms%5B%5D=22&post-type=post"
            HEADER['Referer'] = response.url
            json_response = requests.request("POST", URL, headers=HEADER, data=payload)
            json_response = json_response.json()['post_items']

            if len(json_response) == 0:
                return

            for each in json_response:
                url = re.findall(r'href=[\'"]?([^\'" >]+)', each)[0]
                yield response.follow(url, self.parse_article)

            if len(json_response) < 22:
                return


if __name__ == '__main__':
    process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
    })

    process.crawl(KohsantipheapSpider)
    process.start()
