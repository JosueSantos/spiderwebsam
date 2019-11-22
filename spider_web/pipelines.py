# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import json

from scrapy.exceptions import DropItem
from scrapy.exporters import CsvItemExporter

from spider_web.items import GloboProgramacaoItem
from spider_web.items import FutbolItem
from spider_web.items import MateriaItem

class SpiderWebCSV(object):
	def __init__(self):
		self.file = open("dados.csv", 'wb')
		self.exporter = CsvItemExporter(self.file, encoding='utf-8')
		self.exporter.start_exporting()

	def process_item(self, item, spider):
		self.exporter.export_item(item)

		return item

	def close_spider(self, spider):
		self.exporter.finish_exporting()
		self.file.close()