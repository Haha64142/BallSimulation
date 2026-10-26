import tkinter as tk
from utils import Vec2


class Room:
    canvas: tk.Canvas
    points: list[Vec2]
    directions: list[Vec2]
    normals: list[Vec2]
    object_id: int

    def __init__(self, canvas: tk.Canvas, points: list[Vec2]) -> None:
        self.canvas = canvas
        self.points = points
        length = len(points)
        self.directions = [Vec2() for _ in range(length)]
        self.normals = [Vec2() for _ in range(length)]
        for i in range(length):
            direc = points[(i + 1) % length] - points[i]
            self.directions[i] = direc
            self.normals[i] = Vec2(direc.y, -direc.x).normalize()

    def draw(self) -> int:
        self.object_id = self.canvas.create_polygon(
            [(v.x, v.y) for v in self.points], fill="", outline="black"
        )
        return self.object_id
