import scrapy
from scrapy.http import TextResponse
import requests
import re

def henlo():
    print('x')

class runner1Spider(scrapy.Spider):
    name = "runner1"

    def start_requests(self):              
        #? Real Jobs
        SQL_RemoteCanada_24hrs ='https://ca.linkedin.com/jobs/search?keywords=SQL&location=Canada&locationId=&geoId=101174742&f_TPR=r86400&f_WT=2&position=1&pageNum=0'
        SQL_Toronto_24hrs = 'https://ca.linkedin.com/jobs/search?keywords=SQL&location=Toronto%2C%20Ontario%2C%20Canada&locationId=&geoId=100761630&f_TPR=r86400&distance=25&position=1&pageNum=0'
        Python_RemoteCanada_24hrs = 'https://ca.linkedin.com/jobs/search?keywords=Python&location=Canada&locationId=&geoId=101174742&f_TPR=r86400&f_WT=2&position=1&pageNum=0'
        Python_Toronto_24hrs = 'https://ca.linkedin.com/jobs/search?keywords=Python&location=Toronto%2C%20Ontario%2C%20Canada&locationId=&geoId=100025096&f_TPR=r86400&position=1&pageNum=0'
        Econ_RemoteCanada_24hrs = 'https://ca.linkedin.com/jobs/search?keywords=Economics&location=Canada&locationId=&geoId=101174742&f_TPR=&f_WT=2&position=1&pageNum=0'
        Econ_Toronto_24hrs ='https://ca.linkedin.com/jobs/search?keywords=Economics&location=Toronto%2C%20Ontario%2C%20Canada&locationId=&geoId=100025096&f_TPR=r86400&position=1&pageNum=0'
        SQL_RemoteUS_24hrs = 'https://ca.linkedin.com/jobs/search?keywords=Sql&location=United%20States&locationId=&geoId=103644278&f_TPR=r86400&f_WT=2&f_E=2&position=1&pageNum=0'
        
        #? Any Jobs
        #'support','associate','specialist'
        Entry_RemoteCanada_24hrs = 'https://ca.linkedin.com/jobs/search?keywords=&location=Canada&locationId=&geoId=101174742&f_TPR=r86400&f_E=2&f_WT=2&position=1&pageNum=0'
        Any_Any_RemoteCanada_24hrs = 'https://ca.linkedin.com/jobs/search?keywords=&location=Canada&locationId=&geoId=101174742&f_TPR=r86400&f_WT=2&position=1&pageNum=0'
        _Any_Entry_AnyToronto_24hrs = 'x'
        Any_Any_AnyToronto_24hrs = 'https://ca.linkedin.com/jobs/search?keywords=&location=Toronto%2C%20Ontario%2C%20Canada&locationId=&geoId=100025096&f_TPR=r86400&position=1&pageNum=0'

        #TODO : 
        #? Scraper Stuff:
        #? add no.ofApps, and timePosted to the results/json
        """ #? improve consistency, check error.log in spiders folder for 
        the last real (i.e., not test) run """        
        
        #? Figure out how to analyse this in jupyter notebooks
        #? common key-words
        #? filter by less apps to more apps
        #? do analysis dashboards like the ones the fiver guys had
        feederURLs = [SQL_RemoteCanada_24hrs,SQL_Toronto_24hrs,
                      Python_RemoteCanada_24hrs,Python_Toronto_24hrs,
                      Econ_RemoteCanada_24hrs,Econ_Toronto_24hrs,
                      SQL_RemoteUS_24hrs]
                    
        for feederURL in feederURLs: 

            totalJobs = int(TextResponse(body=requests.get(feederURL)\
                .content, url=feederURL)\
                .css('span.results-context-header__new-jobs::text')\
                .get().strip().replace("\xa0new",'').replace("(","")\
                .replace(',','').replace(')',''))

            """if there are 402 jobs, the page will load if you pass '400' 
            as the parameter, but not '425'. However, it loads if you put '402',
            so this way you can get the last few jobs. You can put a second 
            for loop just for those last few, but you may need another parse func 
            for that."""
            
            #totalJobs = 100
            for i in range(0, totalJobs, 25):
                yield scrapy.Request(url=feederURL.replace("/jobs/",
                                        "/jobs-guest/jobs/api/seeMoreJobPostings/") 
                                        + "&start={}".format(i),
                                    callback=self.after_fetch)
            # remove to loop over feederURLs
            #break
        

    def after_fetch(self, response):
        job_link = response.css('a.base-card__full-link::attr(href)').extract()

        for link in job_link:
            yield response.follow(url=link,
                                  callback=self.parse) 

    def parse(self, response, **kwargs):
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
        
        if postedTimeAgo <= 1:            
            noApplicants = response.css('.num-applicants__caption::text').get()\
                .strip().lower()
            if 'among' in noApplicants:
                noApplicants = 0
            else:
                noApplicants = int(noApplicants.replace("applicants",'')\
                    .replace("over",''))   
                
            appsPerHr = noApplicants/postedTimeAgo
            clean_desc = " ".join(response\
                .css('div.show-more-less-html__markup ::text')\
                .extract()).strip().lower()  
            clean_title = response.css('h1.topcard__title::text').get().strip()\
                .lower()
            clean_company = response.css('a.topcard__org-name-link::text').get()\
                .strip().lower()
            clean_type_of_job = response\
                .css('span.description__job-criteria-text::text').get().strip()\
                .lower()
            job_link = response.request.url
            job_id = int(re.findall("\d{10}",job_link)[0])
            
            yield {'title': clean_title, 'appsPerHour': appsPerHr, #'dateTime': self.dateTime,
                'noApplicants': noApplicants,'postedTimeAgo':postedTimeAgo,
                    'company': clean_company,'job_link': job_link,
                    'description': clean_desc, 'typeOfJob': clean_type_of_job,
                    'job_id': job_id
                    }