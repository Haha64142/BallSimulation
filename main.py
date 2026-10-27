from typing import Callable
import time
import tkinter as tk
from ball import Ball
from room import Room
from utils import Vec2


class Simulation:
    canvas: tk.Canvas
    prev_frame_time: float
    paused: bool = False

    pressed_keys: set[str] = set()
    key_press_funcs: dict[str, Callable[[tk.Event], None]] = {}
    key_repeat_funcs: dict[str, Callable[[], None]] = {}
    key_release_funcs: dict[str, Callable[[tk.Event], None]] = {}

    room_editing: bool = False
    room_edit_points: list[Vec2]
    room_edit_lines_id: int | None

    def __init__(self, canvas: tk.Canvas) -> None:
        self.canvas = canvas

        root = self.canvas.winfo_toplevel()

        root.bind("<KeyPress>", self.press_key)
        root.bind("<KeyRelease>", self.release_key)
        self.add_key_press_func("space", lambda _e: self.pause())
        self.add_key_press_func("e", lambda _e: self.edit_room())
        self.add_key_press_func("r", lambda _e: self.reset_environment())

        root.bind("<Button-1>", self.add_room_point)

    def start(self) -> None:
        self.reset_environment()
        self.prev_frame_time = time.perf_counter()
        self.update()

    def update(self) -> None:
        cur_time = time.perf_counter()
        delta_time = cur_time - self.prev_frame_time

        for key, func in self.key_repeat_funcs.items():
            if key in self.pressed_keys:
                func()

        if not self.paused:
            self.physics_update(delta_time)

        self.prev_frame_time = cur_time
        self.canvas.after(5, self.update)

    def physics_update(self, delta_time: float) -> None:
        self.ball.move_and_collide(delta_time, self.room)

    def reset_environment(self) -> None:
        if hasattr(self, "ball"):
            self.ball.erase()
        if hasattr(self, "room"):
            self.room.erase()

        self.ball = Ball(self.canvas, 10, Vec2(320, 180), Vec2(200, 100))
        self.room = Room(
            self.canvas, [Vec2(20, 20), Vec2(20, 340), Vec2(620, 340), Vec2(620, 20)]
        )
        # self.room = Room(self.canvas, [Vec2(20, 20), Vec2(320, 340), Vec2(620, 100)])

        self.ball.draw()
        self.room.draw()

    def pause(self) -> None:
        self.paused = not self.paused

    def edit_room(self) -> None:
        self.pause()

        self.room_editing = self.paused
        if self.room_editing:
            self.room.erase()
            self.room_edit_points = []
            self.room_edit_lines_id = None
        else:
            if not self.room_edit_lines_id == None:
                self.canvas.delete(self.room_edit_lines_id)
                self.room_edit_lines_id = None
            self.room = Room(self.canvas, self.room_edit_points)
            self.room.draw()

    def add_room_point(self, e: tk.Event) -> None:
        if self.room_editing:
            self.room_edit_points.append(Vec2(e.x, e.y))
            if len(self.room_edit_points) > 1:
                if not self.room_edit_lines_id == None:
                    self.canvas.delete(self.room_edit_lines_id)
                self.room_edit_lines_id = self.canvas.create_line(
                    [(v.x, v.y) for v in self.room_edit_points], capstyle="round"
                )

    def press_key(self, e: tk.Event) -> None:
        key = e.keysym

        if key in self.pressed_keys:
            return

        self.pressed_keys.add(key)
        if key in self.key_press_funcs:
            return self.key_press_funcs[key](e)

    def release_key(self, e: tk.Event) -> None:
        key = e.keysym

        if key not in self.pressed_keys:
            return

        self.pressed_keys.remove(key)
        if key in self.key_release_funcs:
            return self.key_release_funcs[key](e)

    def add_key_press_func(self, key: str, func: Callable[[tk.Event], None]):
        self.key_press_funcs[key] = func

    def add_key_release_func(self, key: str, func: Callable[[tk.Event], None]):
        self.key_release_funcs[key] = func

    def add_key_repeat_func(self, key: str, func: Callable[[], None]):
        self.key_repeat_funcs[key] = func


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
