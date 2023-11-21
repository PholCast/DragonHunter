from dataclasses import dataclass

@dataclass
class GameElement: # Character and GameItem
    name: str
    icon: str

    def __repr__(self):
        return self.icon
