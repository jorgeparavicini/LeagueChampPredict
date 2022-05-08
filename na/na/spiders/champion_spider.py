import scrapy
from ..models.champion import Champion


class ChampionSpider(scrapy.Spider):
    name = "champion"
    start_urls = [
        "https://leagueoflegends.fandom.com/wiki/List_of_champions"
    ]
    pipelines = ['champion_pipeline']

    def parse(self, response, **kwargs):
        champion_list = response.css("tbody>tr>td .champion-icon")
        for champion in champion_list:
            champion_name = champion.css("span::attr(data-champion)").get().strip()
            url = f"https://leagueoflegends.fandom.com/wiki/{champion_name}/LoL"
            yield scrapy.Request(url, callback=self.parse_champion)

    def parse_champion(self, response):
        name = response.css("h2.pi-title span::text").get()
        classes = response.css("div[data-source='role'] span a:nth-child(2)::text").getall()
        ranged = response.css("div[data-source='rangetype'] span a:nth-child(2)::text").get()
        positions = response.css("div[data-source='position'] span a:nth-child(2)::text").getall()

        for i, pos in enumerate(positions):
            if pos == 'Mid':
                positions[i] = 'Middle'

        if name == 'Yone':
            positions = ['Middle']
        if name == 'Rell':
            positions = ['Support']
        if name == 'Seraphine':
            positions = ['Support']
        if name == 'Samira':
            positions = ['Bottom']

        mana = response.css("div[data-source='resource'] span a:nth-child(2)::text").get()
        adaptive_type = response.css("div[data-source='adaptivetype'] span a::text").get()
        difficulty = int(response.css("div[data-source='difficulty'] div>div::attr(title)").get()[-2])

        yield Champion(name, classes, ranged, positions, mana, adaptive_type, difficulty)

