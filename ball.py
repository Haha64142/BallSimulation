import tkinter as tk
from room import Room
from utils import Vec2, sign


class Ball:
    canvas: tk.Canvas
    radius: int
    position: Vec2
    velocity: Vec2
    object_id: int | None = None

    def __init__(
        self,
        canvas,
        radius: int = 10,
        position: Vec2 | None = None,
        velocity: Vec2 | None = None,
    ) -> None:
        self.canvas = canvas
        self.radius = radius
        self.position = position if position is not None else Vec2()
        self.velocity = velocity if velocity is not None else Vec2()

    def __repr__(self) -> str:
        return f"Ball(canvas={self.canvas}, radius={self.radius}, position={self.position}, velocity={self.velocity})"

    def draw(self) -> int:
        if not self.object_id == None:
            self.erase()

        self.object_id = self.canvas.create_oval(
            self.position.x - self.radius,
            self.position.y - self.radius,
            self.position.x + self.radius,
            self.position.y + self.radius,
        )
        return self.object_id

    def erase(self) -> None:
        if self.object_id == None:
            return

        self.canvas.delete(self.object_id)
        self.object_id = None

    def move(self, delta: float) -> None:
        pos_delta = self.velocity * delta
        self.position += pos_delta
        self.canvas.move(self.object_id, pos_delta.x, pos_delta.y)

    def move_and_collide(self, delta: float, room: Room) -> None:
        pos_delta = self.velocity * delta
        new_pos = self.position + pos_delta

        i = 0
        while i < len(room.points):
            cur_distance = (self.position - room.points[i]).dot(room.normals[i]) + sign(
                self.velocity.dot(room.normals[i])
            ) * self.radius
            new_distance = (new_pos - room.points[i]).dot(room.normals[i]) + sign(
                self.velocity.dot(room.normals[i])
            ) * self.radius

            if cur_distance * new_distance < 0:
                new_pos -= 2 * new_distance * room.normals[i]
                self.velocity = (
                    self.velocity
                    - 2 * self.velocity.dot(room.normals[i]) * room.normals[i]
                )
                i = 0
                continue

            i += 1

        pos_delta = new_pos - self.position
        self.position = new_pos
        self.canvas.move(self.object_id, pos_delta.x, pos_delta.y)
