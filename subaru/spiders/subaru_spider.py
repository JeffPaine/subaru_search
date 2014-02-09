import urlparse

from scrapy.spider import BaseSpider
from scrapy.selector import Selector
from scrapy.http import Request

from ..items import Car

# Add the model(s) below you want to search for
# e.g. MODELS = ['Outback']
MODELS = []
# Enter the domain name(s) here you have permission to retrieve data from
# e.g. DOMAINS = ['http://www.example.com', 'http://www.example.com']
DOMAINS = []


class SubaruSpider(BaseSpider):
    name = 'subaru'

    def start_requests(self):
        for domain in DOMAINS:
            for model in MODELS:
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

            # url
            path = c.xpath('.//div/div/h1/a/@href').extract()[0]
            url = urlparse.urlparse(response.url)
            car['url'] = urlparse.urlunsplit([url.scheme, url.netloc, path, None, None])

            # Certain specs are frequently missing, so we need to handle
            # them with try / except
            specs = [
                {
                    'name': 'vin',
                    'xpath': './/*/dt[text()="VIN:"]/following-sibling::dd/text()'
                },
                {
                    'name': 'color',
                    'xpath': './/*/dt[text()="Exterior Color:"]/following-sibling::dd/text()'
                },
                {
                    'name': 'miles',
                    'xpath': './/*/dt[text()="Mileage:"]/following-sibling::dd/text()'
                },
                {
                    'name': 'transmission',
                    'xpath': './/*/dt[text()="Transmission:"]/following-sibling::dd/text()'
                }
            ]

            for s in specs:
                try:
                    car[s['name']] = c.xpath(s['xpath']).extract()[0]
                except IndexError:
                    car[s['name']] = None

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
