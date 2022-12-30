import os
os.environ['SCRAPY_SETTINGS_MODULE']='airflowScrapy.settings'
import sys
# #sys.path.insert(1,'~/astro/include/airflowScrapy')
sys.path.append('/usr/local/airflow/include')
#sys.path.append('/usr/local/airflow/include/airflowScrapy')
from airflowScrapy.spiders.runner1 import runner1Spider
from airflowScrapy.spiders.runner2 import runner2Spider
from scrapy.crawler import CrawlerRunner
from datetime import datetime
from twisted.internet import reactor
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings
from scrapy.settings import Settings


def not_main():
    return print('main() works inside here')

def run1(s3Run1FileName, TimeScraped,
                snow_col_timestamp,
                Hour,
                dayOfWeek,
                dayOfTheMonth,
                NameOfMonth,
                MonthNumber):
    import os
    os.environ['SCRAPY_SETTINGS_MODULE']='airflowScrapy.settings'
    
    configure_logging()
    settings = get_project_settings()
    settings.update({  'FEEDS': {"s3://{}".format(s3Run1FileName): {"format": "csv"}}  })

    runner = CrawlerRunner(settings)
    d = runner.crawl(runner1Spider, timestamp = TimeScraped,
                    snow_col_timestamp=snow_col_timestamp,
                    Hour = Hour,
                    dayOfWeek = dayOfWeek,
                    dayOfTheMonth = dayOfTheMonth,
                    NameOfMonth = NameOfMonth,
                    MonthNumber = MonthNumber)

    d.addBoth(lambda _: reactor.stop())
    reactor.run()
    
def run2(s3Run2FileName,TimeScraped):
    import os
    os.environ['SCRAPY_SETTINGS_MODULE']='airflowScrapy.settings'
    
    configure_logging()
    settings = get_project_settings()
    settings.update({  'FEEDS': {"s3://{}".format(s3Run2FileName): {"format": "csv"}}  })
    """settings.update({'LOG_ENABLED' : False})
    settings.update({'LOG_LEVEL' : 'DEBUG' })
    settings.update({'LOG_FILE' : 'logfile_%(time)s.log'})"""
    runner = CrawlerRunner(settings)
    d = runner.crawl(runner2Spider, timestamp = TimeScraped)
    d.addBoth(lambda _: reactor.stop())
    reactor.run()

if __name__ == '__main__':
    TimeScraped = datetime.now()
    s3FileName = TimeScraped.strftime('%Y-%m-%d_Time-%H-%M{}'.format('.csv'))
    print(s3FileName)
    run1('2022-12-22_Time-08-02.csv',TimeScraped)

    