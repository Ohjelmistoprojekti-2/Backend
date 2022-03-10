import scrapy
from scrapy.crawler import CrawlerProcess , CrawlerRunner
import json
from json import JSONEncoder
from cachetools import cached, TTLCache
import time
from twisted.internet import reactor, defer
from multiprocessing import Process


jobPosts = []



# class Post:
#     def __init__(self,header,ala,company,url,text):
#         self.header = header
#         self.ala = ala
#         self.company = company
#         self.url = url
#         self.text = text


class Post(scrapy.Item):
    header = scrapy.Field()
    ala = scrapy.Field()
    company = scrapy.Field()
    url = scrapy.Field()
    text = scrapy.Field()


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

                request = scrapy.Request(
                    url, callback=self.parse_following_page_Futurice)
                request.cb_kwargs['header'] = header
                request.cb_kwargs['ala'] = ala
                request.cb_kwargs['company'] = company
                request.cb_kwargs['url'] = url
                yield request

    def parse_following_page_Futurice(self, response, header, ala, company, url):

        header = header
        ala = ala
        company = company
        url = url
        textAll = response.css('div.css-b4zh0n  p::text').getall()
        text_trimmed = ' '.join([str(text)for text in textAll])

        new = Post(header=header, ala=ala, company=company,
                   text=text_trimmed, url=url)
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

                request = scrapy.Request(
                    url, callback=self.parse_following_page_Reaktor)
                request.cb_kwargs['header'] = header
                request.cb_kwargs['ala'] = ala
                request.cb_kwargs['company'] = company
                request.cb_kwargs['url'] = url
                yield request

    def parse_following_page_Reaktor(self, response, header, ala, company, url):

        header = header
        ala = ala
        company = company
        url = url
        # palauttaa listan
        text = response.css(
            'div.col.col6-ns.col12.offset1-l.blog-copy  span::text').getall()
        textAll = text + \
            response.css(
                'div.col.col6-ns.col12.offset1-l.blog-copy  p::text').getall()
        text_trimmed = ' '.join([str(text)for text in textAll])

        new = Post(header=header, ala=ala, company=company,
                   text=text_trimmed, url=url)
        jobPosts.append(new)


class VismaSpider(scrapy.Spider):
    name = "visma_jobs"
    start_urls = ['https://ats.talentadore.com/positions/rJ4tqSR/rss?v=2&language=en%2Cfi&tags=&notTags=Visma+Legal+avoin+hakemus&businessUnits=&notBusinessUnits=&display_description=job_description&categories=tags_and_extras']

    def parse(self, response):

        for job in response.xpath('//channel/item'):

            header = job.xpath('title//text()').extract_first()
            ala = 'Tech'
            company = 'Visma'
            url = job.xpath('link//text()').extract_first()

            request = scrapy.Request(url, callback=self.parse_following_page)
            # lähetetään parse_following_page  jo haetut tiedot
            request.cb_kwargs['header'] = header
            request.cb_kwargs['ala'] = ala
            request.cb_kwargs['company'] = company
            request.cb_kwargs['url'] = url
            yield request             # vaatii jotta saadaan kutsuttua parse_following_page

    def parse_following_page(self, response, header, ala, company, url):

        header = header
        ala = ala
        company = company
        url = url
        textlist = response.css(
            'div.job-ad-feature-description  p').getall()  # palauttaa listan
        text_untrimmed = ' '.join([str(text)for text in textlist])
        text_untrimmed = text_untrimmed.replace('<p>', '')
        text = text_untrimmed.replace('</p>', '')

        new = Post(header=header, ala=ala, company=company, text=text, url=url)
        jobPosts.append(new)


class SiiliSpider(scrapy.Spider):
    name = "siili"
    start_urls = ['https://www.siili.com/join-us']

    def parse(self, response):
        for job in response.css('li.c-careers__position-row'):

            header = job.css('h4 a::text').extract_first()
            ala = 'Tech'
            company = 'Siili Solutions'
            url = "https://siili.com" + \
                job.css('a.c-careers__link::attr(href)').extract_first()

            request = scrapy.Request(url, callback=self.parse_following_page)
            request.cb_kwargs['header'] = header
            request.cb_kwargs['ala'] = ala
            request.cb_kwargs['company'] = company
            request.cb_kwargs['url'] = url
            yield request

    def parse_following_page(self, response, header, ala, company, url):
        header = header
        ala = ala
        company = company
        url = url
        textAll = response.css('div.span6.c-careers__content p::text').getall()
        text_trimmed = ' '.join([str(text)for text in textAll])

        new = Post(header=header, ala=ala, company=company,
                   text=text_trimmed, url=url)           
        jobPosts.append(new)
        




##############################

def execute_crawling():
    process = CrawlerProcess()#same way can be done for Crawlrunner
    process.crawl(SiiliSpider)
    #process.crawl(JobsReaktor)
    process.start()

###########################
execute_crawling()
print(len(jobPosts))

#luodaan TimeToLive cache  maxsize pitää löytää sopiva koko ja aika on 1 58600päivä sekunteina

# @cached(cache= TTLCache(maxsize= 50000, ttl = 30))
# def job_info():
#     #saadaan jobPosts täyteen tavaraa
    
#     p = Process(target=execute_crawling)
#     p.start()
#     p.join()
    
#     #print('True')
#     return jobPosts




# start_time = time.time()
# print(job_info())
# time.sleep(30)
# print(jobPosts)
# eka_aika = time.time() - start_time
# start_time = time.time()
# print(job_info())
# toka_aika = time.time() - start_time
# time.sleep(31)
# start_time = time.time()
# print(job_info())
# kolmas_aika = time.time() - start_time


# print(jobPosts)




# print(eka_aika)
# print(toka_aika)
# print(kolmas_aika)
