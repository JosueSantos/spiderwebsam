# -*- coding: utf-8 -*-

import scrapy

from spider_web.items import MateriaItem

class DiarioNordesteSpider(scrapy.Spider):
	name = 'diario_nordeste'
	allowed_domains = ['diariodonordeste.verdesmares.com.br']
	start_urls = [
		'https://diariodonordeste.verdesmares.com.br/editorias/negocios/online/bc-e-febraban-assinam-acordo-para-mutirao-de-renegociacao-de-dividas-1.2177536',
	]

	def __init__(self, *args, **kwargs):
		try:
			urls = open('urls.csv').readlines()

			for i in range(len(urls)):
				if i != 0:
					url = str(urls[i].strip())
					if( len(url) > 10 ):
						self.start_urls.append(url)

		except FileNotFoundError:
			print('File does not exist')

		self.logger.info(self.start_urls)
		super(DiarioNordesteSpider, self).__init__(*args, **kwargs)

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