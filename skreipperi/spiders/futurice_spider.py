import scrapy
from scrapy.crawler import CrawlerProcess
import json
from json import JSONEncoder


jobPosts = []

class Post(scrapy.Item):                       
    header = scrapy.Field()
    ala = scrapy.Field()
    location = scrapy.Field()
    company = scrapy.Field()
    text = scrapy.Field()
    url = scrapy.Field()

class JobsSpider(scrapy.Spider):
    name = "jobs"


    def start_requests(self):
        urls = [
            "https://futurice.com/careers/open-positions"
        ]
        for url in urls:
            tag = getattr(self, 'tag', None)
            if tag is not None:
                url = url + '?haku=' + tag
            yield scrapy.Request(url, self.parse)

    def parse(self, response):

        for job in response.css('.css-ffhm6p'):
            if(job.css('.css-zsp0rz::text').get() == "Tech" or job.css('.css-zsp0rz::text').get() == "Cloud"): 
                if(job.css('.css-r04r1k::text').get() == "Helsinki" or job.css('.css-r04r1k::text').get() == "Tampere"):
                    header = job.css('.focusOnHover::text').get()
                    ala = job.css('.css-zsp0rz::text').get()
                    location = job.css('.css-r04r1k::text').get()
                    company = "Futurice"
                    url = "https://futurice.com/"+job.css('a::attr(href)').get()

                    request = scrapy.Request(url, callback=self.parse_following_page_Futurice)
                    request.cb_kwargs['header'] = header   ##lähetetään parse_following_page  jo haetut tiedot
                    request.cb_kwargs['ala'] = ala
                    request.cb_kwargs['location'] = location
                    request.cb_kwargs['company'] = company
                    request.cb_kwargs['url'] = url
                    yield request      ## vaatii jotta saadaan kutsuttua parse_following_page
    
    def parse_following_page_Futurice(self, response, header, ala, location, company, url):
        
        header = header
        ala = ala
        location = location
        company = company
        url = url
        text = response.css('div.css-b4zh0n  p').getall()   ##palauttaa listan

        new = Post(header=header, ala=ala, location=location, company=company, text=text, url=url)  
        jobPosts.append(new)  


process = CrawlerProcess()
process.crawl(JobsSpider)
process.start()


class JobEncoder(JSONEncoder):
        def default(self, o):
            return o.__dict__


def printList():

    jsonData = json.dumps(jobPosts, indent= 4, cls=JobEncoder)
    print(jsonData)

printList()