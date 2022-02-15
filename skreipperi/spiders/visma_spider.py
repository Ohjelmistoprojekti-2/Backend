import scrapy


class JobsSpider(scrapy.Spider):
    name = "visma_jobs"
    start_urls = ['https://ats.talentadore.com/positions/rJ4tqSR/rss?v=2&language=en%2Cfi&tags=&notTags=Visma+Legal+avoin+hakemus&businessUnits=&notBusinessUnits=&display_description=job_description&categories=tags_and_extras']
    

    def parse(self, response):
        
        for job in response.xpath('//channel/item'):
            yield {
                'title' : job.xpath('title//text()').extract(),
                'link': job.xpath('link//text()').extract(),
                'company': job.xpath('dc.creator//text()').extract(),  ##palauttaa vielä tyhjän listan
            }
      