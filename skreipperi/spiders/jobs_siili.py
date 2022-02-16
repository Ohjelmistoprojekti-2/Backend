import scrapy


class JobsSpider(scrapy.Spider):
    name = "siili"

    def start_requests(self):
        urls = [
            'https://www.siili.com/join-us',
        ]
        for url in urls:
            # haetaan "tagi" -a -flagin kanssa annetusta tags-attribuutista
            #tag = getattr(self, 'tag', None)

            # jos tagi on olemassa, lisätään se urliin
            # if tag is not None:
            #    url = url + '?haku=' + tag

            # parsetaan urlin sisältö
            yield scrapy.Request(url, self.parse)

    def parse(self, response):
        # loopataan jokainen työpaikkadiv
        for job in response.css('li.c-careers__position-row'):
            # jos työpaikkadivillä on jokin järkevä otsikko, huomioidaan työpaikka
            if job.css('h4 a::text').get() != None:
                # assignataan divin sisältöelementtejä nimettyihin kenttiin
                yield {
                    'header': job.css('h4 a::text').get(),
                    # 'company': job.css('span.employer::text').get(),
                    'company': 'Siili Solutions',
                    'url': job.css('a.c-careers__link::attr(href)').get(),
                }
