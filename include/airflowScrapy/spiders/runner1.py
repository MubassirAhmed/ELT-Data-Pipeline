import scrapy
from scrapy.http import TextResponse
import requests
import re

def henlo():
    print('x')

class runner1Spider(scrapy.Spider):
    name = "runner1"

    def start_requests(self):              
        keywords = ["excel"]
        provinces = ['Nova Scotia', 'Manitoba','Saskatchewan', 'New Brunswick', 'Prince Edward Island', 'Newfoundland and Labrador', 'Ontario', 'Quebec', 'Alberta', 'British Columbia']
        #provinces = ['Prince%20Edward%20Island','Newfoundland%20and%20Labrador','New%20Brunswick','Saskatchewan']
        
        time = {'week' : 'r604800', 'month' : 'r2592000' }

        geoIds = ['104823201', '104423466', '104002611', '103790618',
                  '104663945', '106199678','105149290', '102237789', '103564821','102044150']

        for keyword in keywords:
            for index, province in enumerate(provinces):
                feederURL = 'https://www.linkedin.com/jobs/search?keywords={}&location={}%2C%20Canada&geoId={}&f_TPR={}&position=1&pageNum=0'.format(keyword.replace(" ","%20").replace("\"","%22"), province, geoIds[index], time["month"])
                
                totalJobs = int(TextResponse(body=requests.get(feederURL).content, url=feederURL).css('span.results-context-header__job-count::text').get().replace('+','').replace(',',''))

                #totalJobs = 25
                for i in range(0, totalJobs, 25):
                    yield scrapy.Request(url=feederURL.replace("/jobs/",
                                            "/jobs-guest/jobs/api/seeMoreJobPostings/") 
                                            + "&start={}".format(i),
                                        callback=self.after_fetch,
                                        meta={'province': province.replace("%20"," ")})


    def after_fetch(self, response):
        job_link = response.css('a.base-card__full-link::attr(href)').extract()

        for link in job_link:
            yield response.follow(url=link,
                                  meta={'province' : response.meta['province']},
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

        clean_city =  response.css('span.topcard__flavor.topcard__flavor--bullet::text').get().strip().lower().replace(',',"").split()[0]

        job_link = response.request.url
        clean_desc = " ".join(response.css('div.show-more-less-html__markup ::text').extract()).strip().lower()  
        job_id = clean_title + clean_company + clean_industry + clean_job_function
        

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
               'job_id': job_id,
               'city': clean_city,
               'province': response.meta['province'],
               'TimeScraped' : self.timestamp,
               'snow_col_timestamp' : self.snow_col_timestamp,
               'Hour' : self.Hour,
               'dayOfWeek' : self.dayOfWeek,
               'dayOfTheMonth' : self.dayOfTheMonth,
               'NameOfMonth' : self.NameOfMonth,
               'MonthNumber' : self.MonthNumber
                }
