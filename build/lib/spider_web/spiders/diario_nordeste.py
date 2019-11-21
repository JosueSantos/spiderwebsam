# -*- coding: utf-8 -*-

import scrapy

from spider_web.items import MateriaItem

class DiarioNordesteSpider(scrapy.Spider):
	name = 'diario_nordeste'
	allowed_domains = ['diariodonordeste.verdesmares.com.br']
	start_urls = [
		'https://diariodonordeste.verdesmares.com.br/editorias/seguranca/online/dois-sobreviventes-da-queda-do-edificio-andrea-recebem-alta-hospitalar-1.2171459',
		'https://diariodonordeste.verdesmares.com.br/editorias/negocios/online/como-pagar-ipva-atrasado-1.2044940',
		'https://diariodonordeste.verdesmares.com.br/editorias/verso/online/gloria-maria-tem-alta-hospitalar-apos-passar-por-cirurgia-de-emergencia-no-cerebro-1.2175716',
		'https://diariodonordeste.verdesmares.com.br/servicos/ultima-hora',
	]

	def parse(self, response):
		if response.css("h1.c-page-head__name a::text").extract_first() == 'Última Hora':
			for article in response.css("article.c-teaser"):
				link = article.css("main.c-teaser__inner div a::attr(href)").extract_first()
				yield response.follow(link, self.parseMateria)

			next_page = response.css("div.c-pagination__next a::attr(href)").extract_first()
			if next_page is not None:
				yield response.follow(next_page, self.parse)
		else:
			link = response.url
			yield response.follow(link, self.parseMateria)

	def parseMateria(self, response):
		link = response.url
		editoria = response.css("div.c-menu__item--active a::text").extract_first()
		titulo = response.css("h1.c-article__heading::text").extract_first()
		sub_titulo = response.css("h2.c-article__subheading::text").extract_first()
		autor = response.css("div.c-article__info span span::text").extract_first()
		time = response.css("time.c-article__date-created::text").extract_first().strip()
		tags = response.css("footer.c-article__footer div div.tags a::text").extract()

		link_rel = response.css("article.c-article div div div.c-article__main div.c-article-content p a::attr(href)").extract()
		link_rel_interno = response.css("article.c-article div div div.c-article__main div.c-article-content p a[href*='diariodonordeste.verdesmares']::attr(href)").extract()

		id_dn = link.split('-1.')[-1]
		date = time.split('/')[1].strip()
		time = time[0:5]

		materia = MateriaItem(
			link=link,
			editoria=editoria,
			titulo=titulo.strip(),
			sub_titulo=sub_titulo.strip(),
			autor=autor.strip(),
			time=time,
			date=date,
			link_rel=len(link_rel),
			link_rel_interno=len(link_rel_interno),
			id_dn=id_dn,
			tags=tags
		)

		yield materia