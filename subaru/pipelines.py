from scrapy.exceptions import DropItem

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class DuplicatesPipeline(object):
    """Drop any cars with VINs we've already seen"""

    def __init__(self):
        self.vins_seen = set()

    def process_item(self, item, spider):
        if item['vin'] in self.vins_seen:
            raise DropItem('Dropping duplicate car with vin: %s' % item['vin'])
        else:
            self.vins_seen.add(item['vin'])
            return item
