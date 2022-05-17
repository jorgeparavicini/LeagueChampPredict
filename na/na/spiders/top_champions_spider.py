import scrapy

class TopChampionsSpider(scrapy.Spider):
    name = "top_mastery"
    pipelines = "top_mastery_pipeline"

    def start_requests(self):
        url = ""
        yield scrapy.Request(url, callback=self.parse_summoner)
