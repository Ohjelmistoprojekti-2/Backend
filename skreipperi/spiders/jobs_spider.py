import scrapy


class JobsSpider(scrapy.Spider):
    name = "jobs"

    def start_requests(self):
        urls = [
            'https://duunitori.fi/tyopaikat',
        ]
        for url in urls:
            tag = getattr(self, 'tag', None)
            if tag is not None:
                url = url + '?haku=' + tag
            yield scrapy.Request(url, self.parse)

    def parse(self, response):
        for job in response.css('div.job-box'):
            yield {
                'header': job.css('a.gtm-search-result::text').get(),
                'company': job.css('a.gtm-search-result::attr(data-company)').get(),
                'url':job.css('a.gtm-search-result::attr(href)').get(),
            }
