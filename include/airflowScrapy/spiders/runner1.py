import scrapy
from scrapy.http import TextResponse
import requests
import re

def henlo():
    print('x')

class runner1Spider(scrapy.Spider):
    name = "runner1"

    def start_requests(self):              
        #past 24 hrs
        analyticsANDsql = 'https://www.linkedin.com/jobs/search/?currentJobId=3467060936&f_TPR=r86400&geoId=101174742&keywords=analytics%20and%20sql&location=Canada&refresh=true'

        analystAND_sqlORpython_ = 'https://www.linkedin.com/jobs/search?keywords=Analyst%20And%20%28sql%20Or%20Python%29&location=Canada&locationId=&geoId=101174742&sortBy=R&f_TPR=r86400&position=1&pageNum=0'

        #!Initial loading
        #past week

        #analystAND_sqlORpython
        canada_pastWeek = 'https://www.linkedin.com/jobs/search?keywords=Analyst%20And%20%28sql%20Or%20Python%29&location=Canada&locationId=&geoId=101174742&f_TPR=r604800&position=1&pageNum=0'
        
        #analytics_andSQL_notIntern 'analytics' returns wayy more results so I'm splitting it into provinces

        novaScotia_anyTime = 'https://www.linkedin.com/jobs/search?keywords=Analytics%20AND%20Sql&location=nova%20scotia&geoId=&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0'

        ontario_pastWeek = 'https://www.linkedin.com/jobs/search?keywords=Analytics%20AND%20Sql%20NOT%20Intern&location=Ontario%2C%20Canada&locationId=&geoId=105149290&sortBy=R&f_TPR=r604800&position=1&pageNum=0'

        alberta_anyTime = 'https://www.linkedin.com/jobs/search?keywords=Analytics%20AND%20Sql%20NOT%20Intern&location=Alberta&geoId=&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0'

        manitoba_anyTime = 'https://www.linkedin.com/jobs/search?keywords=Analytics%20AND%20Sql%20NOT%20Intern&location=Manitoba&geoId=&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0'

        saskatchewan_anyTime = 'https://www.linkedin.com/jobs/search?keywords=Analytics%20AND%20Sql%20NOT%20Intern&location=Saskatchewan&geoId=&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0'

        BC_anyTime = 'https://www.linkedin.com/jobs/search?keywords=Analytics%20AND%20Sql%20NOT%20Intern&location=British%20Columbia&geoId=&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0'

        Quebec_anyTime = 'https://www.linkedin.com/jobs/search?keywords=Analytics%20AND%20python%20NOT%20Intern&location=Quebec&geoId=&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0'


        #TODO : 
        #? Scraper Stuff:
        #? add no.ofApps, and timePosted to the results/json
        """ #? improve consistency, check error.log in spiders folder for 
        the last real (i.e., not test) run """        
        
        #? Figure out how to analyse this in jupyter notebooks
        #? common key-words
        #? filter by less apps to more apps
        #? do analysis dashboards like the ones the fiver guys had
        feederURLs = [alberta_anyTime,
                      manitoba_anyTime,]
                      # canada_pastWeek,novaScotia_anyTime,
                      # ontario_pastWeek,saskatchewan_anyTime,
                      # BC_anyTime,Quebec_anyTime]
                    
        for feederURL in feederURLs: 

            totalJobs = int(TextResponse(body=requests.get(feederURL).content, url=feederURL).css('span.results-context-header__job-count::text').get().replace('+','').replace(',',''))

            """if there are 402 jobs, the page will load if you pass '400' 
            as the parameter, but not '425'. However, it loads if you put '402',
            so this way you can get the last few jobs. You can put a second 
            for loop just for those last few, but you may need another parse func 
            for that."""
            
            # totalJobs = 600
            for i in range(0, totalJobs, 25):
                yield scrapy.Request(url=feederURL.replace("/jobs/",
                                        "/jobs-guest/jobs/api/seeMoreJobPostings/") 
                                        + "&start={}".format(i),
                                    callback=self.after_fetch)
            # remove to loop over feederURLs
            # break
        

    def after_fetch(self, response):
        job_link = response.css('a.base-card__full-link::attr(href)').extract()

        for link in job_link:
            yield response.follow(url=link,
                                  callback=self.parse) 

    def parse(self, response, **kwargs):
        postedTimeAgo =  response.css('span.posted-time-ago__text::text').get().strip().lower()
        if any(word in postedTimeAgo for word in ['hour','hours']):
            postedTimeAgo = int(postedTimeAgo.replace("hours ago",'').replace("hour ago",'').strip())
        else:
            if any(word in postedTimeAgo for word in ['minutes','minute']):
                postedTimeAgo = int(int(postedTimeAgo.replace("minute ago",'').replace("minutes ago",'').strip())/60)
            else: 
                if any(word in postedTimeAgo for word in ['day','days']):
                    postedTimeAgo = int(postedTimeAgo.replace("day ago",'').replace("days ago",'').strip())*24
                    
        noApplicants = response.css('.num-applicants__caption::text').get().strip().lower()
        if 'among' in noApplicants:
            noApplicants = 0
        else:
            noApplicants = int(noApplicants.replace("applicants",'').replace("over",''))   
            
        # appsPerHr = noApplicants/postedTimeAgo
        clean_title = response.css('h1.topcard__title::text').get().strip().lower()
        clean_company = response.css('a.topcard__org-name-link::text').get().strip().lower()
    
        jobMetaData = len(response.css('span.description__job-criteria-text::text').getall())
        if jobMetaData >= 1:
            clean_seniority_level = response.css('span.description__job-criteria-text::text').getall()[0].strip().lower()
        else:
            clean_seniority_level = 'n/a'
        if jobMetaData >= 2:
            clean_employment_type = response.css('span.description__job-criteria-text::text').getall()[1].strip().lower()
        else:
            clean_employment_type = 'n/a'

        if jobMetaData >= 3:
            clean_job_function = response.css('span.description__job-criteria-text::text').getall()[2].strip().lower()
        else:
            clean_job_function = 'n/a'

        if jobMetaData >= 4:
            clean_industry = response.css('span.description__job-criteria-text::text').getall()[3].strip().lower()
        else:
            clean_industry = 'n/a'

        job_link = response.request.url
        clean_desc = " ".join(response.css('div.show-more-less-html__markup ::text').extract()).strip().lower()  
        job_id = int(re.findall("\d{10}",job_link)[0])
        
        company_link = response.css('a.topcard__org-name-link::attr(href)').get().replace('?trk=public_jobs_topcard-org-name','/?originalSubdomain=ca')

        yield {'title': clean_title, 
               #'appsPerHour': appsPerHr,
               'noApplicants': noApplicants,
               'postedTimeAgo':postedTimeAgo,
               'company': clean_company,
               'job_link': job_link,
               'description': clean_desc,
               'seniorityLevel':clean_seniority_level,
               'employmentType':clean_employment_type,
               'jobFunction':clean_job_function,
               'industry':clean_industry,
               'job_id': job_id
                }