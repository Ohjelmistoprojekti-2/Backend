import scrapy
from scrapy.crawler import CrawlerProcess
import json
from json import JSONEncoder

jobPosts = []

class Post(scrapy.Item):
       ## def __init__(self, header, ala, company, url):
            header = scrapy.Field()
            ala = scrapy.Field()
            company = scrapy.Field()
            text = scrapy.Field()
            url = scrapy.Field()

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
                ala = 'Tech'
                company = 'Tietoevry',
                url = job.css('::attr(href)').get()
                
               



            request = scrapy.Request(url, callback=self.parse_following_page)
            request.cb_kwargs['header'] = header   #lähetetään parse_following_page  jo haetut tiedot
            request.cb_kwargs['ala'] = ala
            request.cb_kwargs['company'] = company
            request.cb_kwargs['url'] = url
            yield request             # vaatii jotta saadaan kutsuttua parse_following_page

    def parse_following_page(self, response, header, ala, company, url):
        
        header = header
        ala = ala
        company = company
        url = url
        textlist = response.css('divGWTCKEditor-Disabled  p').getall()   #ei palauta vielä mitään
        text_untrimmed=' '.join([str(text)for text in textlist])
        text_untrimmed=text_untrimmed.replace('<p>','')
        text = text_untrimmed.replace('</p>','')  #palautettu lista trimataan
                                                    #tähän voisi keksiä jonkun fiksumman keinon jos päätetään pitää tekstin näyttäminen


       # if 'Java' in text:                      #Jos tekstistä löytyy 'Java' niin printaa sen työn tiedot
        p1 = Post(header=header, ala=ala, company=company, text=text, url=url)  
        jobPosts.append(p1)

        #else:
        #   pass 

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