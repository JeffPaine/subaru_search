# Scrapy settings for subaru project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'subaru'

SPIDER_MODULES = ['subaru.spiders']
NEWSPIDER_MODULE = 'subaru.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'subaru (+http://www.yourdomain.com)'

ITEM_PIPELINES = {
    'subaru.pipelines.DuplicatesPipeline': 1
}
