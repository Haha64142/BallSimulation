import math
from dataclasses import dataclass
from typing import Self


@dataclass(slots=True)
class Vec2:
    x: float = 0
    y: float = 0

    @classmethod
    def from_tuple(cls, vec: tuple[float, float]) -> Self:
        return cls(*vec)

    def __add__(self, other: Vec2) -> Vec2:
        if isinstance(other, Vec2):
            return Vec2(self.x + other.x, self.y + other.y)
        return NotImplemented

    def __sub__(self, other: Vec2) -> Vec2:
        if isinstance(other, Vec2):
            return Vec2(self.x - other.x, self.y - other.y)
        return NotImplemented

    def __mul__(self, other: Vec2 | int | float) -> Vec2:
        if isinstance(other, Vec2):
            return Vec2(self.x * other.x, self.y * other.y)
        elif isinstance(other, (int, float)):
            return Vec2(self.x * other, self.y * other)
        return NotImplemented

    def __rmul__(self, other: int | float) -> Vec2:
        if isinstance(other, (int, float)):
            return self * other
        return NotImplemented

    def __truediv__(self, other: Vec2 | int | float) -> Vec2:
        if isinstance(other, Vec2):
            return Vec2(self.x / other.x, self.y / other.y)
        elif isinstance(other, (int, float)):
            return Vec2(self.x / other, self.y / other)
        return NotImplemented

    def dot(self, other: Vec2) -> float:
        return self.x * other.x + self.y * other.y

    def magnitude(self) -> float:
        return math.hypot(self.x, self.y)

    def normalize(self) -> Vec2:
        mag = self.magnitude()
        if mag == 0:
            return Vec2()
        return self / mag
