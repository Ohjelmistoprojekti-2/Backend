import scrapy


class JobsReaktor(scrapy.Spider):
    name = "reaktor"

    def start_requests(self):
        # array haettavista osoitteista
        urls = [
            'https://www.reaktor.com/careers/#careers',
        ]
        for url in urls:
            # haetaan "tagi" -a -flagin kanssa annetusta tags-attribuutista
            #tag = getattr(self, 'tag', None)

            # jos tagi on olemassa, lisätään se urliin
            #if tag is not None:
            #    url = url + '?haku=' + tag

            # parsetaan urlin sisältö
            yield scrapy.Request(url, self.parse)

    def parse(self, response):
        # loopataan jokainen työpaikkadiv
        for job in response.css('a.filter-career-post'):
            # jos työpaikkadivillä on jokin järkevä otsikko, huomioidaan työpaikka
            if job.css('div h2::text').get() != None:
                # assignataan divin sisältöelementtejä nimettyihin kenttiin
                yield {
                    'header': job.css('div h2::text').get(),
                    'company': 'Reaktor',
                    'url':job.css('::attr(href)').get(),
                }
