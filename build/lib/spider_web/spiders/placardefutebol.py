# -*- coding: utf-8 -*-

import scrapy

from spider_web.items import FutbolItem

class PlacarDeFutebolSpider(scrapy.Spider):
	name = 'placardefutebol'
	allowed_domains = ['placardefutebol.com.br']
	start_urls = [
		'https://www.placardefutebol.com.br/jogos-de-ontem',
		'https://www.placardefutebol.com.br/jogos-de-hoje',
		'https://www.placardefutebol.com.br/jogos-de-amanha',
	]

	def parse(self, response):
		for livescore in response.css("div#livescore"):
			for divContainer in livescore.css("div.container"):
				for container in divContainer.css("a"):
					link_league = container.attrib['href']

					if link_league:
						yield response.follow(link_league, self.parse_league_game)

	def parse_league_game(self, response):
		for livescore in response.css("div#livescore"):
			league = livescore.css("div div.league-name h3::text").extract_first()
			link_url = response.url.split('placardefutebol.com.br/')[1]

			if len(link_url.split('/')) > 1:

				date = link_url.split('/')[1].split('-')
				date = date[0]+"-"+date[1]+"-"+date[2]

				match_group = livescore.css("div.container div div.container p.match-group").xpath('.//text()').extract()
				match_group = ' - '.join(match_group)
				
				img_right = "https://www.placardefutebol.com.br/"+livescore.css("div.container div div img::attr(src)").extract()[0]
				img_title_right = livescore.css("div.container div div img::attr(title)").extract()[0]

				img_left = "https://www.placardefutebol.com.br/"+livescore.css("div.container div div img::attr(src)").extract()[1]
				img_title_left = livescore.css("div.container div div img::attr(title)").extract()[1]

				status = livescore.css("div.container div div.match-scoreboard span.status-name::text").extract_first()

				score_right = ''
				score_left = ''
				team_right = ''
				team_right_link = ''
				team_left = ''
				team_left_link = ''
				time_game = ''
				events_home_team = []
				events_away_team = []
				event_game = []
				count_game_event = 0;
				events_game_history = {}
				statistic = {}
				stadium = ''
				city = ''
				date_time = ''
				judge = ''
				address = ''

				team_right = livescore.css("div.container div div.match-card-second-row div a h4.team_link::text").extract()[0]
				team_right_link = livescore.css("div.container div div.match-card-second-row div a::attr(href)").extract()[0]

				team_left = livescore.css("div.container div div.match-card-second-row div a h4.team_link::text").extract()[1]
				team_left_link = livescore.css("div.container div div.match-card-second-row div a::attr(href)").extract()[1]

				if livescore.css("div.match-info p i~strong").extract_first():
					stadium = livescore.css("div.match-info p i~strong::text").extract_first()
					
					if livescore.css("div.match-info hr~p").xpath('//*[text()[contains(., "Cidade")]]/following-sibling::text()').extract_first():
						city = livescore.css("div.match-info hr~p").xpath('//*[text()[contains(., "Cidade")]]/following-sibling::text()').extract_first()
					
					if livescore.css("div.match-info hr~p").xpath('//*[text()[contains(., "Data")]]/following-sibling::text()').extract_first():
						date_time = livescore.css("div.match-info hr~p").xpath('//*[text()[contains(., "Data")]]/following-sibling::text()').extract_first()
					
					if livescore.css("div.match-info hr~p").xpath('//*[text()[contains(., "rbitro")]]/following-sibling::text()').extract_first():
						judge = livescore.css("div.match-info hr~p").xpath('//*[text()[contains(., "rbitro")]]/following-sibling::text()').extract_first()
					
					if livescore.css("div.match-info hr~p").xpath('//*[text()[contains(., "Endere")]]/following-sibling::text()').extract_first():
						address = livescore.css("div.match-info hr~p").xpath('//*[text()[contains(., "Endere")]]/following-sibling::text()').extract_first()

				if status.find("ONTE") == -1 and status.find("HOJ") == -1 and status.find("AMANH") == -1:

					score_right = livescore.css("div.container div div.match-scoreboard span.match-score-text::text").extract()[0]
					score_left = livescore.css("div.container div div.match-scoreboard span.match-score-text::text").extract()[1]

					events = livescore.css("div.container div.content div.w-25")
					
					for event in events:
						if event.css(".match-card-events-space strong").extract_first():
							time_game = event.css(".match-card-events-space strong::text").extract_first().strip()

						elif event.css(".match-card-events-space").extract_first():
							time_game = event.css(".match-card-events-space::text").extract_first().strip()

						elif event.css(".match-card-events-home-team").extract_first():
							if event.css(".match-card-events-home-team p").extract_first():
								events_home_team = event.css(".match-card-events-home-team p").xpath('.//text()').extract()

						elif event.css(".match-card-events-away-team").extract_first():
							if event.css(".match-card-events-away-team p").extract_first():
								events_away_team = event.css(".match-card-events-away-team p").xpath('.//text()').extract()
						
						if event.css("i.fa-futbol").extract_first():
							event_game.append("GOL")

						if event.css("i.own-goal").extract_first():
							event_game.append("CONTRA")

						if event.css("i.yellow-card").extract_first():
							event_game.append("CARTAO AMARELO")

						if event.css("i.red-card").extract_first():
							event_game.append("CARTAO VERMELHO")

						if event.css("i.substitution-in").extract_first():
							event_game.append("SUBSTITUICAO ENTRANDO")

						if event.css("i.substitution-out").extract_first():
							event_game.append("SUBSTITUICAO SAINDO")

						count_game_event += 1
						if count_game_event == 3:
							events_game_history[ time_game ] = {}
							events_game_history[ time_game ]['time_game'] = time_game
							events_game_history[ time_game ]['events_home_team'] = events_home_team
							events_game_history[ time_game ]['events_away_team'] = events_away_team
							events_game_history[ time_game ]['event_game'] = event_game
							
							time_game = ''
							events_home_team = []
							events_away_team = []
							event_game = []
							count_game_event = 0;

					if livescore.css("div.container table.standing-table tbody tr").extract():
						statistic['home_team'] = livescore.css("div.container table.standing-table thead tr th.stats-home-team::text").extract_first().strip()
						statistic['away_team'] = livescore.css("div.container table.standing-table thead tr th.stats-away-team::text").extract_first().strip()
						
						standing_table = livescore.css("div.container table.standing-table tbody tr")

						for tr in standing_table:
							if tr.css("td.stats-category small::text").extract_first():
								category = tr.css("td.stats-category small::text").extract_first()
								cat = category.strip().replace(" ", "_")
								statistic[cat] = {}

								statistic[cat]['category'] = tr.css("td.stats-category small::text").extract_first().strip()
								statistic[cat]['home'] = tr.css("td.stats-home-team small::text").extract_first().strip()
								statistic[cat]['away'] = tr.css("td.stats-away-team small::text").extract_first().strip()

				futbol_item = FutbolItem(
					league=league.strip(),
					date=date,
					match_group=match_group,
					img_right=img_right,
					img_title_right=img_title_right,
					img_left=img_left,
					img_title_left=img_title_left,
					status=status,
					team_right=team_right,
					score_right=score_right,
					team_left=team_left,
					score_left=score_left,
					events_game_history='',#events_game_history,
					statistic='',#statistic,
					stadium=stadium,
					city=city.strip(),
					judge=judge.strip(),
					address=address.strip(),
					date_time=date_time
				)
				
				yield futbol_item