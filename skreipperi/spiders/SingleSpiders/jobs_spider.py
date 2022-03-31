import scrapy


class JobsSpider(scrapy.Spider):
    name = "jobs"

    def start_requests(self):
        # array haettavista osoitteista
        urls = [
            'https://duunitori.fi/tyopaikat',
        ]
        for url in urls:
            # haetaan "tagi" -a -flagin kanssa annetusta tags-attribuutista
            tag = getattr(self, 'tag', None)

            # jos tagi on olemassa, lisätään se urliin
            if tag is not None:
                url = url + '?haku=' + tag
            # parsetaan urlin sisältö
            yield scrapy.Request(url, self.parse)

    def parse(self, response):
        # kun urleja tulee myöhemmin lisää, tähän tarvii ehdon että onko kyseessä Duunitori
        # loopataan jokainen työpaikkadiv
        for job in response.css('div.job-box'):
            # jos työpaikkadivillä on jokin järkevä otsikko, huomioidaan työpaikka
            if job.css('a.gtm-search-result::text').get() != None:
                # assignataan divin sisältöelementtejä nimettyihin kenttiin
                yield {
                    'header': job.css('a.gtm-search-result::text').get(),
                    'company': job.css('a.gtm-search-result::attr(data-company)').get(),
                    'url':job.css('a.gtm-search-result::attr(href)').get(),
                }
