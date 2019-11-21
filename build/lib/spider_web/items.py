# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class GloboProgramacaoItem(scrapy.Item):
	id_section = scrapy.Field()
	logo = scrapy.Field()
	horario = scrapy.Field()
	programa_do_dia = scrapy.Field()
	descricao = scrapy.Field()
	titulo_original = scrapy.Field()
	imagem_programa = scrapy.Field()
	ano = scrapy.Field()
	mes = scrapy.Field()
	dia = scrapy.Field()
	pragrama = scrapy.Field()
	titulo = scrapy.Field()

class FutbolItem(scrapy.Item):
	league = scrapy.Field()
	date = scrapy.Field()
	match_group = scrapy.Field()
	img_right = scrapy.Field()
	img_title_right = scrapy.Field()
	img_left = scrapy.Field()
	img_title_left = scrapy.Field()
	status = scrapy.Field()
	team_right = scrapy.Field()
	score_right = scrapy.Field()
	team_left = scrapy.Field()
	score_left = scrapy.Field()
	events_game_history = scrapy.Field()
	statistic = scrapy.Field()
	stadium = scrapy.Field()
	city = scrapy.Field()
	judge = scrapy.Field()
	address = scrapy.Field()
	date_time = scrapy.Field()

class MateriaItem(scrapy.Item):
	link = scrapy.Field()
	editoria = scrapy.Field()
	titulo = scrapy.Field()
	sub_titulo = scrapy.Field()
	autor = scrapy.Field()
	time = scrapy.Field()
	date = scrapy.Field()
	link_rel = scrapy.Field()
	link_rel_interno = scrapy.Field()
	id_dn = scrapy.Field()
	tags = scrapy.Field()