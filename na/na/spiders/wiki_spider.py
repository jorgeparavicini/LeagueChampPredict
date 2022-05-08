import scrapy
from ..models.champion import Champion


class WikiSpider(scrapy.Spider):
    name = "wiki"
    start_urls = [
        "https://leagueoflegends.fandom.com/wiki/Champion_classes/Controller",
        "https://leagueoflegends.fandom.com/wiki/Fighter",
        "https://leagueoflegends.fandom.com/wiki/Mage",
        "https://leagueoflegends.fandom.com/wiki/Marksman",
        "https://leagueoflegends.fandom.com/wiki/Slayer",
        "https://leagueoflegends.fandom.com/wiki/Tank",
        "https://leagueoflegends.fandom.com/wiki/Specialist"
    ]

    def parse(self, response, **kwargs):
        ch_class = response.css("#firstHeading::text").get().strip()
        headers = response.css("h2 .mw-headline::text").getall()
        if headers[-1] == "References":
            del headers[-1]
        champion_lists = response.css(".columntemplate")
        count = len(champion_lists)
        for i in range(count):
            header = headers[i] if len(headers) > i else ""
            yield from self.get_champions(champion_lists[i], ch_class, header.strip())

    def get_champions(self, doc, ch_class, ch_subclass):
        for ch_doc in doc.css("li"):
            yield Champion(self.get_champion(ch_doc), ch_class, ch_subclass)

    def get_champion(self, doc):
        return doc.css("a::text")[0].get()
    
