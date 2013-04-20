# encoding=UTF-8
'''
Created on 2013-4-20
@author: Administrator
'''
from scrapy.http.request import Request
from scrapy.http.request.form import FormRequest
from scrapy.spider import BaseSpider
from selenium import webdriver
import time
from fost.tools import FOSTConst

class FOSTSpider(BaseSpider):
    '''
    5173 spider
    '''
    name = u'FOSTSpider'
    home_page = u"http://www.5173.com/"


class FOST_Login_Spider(FOSTSpider):
    
    url = u"https://passport.5173.com/?returnUrl=http://www.5173.com"
    
    def __init__(self):
        FOSTSpider.__init__(self)
        self.selenium = webdriver.Firefox()
    
    def parse(self, response):

        cookies = response.request.cookies
        sel = self.selenium
        sel.get(response.url)
        
        time.sleep(10)
#        print sel.session_id, sel.get_cookies()
        
        cookies = {}
        
        for c in sel.get_cookies():
            cookies.update(c)
        else:
            cookies.update(response.request.cookies)
        
        return Request(cookies[FOSTConst.list_url],
                       cookies[u'spider']().parse,
                       cookies=cookies,)
        
        
#        yield Request(u"http://user.5173.com/default.aspx", cookies[u'spider']().parse,
#                      cookies=sel.get_cookies(),
#                      headers=sel.get
#                      )


class FOST_Login_QQ_Spider(FOSTSpider):
    
    url = u"https://passport.5173.com/Partner/LoginFrom?appNo=qq&returnUrl=http%3a%2f%2fwww.5173.com"
    
    def parse(self, response):
        cookies = response.request.cookies
        name = u"535521469"
        pwd = u"Corleone1016@"
        return FormRequest.from_response(response, u"loginform",
                                         formdata={u"u":name, u"p":pwd},
                                         parse=FOST_Login_Spider().parse,
                                         cookies=cookies)
        
        
