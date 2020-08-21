'''
1. scrapy负责爬取数据，selenium负责向下滑动的动作
2
    code flow：
        (1)start_requests() --> parse() --> parse_namedetail()
        (2)通过scrapy crawl sina_spider 去开启蜘蛛
        (3)设置start_url
        (4)通过start_url一页一页的去拿，拿完后做请求，请求完后就callback parse，
        (5)通过parse()去打开浏览器，进行操作（上滑下滑、翻页、点击等）解析内容，点击后在parse_namedetail里爬取内部数据，最终拿到全部数据后，存到数据库

3. 写爬虫code的时候，可以先写爬虫主框架，再考虑数据库的内容
4.
'''



import scrapy
from scrapy.http import Request
from scrapy.selector import Selector
from selenium import webdriver
import re
import datetime
from items import DataItem





class SinaSpiderSpider(scrapy.Spider):
    name = 'sina_spider'
    # allowed_domains = ['sina.com.cn']   # 设定允许爬取的page domain ,一般可注释掉

    def __init__(self, page=None, flag=None, *args, **kwargs):
        super(SinaSpiderSpider, self).__init__(*args, **kwargs)  # 当需要继承父类构造函数中的内容，且子类需要在父类的基础上补充时，使用super().__init__()方法。
        self.page = int(page)   # 定义翻多少页，可以通过main.py 的command line传进来
        self.flag = int(flag)   # 定义标记，可以通过run.py 的command line传过来  想要的效果是0就是跑全量 1 跑增量
        self.start_urls = [
                            'https://ent.sina.com.cn/film/',
                            'https://ent.sina.com.cn/zongyi/',
                            'https://news.sina.com.cn/china/',
                        ]
        self.option = webdriver.ChromeOptions()  # 打开浏览器的动作，需要Chrome webdriver()的支持

        # 把option 添加各种各样的参数，让其特定功能化，让其效率提高
        self.option.add_argument('headless') #不显示浏览器
        self.option.add_argument('no-sandbox') #不显示页面
        self.option.add_argument('--blink-setting=imagesEnabled=false') #不显示图片

    def start_requests(self):
        for url in self.start_urls:
            yield Request(url=url, callback=self.parse)  #callback回调函数名, 回调的是self.parse

    def parse(self, response):
        """
        网址传进来的时候要进行解析，用parse函数
        """
        driver = webdriver.Chrome(chrome_options=self.option)  # 用于打开浏览器的窗口
        driver.set_page_load_timeout(30) # 等待时间,如果网页加载时间大于30秒，就停掉
        driver.get(response.url)  # 做请求设置：取得response的URL，让parse知道应该打开那个网页
        for i in range(self.page):  # 一页一页的去爬
            # 每一页开始找选择页码的元素，如果没有找到，则向下滑动鼠标滚轮
            while not driver.find_element_by_xpath("//div[@class = 'feed-card-page']").text:
                driver.execute_script("window.scrollTo(0,document.body.scrollHeight);") # 执行往下滑的动作，是selenium 自带的动作, 从0 一直滑到height 就是滑到底的意思
            title = driver.find_elements_by_xpath("//h2[@class = 'undefined']/a[@target = '_blank']") #找一页中的所有报道的标题，注意s
            time = driver.find_elements_by_xpath("//h2[@class = 'undefined']/../div[@class = 'feed-card-a feed-card-clearfix']/div[@class ='feed-card-time']")
            for j in range(len(title)):
                eachtitle = title[j].text
                eachtime = time[j].text
                item = DataItem()
                if response.url == "https://ent.sina.com.cn/zongyi/":
                    item['type'] = '综艺'
                elif response.url == 'https://news.sina.com.cn/china/':
                    item['type'] = '国内新闻'
                else:
                    item['type'] = '电影'


                item['title'] = eachtitle
                item['desc'] = ''
                href = title[j].get_attribute('href') # 获取m每一个标题的链接

                #对时间进行处理
                today = datetime.datetime.now()
                eachtime = eachtime.replace('今天', str(today.month) + '月' + str(today.day) + '日') #假如时间有今天的字段，就行替换
                if '分钟前' in eachtime:
                    minute = int(eachtime.split('分钟前')[0]) #获取分钟
                    t = datetime.datetime.now() - datetime.timedelta(minutes=minute)
                    t2 = datetime.datetime(year=t.year, month=t.month, day=t.day, hour=t.hour, minute=t.minute) #获得文章时间
                else:
                    if '年' not in eachtime: #时间标签没有带年份
                        eachtime = str(today.year) + '年' + eachtime
                        t1 = re.split('[年月日:]', eachtime)
                        t2 = datetime.datetime(year=int(t1[0]), month=int(t1[1]), day=int(t1[2]), hour=int(t1[3]), minute=int(t1[4]))

                item['times'] = t2

                # 判断时间试增量还是全量，就是是否是昨天的数据，是否要更新
                if self.flag == 1: # 增量
                    today = datetime.datetime.now().strftime('%Y-%m-%d')
                    yesterday = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime('%Y-%m-%d')
                    if item['times'].strftime('%Y-%m-%d') < yesterday:
                        driver.close() # 浏览器关闭
                        break
                    if yesterday <= item['times'].strftime('%Y-%m-%d') < today:
                        yield Request(url=response.urljoin(href), meta={'name': item}, callback=self.parse_namedetail)
                    return
                else:
                    # 向每个新闻的链接发起请求
                    yield Request(url=response.urljoin(href), meta={'name': item}, callback=self.parse_namedetail)

            try:
                #点击下一页
                driver.find_element_by_xpath("//div[@class ='feed-card-page']/span[@class='pagebox_next']/a").click()
            except:
                break

    def parse_namedetail(self, response):
        selector = Selector(response)
        #获取正文
        desc = selector.xpath("//div[@class='article']/p/text()").extract()
        item = response.meta['name']
        desc = list(map(str.strip, desc))
        item['desc'] = ''.join(desc)
        # print(item)
        yield item

