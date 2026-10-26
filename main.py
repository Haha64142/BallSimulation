import time
import tkinter as tk
from ball import Ball
from room import Room
from utils import Vec2


class Simulation:
    canvas: tk.Canvas
    prev_time: float
    paused: bool = True

    def __init__(self, canvas: tk.Canvas) -> None:
        self.canvas = canvas
        self.ball = Ball(self.canvas, 10, Vec2(100, 200), Vec2(200, 100))
        self.room = Room(
            self.canvas, [Vec2(20, 20), Vec2(20, 340), Vec2(620, 340), Vec2(620, 20)]
        )

        self.canvas.winfo_toplevel().bind("<space>", self.pause)

    def start(self) -> None:
        self.prev_time = time.perf_counter()
        self.ball.draw()
        self.room.draw()
        self.update()

    def update(self) -> None:
        cur_time = time.perf_counter()
        delta_time = cur_time - self.prev_time

        if not self.paused:
            self.physics_update(delta_time)

        self.prev_time = cur_time
        self.canvas.after(16, self.update)

    def physics_update(self, delta_time) -> None:
        self.ball.move_and_collide(delta_time, self.room)

    def pause(self, e) -> None:
        self.paused = not self.paused


root = tk.Tk()
root.title("Ball Simulation")
root.attributes("-topmost", True)
root.update_idletasks()
root.attributes("-topmost", False)

canvas = tk.Canvas(root, width=640, height=360, bg="white")
canvas.pack()

sim = Simulation(canvas)
sim.start()

root.mainloop()
