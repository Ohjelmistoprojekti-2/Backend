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
                sijaintilistaus = job.css('div.f-paragraph-small.gray.flex.flex-wrap.items-center span::text').getall()
                header = job.css('div h2::text').get()
                ala = sijaintilistaus[0]
                location = sijaintilistaus[1]
                company = 'Reaktor'
                url = job.css('::attr(href)').get()

                request = scrapy.Request(
                    url, callback=self.parse_following_page_Reaktor)
                request.cb_kwargs['header'] = header
                request.cb_kwargs['ala'] = ala
                request.cb_kwargs['location'] = location
                request.cb_kwargs['company'] = company
                request.cb_kwargs['url'] = url
                yield request

    def parse_following_page_Reaktor(self, response, header, ala,location , company, url):

        header = header
        ala = ala
        location = location
        company = company
        url = url
        # palauttaa listan
        text = response.css(
            'div.col.col6-ns.col12.offset1-l.blog-copy  span::text').getall()
        textAll = text + \
            response.css(
                'div.col.col6-ns.col12.offset1-l.blog-copy  p::text').getall()
        text_trimmed = ' '.join([str(text)for text in textAll])

        new = Post(header=header, ala=ala,location = location ,company=company,
                   text=text_trimmed, url=url)
        jobPosts.append(new)



process = CrawlerProcess()
process.crawl(JobsReaktor)
process.start()


class JobEncoder(JSONEncoder):
        def default(self, o):
            return o.__dict__


def printList():  
    jsonData = json.dumps(jobPosts, indent= 4, cls=JobEncoder)
    #ref.set(jsonData)
    print(ref.get())
    return jsonData

printList()