# encoding=UTF-8
'''
Created on 2013-4-20
@author: Administrator
'''
from robot.configutil import ConfigFile
from scrapy.cmdline import execute
from scrapy.settings import CrawlerSettings

if __name__ == '__main__':
    
    cfg_file = r'fetchqkyj.cfg'
    configdata = ConfigFile.readconfig(cfg_file).data
    import_modules = __import__('fost.zxy.qkyj.settings', globals={}
                                , locals={}, fromlist=['', ])
    values = dict(configdata)
    settings = CrawlerSettings(import_modules, values=values)
    execute(['scrapy', 'crawl', 'ZXY_QKYJ_Spider', ], settings=settings)

