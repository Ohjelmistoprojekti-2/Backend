from re import I
import scrapy
from urllib import request
from scrapy.crawler import CrawlerProcess
import json
from json import JSONEncoder

jobPosts = []

class Post(scrapy.Item):
    header = scrapy.Field()
    ala = scrapy.Field()
    company = scrapy.Field()
    location = scrapy.Field()
    text = scrapy.Field()
    url = scrapy.Field()


class SiiliSpider(scrapy.Spider):
    name = "siili"
    start_urls = ['https://www.siili.com/join-us']
        
    def parse(self, response):
        for job in response.css('li.c-careers__position-row'):
            
            header = job.css('h4 a::text').extract_first()
            ala = 'Tech'
            company = 'Siili Solutions'
            locationLong = job.css('span.paragraph-3.siili__color--grey.c-careers-city::text').extract_first()
            location = locationLong.split("/")[0]
            url = "https://siili.com"+job.css('a.c-careers__link::attr(href)').extract_first()

            request = scrapy.Request(url, callback=self.parse_following_page)
            request.cb_kwargs['header'] = header
            request.cb_kwargs['ala'] = ala
            request.cb_kwargs['company'] = company
            request.cb_kwargs['location'] = location
            request.cb_kwargs['url'] = url
            yield request

    def parse_following_page(self, response, header, ala, company, location, url):
        header = header
        ala = ala
        company = company
        location = location
        url = url
        text = response.css('div.span6.c-careers__content p::text').getall()

            # if 'Java' in text:
        new = Post(header=header, ala=ala, company=company, location=location, text=text, url=url)
        jobPosts.append(new)

process = CrawlerProcess()
process.crawl(SiiliSpider)
process.start()

class JobEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__

def printList():
    jsonData = json.dumps(jobPosts, indent= 4, cls=JobEncoder)
    print(jsonData)
    return jsonData

printList()

        
