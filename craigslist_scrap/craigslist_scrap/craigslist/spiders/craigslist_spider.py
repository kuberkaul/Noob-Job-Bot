from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from craigslist.items import CraigslistItem

class craigslist_spider(BaseSpider):
    name = "craigslist_unique"
    allowed_domains = ["craiglist.org"]
    start_urls = [
        "http://sfbay.craigslist.org/search/sof?zoomToPosting=&query=&srchType=A&addFour=part-time",
        "http://newyork.craigslist.org/search/sof?zoomToPosting=&query=&srchType=A&addThree=internship",
	"http://seattle.craigslist.org/search/sof?zoomToPosting=&query=&srchType=A&addFour=part-time"
    ]

	
    def parse(self, response):
       hxs = HtmlXPathSelector(response)
       sites = hxs.select("//span[@class='pl']")
       items = []
       for site in sites:
           item = CraigslistItem()
           item['title'] = site.select('a/text()').extract()
           item['link'] = site.select('a/@href').extract()
           #item['desc'] = site.select('text()').extract()
           items.append(item)
	   hxs = HtmlXPathSelector(response)
	   #print title, link        
       return items

