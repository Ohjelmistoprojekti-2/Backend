
from urllib import request
import scrapy
from scrapy.crawler import CrawlerProcess
import json
from json import JSONEncoder

jobPosts = []

#luodaan luokka
class Post(scrapy.Item):                       
          ##def __init__(self, header, ala, company, text, url):
                header = scrapy.Field()
                ala = scrapy.Field()
                location = scrapy.Field()
                company = scrapy.Field()
                text = scrapy.Field()
                url = scrapy.Field()
class VismaSpider(scrapy.Spider):
    name = "visma_jobs"
    start_urls = ['https://ats.talentadore.com/positions/rJ4tqSR/rss?v=2&language=en%2Cfi&tags=&notTags=Visma+Legal+avoin+hakemus&businessUnits=&notBusinessUnits=&display_description=job_description&categories=tags_and_extras']
    
    
    

    def parse(self, response):
        


        for job in response.xpath('//channel/item'):
            
              header = job.xpath('title//text()').extract_first()
              ala = job.xpath('category[@domain="job_area"]//text()').extract_first()
              location = job.xpath('category[@domain="city"]//text()').extract()
              company = 'Visma'
              url =  job.xpath('link//text()').extract_first()
               
              request = scrapy.Request(url, callback=self.parse_following_page)
              request.cb_kwargs['header'] = header   #lähetetään parse_following_page  jo haetut tiedot
              request.cb_kwargs['location'] = location
              request.cb_kwargs['ala'] = ala
              request.cb_kwargs['company'] = company
              request.cb_kwargs['url'] = url
              yield request             # vaatii jotta saadaan kutsuttua parse_following_page

    def parse_following_page(self, response, header, ala, location, company, url):
        
        header = header
        ala = ala
        location = location
        company = company
        url = url
        textlist = response.css('div.job-ad-feature-description  p').getall()   #palauttaa listan
        text_untrimmed=' '.join([str(text)for text in textlist])
        text_untrimmed=text_untrimmed.replace('<p>','')
        text = text_untrimmed.replace('</p>','')  #palautettu lista trimataan
                                                    #tähän voisi keksiä jonkun fiksumman keinon jos päätetään pitää tekstin näyttäminen
        
        

        #if 'Java' in text:                      #Jos tekstistä löytyy 'Java' niin printaa sen työn tiedot
        new = Post(header=header, ala=ala, location=location, company=company, text=text, url=url)  
        jobPosts.append(new)

        #else:
           #pass 
         
        

              
              
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