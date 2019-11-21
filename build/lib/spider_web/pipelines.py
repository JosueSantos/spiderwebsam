# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

#import pymongo
import json

from scrapy.exceptions import DropItem
from scrapy.exporters import CsvItemExporter

from spider_web.items import GloboProgramacaoItem
from spider_web.items import FutbolItem
from spider_web.items import MateriaItem

class SpiderWebPipeline(object):
	def __init__(self):
		connection = pymongo.MongoClient(
			host="localhost",
			port=27017
		)
		self.db = connection.pymongo_test
		self.collection = self.db.spider

	def process_item(self, item, spider):
		valid = True
		for data in item:
			if not data:
				valid = False
				raise DropItem("Missing {0}!".format(data))

		if valid:
			if isinstance(item, GloboProgramacaoItem):
				self.collection = self.db.programacao_globo
				self.collection.update(
					{
						'id_section' : item['id_section']
					},
					{"$set":dict(item)}, True
				)
			if isinstance(item, FutbolItem):
				self.collection = self.db.placar_futebol
				self.collection.update(
					{
						'$and': [
							{'league' : item['league']},
							{'date' : item['date']},
							{'match_group' : item['match_group']},
							{'team_right' : item['team_right']},
							{'team_left' : item['team_left']}
						]
					},
					{"$set":dict(item)}, True
				)
			if isinstance(item, MateriaItem):
				self.collection = self.db.materia_dn
				self.collection.update(
					{
						'id_dn': item['id_dn']
					},
					{"$set":dict(item)}, True
				)

		return item

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