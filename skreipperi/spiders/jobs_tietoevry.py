import scrapy


class JobsSpider(scrapy.Spider):
    name = "tietoevry"

    def start_requests(self):
        # array haettavista osoitteista
        urls = [
            'https://tietoevry.com/en/careers/search-our-jobs/',
        ]
        for url in urls:
            # haetaan "tagi" -a -flagin kanssa annetusta tags-attribuutista
            #tag = getattr(self, 'tag', None)

            # jos tagi on olemassa, lisätään se urliin
            #if tag is not None:
                #url = url + '?haku=' + tag
            # parsetaan urlin sisältö
            yield scrapy.Request(url, self.parse)

    def parse(self, response):
        # kun urleja tulee myöhemmin lisää, tähän tarvii ehdon että onko kyseessä Duunitori
        # loopataan jokainen työpaikkadiv
        for job in response.css('a.jobResultRow'):
            # jos työpaikkadivillä on jokin järkevä otsikko, huomioidaan työpaikka
            if job.css('a.jobResultRow::text').get() != None:
                # assignataan divin sisältöelementtejä nimettyihin kenttiin
                yield {
                    'header': job.css('div:nth-child(1)::text').get(),
                    'company': 'Tietoevry',
                    'url':job.css('::attr(href)').get()
                }