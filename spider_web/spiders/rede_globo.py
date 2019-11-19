# -*- coding: utf-8 -*-

import scrapy

from spider_web.items import GloboProgramacaoItem


class ProgramacaoGloboSpider(scrapy.Spider):
	name = 'rede_globo'
	allowed_domains = ['redeglobo.globo.com']
	start_urls = ['https://redeglobo.globo.com/tvverdesmares/programacao/']

	def parse(self, response):
		for article in response.css("div.schedule-inner"):
			for section in response.css("section.schedule-item"):
				id_section = section.css("div div input.schedule-toggle::attr(id)").extract_first()
				logo = section.css("div div label header div.schedule-item-header-logo img::attr(src)").extract_first()
				horario = section.css("div div label header div.schedule-item-header-info p.schedule-item-header-time time::text").extract_first()
				programa_do_dia = section.css("div div label header div.schedule-item-header-info h2::text").extract_first()
				descricao = section.css("div div div.schedule-item-content div.schedule-item-content-unique div p::text").extract_first()
				titulo_original = section.css("div div div.schedule-item-content div.schedule-item-content-unique div dl dd::text").extract_first()
				imagem_programa = section.css("div div div.schedule-item-content div.schedule-item-content-unique div div img::attr(src)").extract_first()

				ano = id_section[0:4]
				mes = id_section[4:6]
				dia = id_section[6:8]

				prog = programa_do_dia.split('-')

				pragrama = prog[0].strip()
				titulo = ' '.join(prog[1:])

				programacao_blobo = GloboProgramacaoItem(
					id_section=id_section,
					logo=logo,
					horario=horario,
					programa_do_dia=programa_do_dia,
					descricao=descricao,
					titulo_original=titulo_original,
					imagem_programa=imagem_programa,
					ano=ano,
					mes=mes,
					dia=dia,
					pragrama=pragrama,
					titulo=titulo.strip(),
				)
				
				yield programacao_blobo