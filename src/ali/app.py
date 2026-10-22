"""Interactive desktop simulator. No physical hardware is controlled here."""

from __future__ import annotations

import tkinter as tk
from tkinter import messagebox

from ali.config import SimulationConfig
from ali.core.models import Cell
from ali.navigation.astar import plan_path
from ali.navigation.grid import GridWorld


class AliSimulator:
    def __init__(self, root: tk.Tk, config: SimulationConfig | None = None):
        self.root = root
        self.config = config or SimulationConfig()
        self.world = GridWorld(self.config.width, self.config.height)
        self.start = Cell(1, 1)
        self.robot = self.start
        self.goal = Cell(self.config.width - 2, self.config.height - 2)
        self.path: list[Cell] = []
        self.paused = False
        self.running = True

        root.title("Ali — Robotics Simulator")
        root.minsize(700, 520)
        self.status = tk.StringVar(value="Ready — simulation only; no hardware connected.")
        bar = tk.Frame(root, padx=10, pady=8)
        bar.pack(fill="x")
        tk.Label(bar, text="ALI", font=("Segoe UI", 16, "bold")).pack(side="left")
        tk.Label(bar, textvariable=self.status, anchor="w").pack(side="left", padx=16)
        tk.Button(bar, text="Plan path", command=self.replan).pack(side="right", padx=3)
        tk.Button(bar, text="Reset", command=self.reset).pack(side="right", padx=3)

        self.canvas = tk.Canvas(root, bg="#111827", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True, padx=10, pady=(0, 8))
        tk.Label(root, text="Left click: goal  •  Right click: obstacle  •  Space: pause  •  R: reset  •  Arrows: manual step",
                 pady=8).pack(fill="x")
        self.canvas.bind("<Button-1>", self.on_left_click)
        self.canvas.bind("<Button-3>", self.on_right_click)
        self.canvas.bind("<Configure>", lambda _event: self.draw())
        root.bind("<space>", self.toggle_pause)
        root.bind("<r>", lambda _event: self.reset())
        root.bind("<R>", lambda _event: self.reset())
        for key, delta in {"<Up>": (0, -1), "<Down>": (0, 1),
                           "<Left>": (-1, 0), "<Right>": (1, 0)}.items():
            root.bind(key, lambda event, d=delta: self.manual_step(*d))
        self.replan()
        self.root.protocol("WM_DELETE_WINDOW", self.close)

    def cell_at(self, event: tk.Event) -> Cell | None:
        cw = self.canvas.winfo_width() / self.config.width
        ch = self.canvas.winfo_height() / self.config.height
        if cw <= 0 or ch <= 0:
            return None
        cell = Cell(int(event.x / cw), int(event.y / ch))
        return cell if self.world.contains(cell) else None

    def on_left_click(self, event: tk.Event) -> None:
        cell = self.cell_at(event)
        if cell and self.world.is_free(cell) and cell != self.robot:
            self.goal = cell
            self.replan()

    def on_right_click(self, event: tk.Event) -> None:
        cell = self.cell_at(event)
        if not cell or cell in (self.robot, self.goal):
            return
        self.world.set_obstacle(cell, cell not in self.world.obstacles)
        self.replan()

    def replan(self) -> None:
        self.path = plan_path(self.world, self.robot, self.goal)
        if self.path:
            self.status.set(f"Path found: {len(self.path) - 1} steps — simulation only.")
        else:
            self.status.set("No safe path found. Change the goal or remove obstacles.")
        self.draw()

    def toggle_pause(self, _event: tk.Event | None = None) -> None:
        self.paused = not self.paused
        self.status.set("Paused." if self.paused else "Simulation resumed.")

    def manual_step(self, dx: int, dy: int) -> None:
        if self.paused:
            return
        candidate = Cell(self.robot.x + dx, self.robot.y + dy)
        if not self.world.is_free(candidate):
            self.status.set("Blocked: movement rejected by world safety check.")
            return
        if dx and dy and (not self.world.is_free(Cell(self.robot.x + dx, self.robot.y))
                          or not self.world.is_free(Cell(self.robot.x, self.robot.y + dy))):
            self.status.set("Blocked: diagonal corner cutting is forbidden.")
            return
        self.robot = candidate
        self.replan()

    def reset(self) -> None:
        self.world = GridWorld(self.config.width, self.config.height)
        self.robot = self.start
        self.goal = Cell(self.config.width - 2, self.config.height - 2)
        self.paused = False
        self.replan()

    def draw(self) -> None:
        if not hasattr(self, "canvas"):
            return
        self.canvas.delete("all")
        width, height = self.canvas.winfo_width(), self.canvas.winfo_height()
        if width < 2 or height < 2:
            return
        cw, ch = width / self.config.width, height / self.config.height
        for y in range(self.config.height):
            for x in range(self.config.width):
                cell = Cell(x, y)
                x1, y1, x2, y2 = x * cw, y * ch, (x + 1) * cw, (y + 1) * ch
                fill = "#1f2937"
                if cell in self.world.obstacles:
                    fill = "#ef4444"
                elif cell in self.path:
                    fill = "#155e75"
                if cell == self.goal:
                    fill = "#22c55e"
                if cell == self.robot:
                    fill = "#60a5fa"
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=fill, outline="#374151")
                if cell in (self.robot, self.goal):
                    label = "A" if cell == self.robot else "G"
                    self.canvas.create_text((x1+x2)/2, (y1+y2)/2, text=label,
                                            fill="#0b1020", font=("Segoe UI", 11, "bold"))

    def close(self) -> None:
        self.running = False
        self.root.destroy()


def main() -> None:
    try:
        root = tk.Tk()
    except tk.TclError as exc:
        messagebox.showerror("Ali Simulator", f"Could not start the desktop UI: {exc}")
        return
    AliSimulator(root)
    root.mainloop()
