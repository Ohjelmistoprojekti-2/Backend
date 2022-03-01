import scrapy
from scrapy.crawler import CrawlerProcess
import json
from json import JSONEncoder


jobPosts = []

class Post(scrapy.Item):                       
    header = scrapy.Field()
    ala = scrapy.Field()
    company = scrapy.Field()
    text = scrapy.Field()
    url = scrapy.Field()

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

                request = scrapy.Request(url, callback=self.parse_following_page_Futurice)
                request.cb_kwargs['header'] = header   ##lähetetään parse_following_page  jo haetut tiedot
                request.cb_kwargs['ala'] = ala
                request.cb_kwargs['company'] = company
                request.cb_kwargs['url'] = url
                yield request      ## vaatii jotta saadaan kutsuttua parse_following_page
    
    def parse_following_page_Futurice(self, response, header, ala, company, url):
        
        header = header
        ala = ala
        company = company
        url = url
        text = response.css('div.css-b4zh0n  p').getall()   ##palauttaa listan

        new = Post(header=header, ala=ala, company=company, text=text, url=url)  
        jobPosts.append(new)  

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

                    request = scrapy.Request(url, callback=self.parse_following_page_Reaktor)
                    request.cb_kwargs['header'] = header   ##lähetetään parse_following_page  jo haetut tiedot
                    request.cb_kwargs['ala'] = ala
                    request.cb_kwargs['company'] = company
                    request.cb_kwargs['url'] = url
                    yield request      ## vaatii jotta saadaan kutsuttua parse_following_page
    
    def parse_following_page_Reaktor(self, response, header, ala, company, url):
        
        header = header
        ala = ala
        company = company
        url = url
        text = response.css('div.col.col6-ns.col12.offset1-l.blog-copy  span::text').getall()   ##palauttaa listan
        text = text + response.css('div.col.col6-ns.col12.offset1-l.blog-copy  p::text').getall()

        new = Post(header=header, ala=ala, company=company, text=text, url=url)  
        jobPosts.append(new)


process = CrawlerProcess()
#process.crawl(JobsSpider)
process.crawl(JobsReaktor)
process.start()


class JobEncoder(JSONEncoder):
        def default(self, o):
            return o.__dict__


def printList():

    jsonData = json.dumps(jobPosts, indent= 4, cls=JobEncoder)
    print(jsonData)

printList()