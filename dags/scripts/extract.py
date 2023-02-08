import os
os.environ['SCRAPY_SETTINGS_MODULE']='include.airflowScrapy.settings'
import sys
sys.path.append('/usr/local/airflow/include')
from include.airflowScrapy.spiders.scraper import scraperSpider
from scrapy.crawler import CrawlerRunner
from datetime import datetime
from twisted.internet import reactor
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings
from scrapy.settings import Settings


def run1(s3Run1FileName, TimeScraped,
                snow_col_timestamp,
                Hour,
                dayOfWeek,
                dayOfTheMonth,
                NameOfMonth,
                MonthNumber):
    import os
    os.environ['SCRAPY_SETTINGS_MODULE']='include.airflowScrapy.settings'
    
    configure_logging()
    settings = get_project_settings()
    settings.update({  'FEEDS': {"s3://{}".format(s3Run1FileName): {"format": "csv"}}  })

    runner = CrawlerRunner(settings)
    d = runner.crawl(scraperSpider, 
                    timestamp = TimeScraped,
                    snow_col_timestamp=snow_col_timestamp,
                    Hour = Hour,
                    dayOfWeek = dayOfWeek,
                    dayOfTheMonth = dayOfTheMonth,
                    NameOfMonth = NameOfMonth,
                    MonthNumber = MonthNumber)

    d.addBoth(lambda _: reactor.stop())
    reactor.run()
    

# if __name__ == '__main__':
#     pass

    