import scrapy
from ..models.player import Player
import re


class MasterySpider(scrapy.Spider):
    name = "mastery"
    nr_pages = 50
    pipelines = ['mastery_pipeline']
    start_urls = [
        "https://leagueoflegends.fandom.com/wiki/List_of_champions"
    ]

    def parse(self, response, **kwargs):
        champion_list = response.css("tbody>tr>td .champion-icon")
        for champion in champion_list:
            champion_name = champion.css("span::attr(data-champion)").get().strip().lower()

            query_name = "".join(champion_name.split())
            query_name = "".join(re.split(r"[\'.]", query_name))

            if query_name == 'renataglasc':
                query_name = 'renata'
            if query_name == 'wukong':
                query_name = 'monkeyking'
            for i in range(1, MasterySpider.nr_pages + 1):
                url = f"https://www.leagueofgraphs.com/rankings/champion-masteries/{query_name}/page-{i}"
                yield scrapy.Request(url, callback=self.parse_champion_page, meta={'champion': champion_name})

    def parse_champion_page(self, response):
        player_list = response.css("table.summonerRankingsTable tr")[1:]
        for player in player_list:
            name = player.css(".name a::text").get()
            if not name:
                continue
            name = name.strip()
            tier = player.css(".hide-for-small-down::text").get().strip().split()[0]
            region = player.css("a.championBlock-bottom::text").get().strip()
            if tier == '-':
                continue
            yield Player(response.meta.get('champion'), name, tier, region)


