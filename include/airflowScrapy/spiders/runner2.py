import scrapy
from scrapy.http import TextResponse
import re

#? TODO
#? Fix timeStamp passing
#? Fix job_links.txt location
class runner2Spider(scrapy.Spider):
    name = "runner2"

    def start_requests(self):
        with open('job_links.txt') as f:
            urls = [link.rstrip() for link in f]
            
        for url in urls:
            yield scrapy.Request(url=url.replace("('","").replace("',)",""), callback=self.parse)

    def parse(self, response):
        postedTimeAgo =  response.css('span.posted-time-ago__text::text')\
            .get().strip().lower()
        if any(word in postedTimeAgo for word in ['hour','hours']):
            postedTimeAgo = int(postedTimeAgo.replace("hours ago",'')\
            .replace("hour ago",'').strip())
        else:
            if any(word in postedTimeAgo for word in ['minutes','minute']):
                postedTimeAgo = int(postedTimeAgo.replace("minute ago",'')\
                .replace("minutes ago",'').strip())/60
            else: 
                if any(word in postedTimeAgo for word in ['day','days']):
                    postedTimeAgo = int(postedTimeAgo.replace("day ago",'')\
                    .replace("days ago",'').strip())*24
        noApplicants = response.css('.num-applicants__caption::text').get()\
            .strip().lower()
        if 'among' in noApplicants:
            noApplicants = 0
        else:
            noApplicants = int(noApplicants.replace("applicants",'')\
                .replace("over",''))   
        appsPerHr = noApplicants/postedTimeAgo
        job_id = int(re.findall("\d{10}",response.request.url)[0])
        
        #filename= ''
        #self.log(f'Saved file {filename}')
        
        yield { 'job_id': job_id,'noApplicants': noApplicants, 'TimeScraped':self.date_Time,
               'appsPerHour': appsPerHr, 
                }