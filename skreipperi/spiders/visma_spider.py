import scrapy
from scrapy.crawler import CrawlerProcess
import json
from json import JSONEncoder

jobPosts = []
class VismaSpider(scrapy.Spider):
    name = "visma_jobs"
    start_urls = ['https://ats.talentadore.com/positions/rJ4tqSR/rss?v=2&language=en%2Cfi&tags=&notTags=Visma+Legal+avoin+hakemus&businessUnits=&notBusinessUnits=&display_description=job_description&categories=tags_and_extras']
    
    

    def parse(self, response):
        
        class Post:
            def __init__(self, header, ala, company, url):
                self.header = header
                self.ala = ala
                self.company = company
                self.url = url
        


        for job in response.xpath('//channel/item'):
            
              header = job.xpath('title//text()').extract_first()
              ala = 'Tech'
              company = job.xpath('dc.creator//text()').extract_first()
              url =  job.xpath('link//text()').extract_first()

              new = Post(header, ala, company, url)   
              jobPosts.append(new)
              
              
process = CrawlerProcess()
process.crawl(VismaSpider)
process.start()


class JobEncoder(JSONEncoder):
        def default(self, o):
            return o.__dict__


def printList():  
    jsonData = json.dumps(jobPosts, indent= 4, cls=JobEncoder)
    print(jsonData)
    return jsonData

printList()           