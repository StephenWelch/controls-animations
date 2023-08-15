from matplotlib.lines import Line2D
import numpy as np
from collections import defaultdict
from collections.abc import Hashable
from matplotlib.figure import Figure
from matplotlib.animation import FuncAnimation
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Line3D
from dataclasses import dataclass, field

Color = tuple[float, float, float] | str

@dataclass
class Line:
    x: list[float] = field(default_factory=list)
    y: list[float] = field(default_factory=list)
    z: list[float] = field(default_factory=list)
    color: list[Color] = field(default_factory=list)

class AnimatedPlot3d:

    def __init__(self, fig: Figure, dt: float):
        self._fig = fig
        self._axes = fig.add_subplot(projection="3d")


        self.dt = dt
        self.lines: dict[Hashable, Line] = {}
        self.line_objs: dict[Hashable, Line3D] = {}

    def add_data(self, name: Hashable, x: float, y: float, z: float, color: Color = 'r'):
        if name not in self.lines:
            self.lines[name] = Line()
            line_obj, = self._axes.plot([x], [y], [z], color=color, label=name)
            self.line_objs[name] = line_obj

        self.lines[name].x.append(x)
        self.lines[name].y.append(y)
        self.lines[name].z.append(z)
        self.lines[name].color.append(color)
        
    def plot(self):
        ...

    def _update_anim(self, frame_idx: int) -> list[Line3D]:
        modified_line_objs = []
        
        # if frame_idx == 0:
        #     return []
        
        for name, line in self.lines.items():
            # some lines may be shorter than others
            if frame_idx >= len(line.x):
                continue

            line_obj = self.line_objs[name]

            line_obj.set_data_3d(line.x[:frame_idx], line.y[:frame_idx], line.z[:frame_idx])
            line_obj.set_color(line.color[frame_idx])
            # line_obj.set_color(line.color[:frame_idx])

            modified_line_objs.append(line_obj)

        return modified_line_objs

    def animate(self):

        self._axes.set_xlim3d(1.1*min([min(line.x) for line in self.lines.values()]), 1.1*max([max(line.x) for line in self.lines.values()]))
        self._axes.set_ylim3d(1.1*min([min(line.y) for line in self.lines.values()]), 1.1*max([max(line.y) for line in self.lines.values()]))
        self._axes.set_zlim3d(1.1*min([min(line.z) for line in self.lines.values()]), 1.1*max([max(line.z) for line in self.lines.values()]))

        anim = FuncAnimation(self._fig, lambda i: self._update_anim(i), interval=self.dt*1000, blit=True)
        return anim