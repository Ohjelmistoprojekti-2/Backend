import scrapy
from scrapy.crawler import CrawlerProcess
import json
from json import JSONEncoder


jobPosts = []

class Post:
        def __init__(self, header, ala, company, url):
            self.header = header
            self.ala = ala
            self.company = company
            self.url = url

class JobsSpider(scrapy.Spider):
    name = "jobs"


    def start_requests(self):
        urls = [
            "https://futurice.com/careers/open-positions?category=tech"
        ]
        for url in urls:
            tag = getattr(self, 'tag', None)
            if tag is not None:
                url = url + '?haku=' + tag
            yield scrapy.Request(url, self.parse)

    def parse(self, response):

        for job in response.css('.css-ffhm6p'):
            if(job.css('.css-zsp0rz::text').get() == "Tech"):

                header = job.css('.focusOnHover::text').get()
                ala = job.css('.css-zsp0rz::text').get()
                company = "Futurice"
                url = "https://futurice.com/"+job.css('a::attr(href)').get()

                p1 = Post(header, ala, company, url)
                print(p1.header)
                jobPosts.append(p1)

class JobsReaktor(scrapy.Spider):
    name = "reaktor"

    def start_requests(self):

        urls = [
            'https://www.reaktor.com/careers/#careers',
        ]
        for url in urls:
            yield scrapy.Request(url, self.parse)

    def parse(self, response):
        
        for job in response.css('a.filter-career-post'):
            if job.css('div h2::text').get() != None:
                    header = job.css('div h2::text').get()
                    ala = 'Tech'
                    company = 'Reaktor'
                    url = job.css('::attr(href)').get()

                    p1 = Post(header, ala, company, url)
                    print(p1.header)
                    jobPosts.append(p1)

process = CrawlerProcess()
process.crawl(JobsSpider)
process.crawl(JobsReaktor)
process.start()


class JobEncoder(JSONEncoder):
        def default(self, o):
            return o.__dict__


def printList():

    jsonData = json.dumps(jobPosts, indent= 4, cls=JobEncoder)
    print(jsonData)

printList()