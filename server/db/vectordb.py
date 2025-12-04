from typing import Dict, List, Tuple
import random


class VectorDB:
    def __init__(self, dimensions: int = 384):
        self.dimensions = dimensions
        self.vectors: Dict[str, List[float]] = {}

    def upsert(self, key: str, vector: List[float]) -> str:
        self.vectors[key] = vector
        return key

    def _similarity(self, a: List[float], b: List[float]) -> float:
        length = min(len(a), len(b))
        if length == 0:
            return 0.0
        numerator = sum(x * y for x, y in zip(a[:length], b[:length]))
        denominator = (sum(x * x for x in a) ** 0.5) * (sum(y * y for y in b) ** 0.5)
        return numerator / denominator if denominator else 0.0

    def search(self, vector: List[float], limit: int = 5) -> List[Tuple[str, float]]:
        scored = [
            (key, self._similarity(vector, stored)) for key, stored in self.vectors.items()
        ]
        scored.sort(key=lambda item: item[1], reverse=True)
        return scored[:limit]

    def generate_embedding(self, text: str) -> List[float]:
        random.seed(hash(text))
        return [random.random() for _ in range(self.dimensions)]
