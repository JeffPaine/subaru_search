import urlparse

from scrapy.spider import BaseSpider
from scrapy.selector import Selector
from scrapy.http import Request

from ..items import Car


class SubaruSpider(BaseSpider):
    name = 'subaru'

    # Enter the domain names here you have permission to retrieve data from
    # e.g. domains = ['http://www.example.com', 'http://www.example.com']
    domains = []

    def start_requests(self):
        # Add the model below you want to search for
        # e.g. models = ['Outback']
        models = []
        for domain in self.domains:
            for model in models:
                url = urlparse.urljoin(domain, 'used-inventory/index.htm?listingConfigId=auto-used&make=Subaru&model=%s' % model)
                yield Request(url)

    def parse(self, response):
        sel = Selector(response)

        # Extract any cars found
        cars = sel.xpath('//*[contains(@class, "inv-type-used")]')
        for c in cars:
            car = Car()

            # Title and year
            car['title'] = c.xpath('.//div/div/h1/a/text()').extract()[0].strip()
            car['year'] = car['title'][0:4]

            # Price, but remove non-number characters.
            # Examples: '$12,000', 'Please Call', etc.
            price = c.xpath('.//*[contains(@class, "value")]/text()').extract()[0]
            car['price'] = ''.join(d for d in price if d.isdigit())

            # No VIN
            try:
                car['vin'] = c.xpath('.//*/dt[text()="VIN:"]/following-sibling::dd/text()').extract()[0]
            except IndexError:
                car['vin'] = None

            # Some cars don't have the color listed
            try:
                car['color'] = c.xpath('.//*/dt[text()="Exterior Color:"]/following-sibling::dd/text()').extract()[0]
            except IndexError:
                car['color'] = None

            # Some cars don't have mileage listed
            try:
                car['miles'] = c.xpath('.//*/dt[text()="Mileage:"]/following-sibling::dd/text()').extract()[0]
            except IndexError:
                car['miles'] = None

            # Some cars don't have a transmission listed
            try:
                car['transmission'] = c.xpath('.//*/dt[text()="Transmission:"]/following-sibling::dd/text()').extract()[0]
            except IndexError:
                car['transmission'] = None

            # Construct url
            # url
            path = c.xpath('.//div/div/h1/a/@href').extract()[0]
            url = urlparse.urlparse(response.url)
            car['url'] = urlparse.urlunsplit([url.scheme, url.netloc, path, None, None])
            yield car

        # If there's a next page link, parse it for cars as well
        next_links = sel.xpath('//*[@rel="next"]/@href').extract()
        if len(next_links) > 0:
            query = next_links[0]
            url = urlparse.urlparse(response.url)
            base = urlparse.urlunsplit([url.scheme, url.netloc, url.path, None, None])
            next_url = urlparse.urljoin(base, query)
            # Construct url
            yield Request(next_url, callback=self.parse)
