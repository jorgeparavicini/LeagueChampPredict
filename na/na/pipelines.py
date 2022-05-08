# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import networkx as nx
import json


class ChampionPipeline:

    def __init__(self):
        self.champions = []

    def process_item(self, item, spider):
        if 'champion_pipeline' not in getattr(spider, 'pipelines'):
            return item
        self.champions.append(item)

    def close_spider(self, spider):
        if 'champion_pipeline' not in getattr(spider, 'pipelines'):
            return

        g = nx.Graph()
        for champion in self.champions:
            g.add_node(champion.ch_name)

        for i, champion in enumerate(self.champions):
            for j, inner in enumerate(self.champions):
                if i >= j:
                    continue

                if champion.ch_name == inner.ch_name:
                    continue

                equal_positions = [i for i in champion.positions if i in inner.positions]
                equal_classes = [i for i in champion.ch_class if i in inner.ch_class]

                equal_attribute_count = 0

                if len(equal_classes) > 0:
                    equal_attribute_count += 1

                if champion.range == inner.range:
                    equal_attribute_count += 1

                if champion.mana == inner.mana:
                    equal_attribute_count += 1

                if champion.adaptive_type == inner.adaptive_type:
                    equal_attribute_count += 1

                if equal_attribute_count >= 3 \
                        and abs(champion.difficulty - inner.difficulty) <= 1 \
                        and len(equal_positions) > 0:
                    g.add_edge(champion.ch_name, inner.ch_name)

        nx.write_graphml(g, "hue.graphml")
        print(g)


class MasteryPipeline:

    def __init__(self):
        self.masteries = {}

    def process_item(self, item, spider):
        if 'mastery_pipeline' not in getattr(spider, 'pipelines'):
            return item

        if item.champion not in self.masteries:
            self.masteries[item.champion] = {'Iron': [], 'Bronze': [], 'Silver': [], 'Gold': [], 'Platinum': [],
                                             'Diamond': [], 'Master': [], 'GrandMaster': [], 'Challenger': []}

        self.masteries[item.champion][item.tier].append(item.name)

    def close_spider(self, spider):
        if 'mastery_pipeline' not in getattr(spider, 'pipelines'):
            return

        with open('champion_mastery.json', 'w') as file:
            json.dump(self.masteries, file)
