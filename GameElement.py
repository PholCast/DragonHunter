from dataclasses import dataclass

@dataclass
class GameElement:
    name: str
    icon: str

    def __repr__(self):
        return self.icon
