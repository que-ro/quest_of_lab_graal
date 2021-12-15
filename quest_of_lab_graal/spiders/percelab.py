import scrapy


class PercelabSpider(scrapy.Spider):
    name = 'percelab'
    allowed_domains = ['www.igbmc.fr']
    start_urls = ['https://www.igbmc.fr//']

    def parse(self, response):
        pass
