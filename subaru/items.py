# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field


class Car(Item):
    title = Field()
    year = Field()
    price = Field()
    miles = Field()
    color = Field()
    transmission = Field()
    vin = Field()
    url = Field()
