# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

import csv

'''
    数据库的操作，在piplines.py中。
        
'''
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Column, Integer, DateTime, Text,String
from sqlalchemy.orm import sessionmaker


Base = declarative_base()
'''
通常导入的模块中，应用程序通常只有一个实例。我们使用declarative_base()函数创建基类
现在我们有了一个“Base”，我们可以用它来定义任意数量的映射类去配置ORM，描述我们要处理的数据库表，定义自己的类，并映射到表中

*写完piplines中的MySQL后关联到settings.py ---- 见settings.py文件  ！！！！
    ITEM_PIPELINES = {
        'sina.pipelines.SinaPipeline': 300
    }
'''

# 定义MySQL表头
class Data(Base): #建表
    __tablename__ = 'data' #表名
    id = Column(Integer(), primary_key=True)
    times = Column(DateTime)
    title = Column(Text())
    desc = Column(Text())
    type = Column(Text())


class SinaPipeline:
    def __init__(self):
        # 初始化引擎、创建base的metadata、创建DBSession，这是default操作
        self.engine = create_engine('mysql+pymysql://root:1413@localhost:3306/sina', encoding='utf-8')
        Base.metadata.create_all(self.engine)
        self.DBSession = sessionmaker(bind=self.engine)

    def process_item(self, item, spider):
        new = Data()
        new.title = item['title']
        new.times = item['times']
        new.desc = item['desc']
        new.type = item['type']
        session = self.DBSession()
        session.add(new)  #添加数据，直接通过orm操作
        session.commit()  #上传数据

        return item


