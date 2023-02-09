# Scrapy settings for airflowScrapy project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'airflowScrapy'

SPIDER_MODULES = ['airflowScrapy.spiders']
NEWSPIDER_MODULE = 'airflowScrapy.spiders'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False


#LOG_ENABLED = False
#LOG_LEVEL = 'ERROR' # Levels: CRITICAL, ERROR, WARNING, INFO, DEBUG
#LOG_FILE = 'logfile_%(time)s.log'

# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 250

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 0
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}
RETRY_HTTP_CODES = [429]
# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html


DOWNLOADER_MIDDLEWARES = {
    'scrapy.downloadermiddlewares.retry.RetryMiddleware': None,
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
    'scrapy_fake_useragent.middleware.RandomUserAgentMiddleware': 400,
    'scrapy_fake_useragent.middleware.RetryUserAgentMiddleware': 401,
    'airflowScrapy.middlewares.TooManyRequestsRetryMiddleware': 543,
    'rotating_proxies.middlewares.RotatingProxyMiddleware': 610,
    'rotating_proxies.middlewares.BanDetectionMiddleware': 620,

}


FAKEUSERAGENT_PROVIDERS = [
    'scrapy_fake_useragent.providers.FakeUserAgentProvider',  # This is the first provider we'll try
    'scrapy_fake_useragent.providers.FakerProvider',  # If FakeUserAgentProvider fails, we'll use faker to generate a user-agent string for us
    'scrapy_fake_useragent.providers.FixedUserAgentProvider',  # Fall back to USER_AGENT value
]

# Fallback User_Agent
USER_AGENT = 'Mozilla/5.0 (iPad; CPU OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148'

