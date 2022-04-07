from xml.etree.ElementTree import tostring
import scrapy
import os
from scrapy.crawler import CrawlerProcess
import json
from json import JSONEncoder
import firebase_admin
from firebase_admin import db
from firebase_admin import credentials
from dotenv import load_dotenv
from datetime import datetime
import pytz

load_dotenv()

private_key_id = os.getenv('private_key_id')
private_key = os.getenv('private_key')
client_email = os.getenv('client_email')
client_id = os.getenv('client_id')

testidict = {
    "type": "service_account",
    "project_id": "ohjelmistoprojekti2",
    "private_key_id": private_key_id,
    "private_key": json.loads(private_key), 
    "client_email": client_email,
    "client_id": client_id,
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-9h6ca%40ohjelmistoprojekti2.iam.gserviceaccount.com"
}

jobPosts = []

cred = credentials.Certificate(testidict)

firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://ohjelmistoprojekti2-default-rtdb.europe-west1.firebasedatabase.app/'
})

ref = db.reference("/tyopaikat")
time_ref = db.reference("/time")

#luodaan timezone helsingille
HKI = pytz.timezone('Europe/Helsinki')


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
            if(job.css('.css-1rwq02b.e1vztrv40::text').get() == "Tech" or job.css('.css-1rwq02b.e1vztrv40::text').get() == "Cloud"): 
                if(job.css('.css-tv0ozi.e1vztrv40::text').get() == "Helsinki" or job.css('.css-tv0ozi.e1vztrv40::text').get() == "Tampere"):
                    header = job.css('.focusOnHover::text').get()
                    ala = job.css('.css-1rwq02b.e1vztrv40::text').get()
                    location = job.css('.css-tv0ozi.e1vztrv40::text').get()
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
        text = response.css('div.css-b4zh0n.e1rcc2lx2  p::text').getall()   ##palauttaa listan

        new = Post(header=header, ala=ala, location=location, company=company, text=text, url=url)  
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
                sijaintilistaus = job.css(
                    'div.f-paragraph-small.gray.flex.flex-wrap.items-center span::text').getall()
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

    def parse_following_page_Reaktor(self, response, header, ala, location, company, url):

        header = header
        ala = ala
        location = location
        company = company
        url = url
        text = response.css(
            'div.col.col6-ns.col12.offset1-l.blog-copy  span::text').getall()
        textAll = text + \
            response.css(
                'div.col.col6-ns.col12.offset1-l.blog-copy  p::text').getall()
        text_trimmed = ' '.join([str(text)for text in textAll])

        new = Post(header=header, ala=ala, location=location, company=company,
                   text=text_trimmed, url=url)
        jobPosts.append(new)


class VismaSpider(scrapy.Spider):
    name = "visma_jobs"
    start_urls = ['https://ats.talentadore.com/positions/rJ4tqSR/rss?v=2&language=en%2Cfi&tags=&notTags=Visma+Legal+avoin+hakemus&businessUnits=&notBusinessUnits=&display_description=job_description&categories=tags_and_extras']

    def parse(self, response):
        for job in response.xpath('//channel/item'):

            header = job.xpath('title//text()').extract_first()
            ala = job.xpath(
                'category[@domain="job_area"]//text()').extract_first()
            location = job.xpath('category[@domain="city"]//text()').extract()
            company = 'Visma'
            url = job.xpath('link//text()').extract_first()

            request = scrapy.Request(url, callback=self.parse_following_page)
            request.cb_kwargs['header'] = header
            request.cb_kwargs['location'] = location
            request.cb_kwargs['ala'] = ala
            request.cb_kwargs['company'] = company
            request.cb_kwargs['url'] = url
            yield request

    def parse_following_page(self, response, header, ala, location, company, url):

        header = header
        ala = ala
        location = location
        company = company
        url = url
        textlist = response.css(
            'div.job-ad-feature-description  p').getall()  # palauttaa listan
        text_untrimmed = ' '.join([str(text)for text in textlist])
        text_untrimmed = text_untrimmed.replace('<p>', '')
        text = text_untrimmed.replace('</p>', '')

        new = Post(header=header, ala=ala, location=location,
                   company=company, text=text, url=url)
        jobPosts.append(new)


class SiiliSpider(scrapy.Spider):
    name = "siili"
    start_urls = ['https://www.siili.com/join-us']

    def parse(self, response):
        for job in response.css('li.c-careers__position-row'):

            header = job.css('h4 a::text').extract_first()
            ala = 'Tech'
            locationLong = job.css(
                'span.paragraph-3.siili__color--grey.c-careers-city::text').extract_first()
            location1 = locationLong.split(" /")[0]
            location = location1.split(", ")
            company = 'Siili Solutions'
            url = "https://siili.com" + \
                job.css('a.c-careers__link::attr(href)').extract_first()

            request = scrapy.Request(url, callback=self.parse_following_page)
            request.cb_kwargs['header'] = header
            request.cb_kwargs['ala'] = ala
            request.cb_kwargs['location'] = location
            request.cb_kwargs['company'] = company
            request.cb_kwargs['url'] = url
            yield request

    def parse_following_page(self, response, header, ala, location, company, url):
        header = header
        ala = ala
        location = location
        company = company
        url = url
        textAll = response.css('div.span6.c-careers__content p::text').getall()
        text_trimmed = ' '.join([str(text)for text in textAll])

        new = Post(header=header, ala=ala, location=location, company=company,
                   text=text_trimmed, url=url)
        jobPosts.append(new)


def execute_crawling():
    process = CrawlerProcess()
    process.crawl(SiiliSpider)
    process.crawl(VismaSpider)
    process.crawl(JobsReaktor)
    process.crawl(JobsSpider)
    process.start()
    

def crawl_timer():
    #crawlin kellotus
    crawl_time = datetime.now()
    ts= datetime.timestamp(crawl_time)
    timestamp = datetime.fromtimestamp(ts, tz=HKI)
    timestamp = timestamp.strftime("%m/%d/%Y, %H:%M:%S")
    crawl_time = crawl_time.strftime("%m/%d/%Y, %H:%M:%S")
    return ('Local time: '+crawl_time+' Helsinki time: '+ timestamp)

class JobEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__


def storeToFirebase():
    jsonData = json.dumps(jobPosts, indent=4, cls=JobEncoder)
    ref.set(jsonData)

    time = crawl_timer()
    time_ref.set(time)


execute_crawling()
storeToFirebase()
