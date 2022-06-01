import scrapy
import json
from ..models.top_champions import ChampionPoints, TopChampions


class TopChampionsSpider(scrapy.Spider):
    name = "top_mastery"
    pipelines = "top_mastery-pipeline"
    max_champions = 10

    def start_requests(self):
        with open('champion_mastery.json', encoding='utf-8') as file:
            data = json.load(file)

        for champion, ranks in data.items():
            for rank, summoners in ranks.items():
                for summoner in summoners:
                    yield scrapy.Request(
                        f"https://championmastery.gg/summoner?summoner={summoner['name']}&region={summoner['region']}",
                        callback=self.parse,
                        meta={'champion': champion, 'rank': rank, 'summoner': summoner})

    def parse(self, response, **kwargs):
        champion_list = response.css("#tbody tr")
        champion_points = []
        for i, champion in enumerate(champion_list):
            if i == self.max_champions:
                break
            name = champion.css("td")[0].css("a::text").get().strip()
            points = champion.css("td")[2].css("::text").get().strip()
            points = int(points)
            champion_points.append(ChampionPoints(name, points))

        summoner = response.meta.get('summoner')['name']
        rank = response.meta.get('rank')
        champion = response.meta.get('champion')
        region = response.meta.get('summoner')['region']
        yield TopChampions(summoner, rank, region, champion, champion_points)
