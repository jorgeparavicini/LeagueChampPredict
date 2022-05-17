from dataclasses import dataclass


@dataclass(frozen=True, eq=True)
class Player:
    champion: str
    name: str
    tier: str
    region: str


@dataclass(frozen=True, eq=True)
class Summoner:
    name: str
    region: str
