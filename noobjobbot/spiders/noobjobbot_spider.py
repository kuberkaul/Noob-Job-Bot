from scrapy.spider import BaseSpider

class DmozSpider(BaseSpider):
    name = "craiglist"
    allowed_domains = ["www.craigslist.org"]
    start_urls = ["http://newyork.craigslist.org/sof/", "http://sfbay.craigslist.org/sfc/sof/" ]

    def parse(self, response):
        filename = response.url.split("/")[-2]
        open(filename, 'wb').write(response.body)
