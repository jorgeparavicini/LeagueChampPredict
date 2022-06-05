import scrapy
import json
from ..models.top_champions import ChampionPoints, TopChampions
from faker import Faker

fake = Faker()


class TopChampionsSpider(scrapy.Spider):
    name = "top_mastery"
    pipelines = "top_mastery-pipeline"
    max_champions = 10
    max_champs_per_rank = 50

    def start_requests(self):
        with open('champion_mastery.json', encoding='utf-8') as file:
            data = json.load(file)

        with open('top_champion_mastery.json', encoding='utf-8') as file:
            read_champs = json.load(file)

        for champion, ranks in data.items():
            if champion in read_champs:
                continue

            for rank, summoners in ranks.items():

                for i, summoner in enumerate(summoners):
                    if i == self.max_champs_per_rank:
                        break
                    # Masterypoints.com
                    yield scrapy.FormRequest(f"https://masterypoints.com/modules/player_profile", method="POST",
                                             formdata={'name': summoner['name'], 'server': summoner['region']},
                                             meta={'champion': champion, 'rank': rank, 'summoner': summoner},
                                             callback=self.parse_mastery_points,
                                             headers={"User-Agent": fake.chrome()})

                    # Champion Mastery.gg
                    #yield scrapy.Request(
                    #    f"https://championmastery.gg/summoner?summoner={summoner['name']}&region={summoner['region']}",
                    #    callback=self.parse,
                    #    meta={'champion': champion, 'rank': rank, 'summoner': summoner},
                    #    headers={"User-Agent": fake.chrome()})

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

    def parse_mastery_points(self, response):
        json_response = response.json()
        selector = scrapy.selector.Selector(text=json_response['content'])
        champion_list = selector.css('tbody tr')

        champion_points = []
        for i, champion in enumerate(champion_list):
            if i == self.max_champions:
                break
            name = champion.css(".hidden-xs span.fw-semi-bold::text").get().strip()
            points = champion.css("span.text-bigger::text").get().strip()
            points = int(points.replace(",", ""))
            champion_points.append(ChampionPoints(name, points))

        summoner = response.meta.get('summoner')['name']
        rank = response.meta.get('rank')
        champion = response.meta.get('champion')
        region = response.meta.get('summoner')['region']
        yield TopChampions(summoner, rank, region, champion, champion_points)
