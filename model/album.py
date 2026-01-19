from dataclasses import dataclass

@dataclass
class Album:
    album_id: int
    titolo: str
    minuti: float

    def __str__(self):
        return f"{self.titolo}"

    def __repr__(self):
        return f"{self.titolo}"

    def __hash__(self):
        return hash(self.album_id)

    def __eq__(self, other):
        return self.album_id == other.album_id

