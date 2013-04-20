# encoding=UTF-8
'''
Created on 2013-4-20
@author: Administrator
'''
from fost.spiders import FOSTSpider, FOST_Login_Spider
from scrapy import log
from scrapy.http.request import Request
from scrapy.selector import HtmlXPathSelector
import decimal
from fost.zxy.qkyj.tools import QKYJConst
from scrapy.http.request.form import FormRequest

class ZXY_QKYJ_Spider(FOSTSpider):
    
    name = u'ZXY_QKYJ_Spider'
    
    def start_requests(self):
        
        list_url = self.settings[QKYJConst.qkyj_config].get(QKYJConst.list_url)
        price = self.settings[QKYJConst.qkyj_config].get(QKYJConst.qkyj_config_price)
        Tel = self.settings[QKYJConst.qkyj_config].get(QKYJConst.qkyj_config_tel)
        QQ = self.settings[QKYJConst.qkyj_config].get(QKYJConst.qkyj_config_QQ)
        Role = self.settings[QKYJConst.qkyj_config].get(QKYJConst.qkyj_config_Role)
        per_cost = self.settings[QKYJConst.qkyj_config].get(QKYJConst.qkyj_config_per_cost)
        
        cookies = {
                   QKYJConst.list_url:list_url,
                   u'spider':self.__class__,
                   QKYJConst.qkyj_config_price:price,
                   QKYJConst.qkyj_config_QQ:QQ,
                   QKYJConst.qkyj_config_tel:Tel,
                   QKYJConst.qkyj_config_Role:Role,
                   QKYJConst.qkyj_config_per_cost:per_cost,
                   }
        url = u'http://ui.ptlogin2.qq.com/cgi-bin/login?appid=716027609&style=12&s_url=https%3A%2F%2Fgraph.qq.com%2Foauth2.0%2Fauthorize%3Fwhich%3DLogin%26display%3Dpc%26response_type%3Dcode%26client_id%3D213333%26redirect_uri%3Dhttp%253a%252f%252fpassport.5173.com%252fPartner%252fSignIn%253fappNo%253dqq%26state%3D7277%26src%3D1&pt_feedback_link=http%3A%2F%2Fsupport.qq.com%2Fwrite.shtml%3Ffid%3D780%26SSTAG%3Dwww.5173.com.appid213333'
        yield Request(url, FOST_Login_Spider().parse, cookies=cookies)

    def parse(self, response):
        
        base_price = response.request.cookies[QKYJConst.qkyj_config_price]
        
        hxs = HtmlXPathSelector(response)
        cookies = response.request.cookies
        
        reserve_count = 0
        
        for div in hxs.select('//div[@class="sin_pdlbox"]'):
            price = div.select('ul[@class="pdlist_unitprice"]//li/text()').extract()[1]
            url = div.select('ul[@class="pdlist_delivery"]//a[@class="btnlink_o_s_small"]/@href').extract()[0]
            
            price_decimal = decimal.Decimal(price[:price.index(u'元')])
            
            if price_decimal <= decimal.Decimal(base_price):
                
                cookies = dict(cookies)
                cookies[QKYJConst.qkyj_config_per_cost] = price
                self.log(u"price %s %s" % (price, url), log.INFO)
                reserve_count = reserve_count + 1
                yield Request(url, ZXY_QKYJ_Detail_Spider().parse,
                              cookies=cookies,
                              dont_filter=True,
                              )
        else:
            if not reserve_count:
                self.log(u"no suit price ", log.INFO)
            yield Request(response.request.url,
                          self.parse,
                          dont_filter=True,
                          cookies=cookies,
                          )
            
class ZXY_QKYJ_List_Spider(FOSTSpider):
    pass

class ZXY_QKYJ_Detail_Spider(FOSTSpider):
    
    def parse(self, response):
        
        hxs = HtmlXPathSelector(response)
        
        cookies = response.request.cookies
        
        
        try:
            count = hxs.select(u'//select[@name="ddrQuantity"]/option/@value').extract()[-1]
        except Exception :
            count = 1
        
        formdata = {u'ddrQuantity':unicode(count), # 购买数量
                    u'txtReceivingRole':cookies[QKYJConst.qkyj_config_Role], # 收获角色
                    u'txtSureReceivingRole':cookies[QKYJConst.qkyj_config_Role], # 确认
                    u'txtPhone':cookies[QKYJConst.qkyj_config_tel], # 联系电话
                    u'txtQq':cookies[QKYJConst.qkyj_config_QQ], # QQ
                    }
        
        try:
            yield FormRequest.from_response(response, ZXY_QKYJ_Deal_Spider().parse,
                                            formdata=formdata,)
        except Exception as e:
            self.log(u'%s'%str(e),log.INFO)
            

class ZXY_QKYJ_Deal_Spider(FOSTSpider):
    
    def parse(self, response): pass
