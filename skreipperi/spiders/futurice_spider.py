import scrapy


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
                yield {
                    'header': job.css('.focusOnHover::text').get(),
                    'ala': job.css('.css-zsp0rz::text').get(),
                    'company': "Futurice",
                    'url': "https://futurice.com/"+job.css('a::attr(href)').get(),
                }
