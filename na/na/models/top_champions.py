from dataclasses import dataclass
from typing import List


@dataclass(frozen=True, eq=True)
class ChampionPoints:
    champion: str
    points: int


@dataclass(frozen=True, eq=True)
class TopChampions:
    summoner: str
    rank: str
    region: str
    champion: str
    top_champs: List[ChampionPoints]