ROTATING_PROXY_LIST_PATH = 'include/airflowScrapy/250proxiesWithAuth.txt'
ROTATING_PROXY_LIST = [
'45.224.255.126:9692',
'192.3.48.176:6169',
'154.85.100.80:5121',
'45.128.245.33:9044',
'186.179.7.188:8265',
'185.230.46.102:5751',
'45.127.248.127:5128',
'209.127.183.126:8224',
'141.98.135.130:7080',
'198.23.239.134:6540',
'64.137.95.130:6613',
'23.247.105.4:5068',
'185.101.169.112:6656',
'45.128.247.14:7515',
'5.183.34.106:6457',
'2.59.21.247:7777',
'104.144.3.253:6332',
'192.3.48.64:6057',
'45.154.56.161:7179',
'179.61.248.97:5188',
'193.23.245.97:8668',
'103.53.216.113:5197',
'134.73.188.42:5132',
'161.123.33.41:6064',
'216.74.118.200:6355',
'66.78.32.185:5235',
'193.8.94.208:9253',
'45.128.76.88:6089',
'192.186.176.144:8194',
'184.174.24.251:5261',
'198.23.128.2:5630',
'181.177.94.220:7794',
'104.148.5.211:6222',
'45.86.72.205:6352',
'170.244.93.194:7755',
'182.54.239.201:8218',
'45.140.13.166:9179',
'104.227.133.89:7151',
'144.168.143.57:7604',
'80.253.249.242:5285',
'45.192.138.108:6750',
'45.72.40.235:9329',
'154.95.36.80:6774',
'64.137.100.133:5188',
'23.236.182.205:7754',
'45.158.187.189:7198',
'64.137.94.224:6447',
'154.92.122.235:5305',
'23.250.83.161:6170',
'91.214.65.189:6036',
'216.173.111.59:6769',
'67.227.110.44:6602',
'185.230.47.78:6001',
'176.116.231.33:7375',
'185.230.46.215:5864',
'91.246.194.75:6588',
'185.102.50.164:7247',
'154.95.0.32:6285',
'107.152.230.223:9311',
'192.241.112.226:7728',
'157.52.174.37:6246',
'192.198.126.36:7079',
'161.123.33.136:6159',
'179.61.248.108:5199',
'157.52.145.214:5823',
'45.135.39.48:7128',
'161.123.5.2:5051',
'107.152.192.246:7301',
'198.46.161.217:5267',
'45.154.228.232:8256',
'104.224.90.131:6292',
'64.137.14.131:5797',
'161.123.214.134:6489',
'184.174.44.185:6611',
'107.175.119.186:6714',
'113.30.154.97:5774',
'198.46.241.150:6685',
'181.177.94.32:7606',
'23.250.83.47:6056',
'107.152.192.162:7217',
'156.238.7.184:6196',
'185.245.26.204:6721',
'192.186.176.49:8099',
'84.21.188.167:8701',
'107.152.230.216:9304',
'157.52.145.233:5842',
'45.192.150.124:6307',
'104.227.223.41:8128',
'193.8.94.6:9051',
'154.30.250.183:5224',
'184.174.28.55:5070',
'45.153.216.9:8066',
'185.242.95.191:6532',
'154.95.32.83:5136',
'45.224.229.182:9247',
'182.54.239.22:8039',
'184.174.28.50:5065',
'185.102.50.212:7295',
'192.198.126.243:7286',
'67.227.110.242:6800',
'64.137.73.83:5171',
'45.72.36.186:7196',
'107.181.154.59:5737',
'45.134.184.178:6214',
'154.92.114.181:5876',
'154.92.126.17:5355',
'198.23.128.145:5773',
'45.192.138.119:6761',
'64.43.89.56:6315',
'64.137.77.152:5587',
'193.27.19.229:7315',
'45.114.12.35:5103',
'64.43.90.104:6619',
'104.168.25.74:5756',
'45.152.208.214:8245',
'132.255.132.229:7752',
'45.12.144.143:7146',
'64.43.89.193:6452',
'191.102.158.152:8216',
'5.181.43.190:7252',
'2.59.21.38:7568',
'37.35.41.73:8419',
'186.179.23.99:5143',
'45.146.130.218:5895',
'192.241.112.119:7621',
'45.86.247.238:7306',
'45.140.13.159:9172',
'113.30.155.89:6097',
'185.230.47.169:6092',
'104.144.3.95:6174',
'141.98.161.97:7794',
'45.12.115.120:6243',
'161.123.93.86:5816',
'45.192.138.13:6655',
'134.73.188.113:5203',
'144.168.241.104:8698',
'107.181.154.91:5769',
'23.236.247.178:8210',
'45.224.255.229:9795',
'156.238.7.88:6100',
'157.52.145.184:5793',
'45.152.196.134:9167',
'64.137.89.76:6149',
'80.253.249.51:5094',
'104.148.0.97:5452',
'45.147.28.193:9251',
'64.43.90.12:6527',
'185.102.48.115:6197',
'23.229.109.19:6045',
'45.8.134.178:7194',
'45.131.213.193:7741',
'45.224.229.68:9133',
'107.152.146.151:8669',
'104.223.157.226:6465',
'104.148.5.62:6073',
'154.92.121.134:5153',
'192.241.112.80:7582',
'104.227.101.178:6239',
'186.179.29.125:5439',
'156.238.7.251:6263',
'157.52.174.229:6438',
'5.252.140.101:6196',
'198.46.246.58:6682',
'104.227.13.14:8573',
'45.137.60.194:6722',
'173.211.0.188:6681',
'170.244.93.206:7767',
'37.35.40.112:8202',
'45.43.65.8:6522',
'104.224.90.41:6202',
'192.241.112.88:7590',
'193.8.127.44:9126',
'45.87.249.232:7810',
'104.144.34.211:7795',
'45.94.47.240:8284',
'45.154.228.51:8075',
'182.54.239.2:8019',
'23.229.109.81:6107',
'45.192.140.200:6790',
'2.59.148.47:5093',
'107.152.197.252:8274',
'64.137.77.189:5624',
'45.128.77.170:6456',
'37.35.42.181:8783',
'179.60.178.171:9198',
'84.21.189.111:5758',
'185.230.46.124:5773',
'216.74.118.30:6185',
'194.35.122.211:5102',
'45.72.95.179:8217',
'45.152.196.185:9218',
'103.53.219.217:6310',
'157.52.252.58:6622',
'161.123.115.203:5224',
'45.152.208.157:8188',
'104.144.51.198:7729',
'104.227.100.76:8157',
'113.30.154.34:5711',
'144.168.143.146:7693',
'154.92.126.62:5400',
'154.92.126.118:5456',
'185.99.96.39:8554',
'104.227.100.105:8186',
'194.33.61.246:8829',
'45.224.229.19:9084',
'185.126.65.109:6894',
'104.144.3.57:6136',
'154.95.36.203:6897',
'164.163.127.74:7137',
'64.137.100.230:5285',
'192.153.171.172:6245',
'23.247.105.107:5171',
'95.214.248.155:7267',
'45.224.255.101:9667',
'185.102.49.200:6538',
'107.181.128.225:5237',
'107.181.130.69:5690',
'154.92.114.42:5737',
'107.181.128.38:5050',
'185.213.242.15:8479',
'113.30.152.205:5263',
'104.223.223.163:6748',
'156.238.5.169:5510',
'104.223.223.5:6590',
'161.123.93.138:5868',
'104.148.5.216:6227',
'161.0.70.42:5631',
'198.105.108.220:6242',
'185.242.95.26:6367',
'45.13.184.37:6598',
'45.86.244.231:6298',
'45.151.253.119:6284',
'64.43.91.82:6853',
'64.137.8.21:6703',
'191.102.158.109:8173',
'198.46.246.83:6707',
'185.242.95.42:6383',
'45.130.128.93:9110',
'45.127.250.124:5733',
'109.207.130.31:8038',
'184.174.44.4:6430',
'64.137.89.160:6233',
'161.0.24.240:6264',
'186.179.7.189:8266',
'104.227.133.23:7085',
'216.74.118.142:6297',
'45.152.196.20:9053',
'45.192.146.74:6085',
'161.123.151.228:6212',
'104.223.223.155:6740'    
] 


# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
#ITEM_PIPELINES = {
#    'airflowScrapy.pipelines.AirflowscrapyPipeline': 300,
#}
AWS_ACCESS_KEY_ID = 'AKIAYUJWZRTZXMMGGNFE'
AWS_SECRET_ACCESS_KEY = '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'

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
AUTOTHROTTLE_DEBUG = True

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
