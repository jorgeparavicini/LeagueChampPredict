from dataclasses import dataclass


@dataclass(frozen=True, eq=True)
class Player:
    champion: str
    name: str
    tier: str
