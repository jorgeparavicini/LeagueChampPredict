from dataclasses import dataclass


@dataclass(frozen=True, eq=True)
class Champion:
    ch_name: str
    ch_class: list
    range: str
    positions: list
    mana: str
    adaptive_type: str
    difficulty: int
