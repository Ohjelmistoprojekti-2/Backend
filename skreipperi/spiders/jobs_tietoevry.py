import scrapy
from scrapy.crawler import CrawlerProcess
import json
from json import JSONEncoder

jobPosts = []

class Post:
        def __init__(self, header, ala, company, url):
            self.header = header
            self.company = company
            self.url = url

class TietoevrySpider(scrapy.Spider):
    name = "tietoevry"

    def start_requests(self):
        urls = [
            (f'https://www.tietoevry.com/en/careers/search-our-jobs/?country=&city=&area=Application%20and%20Product%20Development&role=&organization=&q='),
        ]
        for url in urls:
            #tag = getattr(self, 'tag', None)

            #if tag is not None:
                #url = url + '?haku=' + tag
    
            yield scrapy.Request(url, self.parse)

    def parse(self, response):

        for job in response.css('a.jobResultRow'):
            if job.css('a.jobResultRow::text').get() != None:
                
                header = job.css('div:nth-child(1)::text').get(),
                company = 'Tietoevry',
                url = job.css('::attr(href)').get()
                
                p1 = Post(header, company, url)
                jobPosts.append(p1)

process = CrawlerProcess(settings = {
    'FEED_URI': 'tietoevry.json',
    'FEED_FORMAT': 'json'
})

process.crawl(TietoevrySpider)
process.start()

class JobEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__

def printList():

    jsonData = json.dumps(jobPosts, indent= 4, cls=JobEncoder)
    print(jsonData)

printList()