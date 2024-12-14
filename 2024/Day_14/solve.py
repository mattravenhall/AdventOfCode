#!/usr/bin/env python3.11

from collections import Counter
from functools import partial
import math
import re

from matplotlib.animation import FuncAnimation, PillowWriter
import matplotlib.pyplot as plt

re_robots = r'p=(-?\d+),(-?\d+) v=(-?\d+),(-?\d+)'


class RobotRestroom():
    def __init__(self, input_file: str, space: tuple[int, int] = (101, 103)) -> None:
        self.space = space
        self.robots = self._parse_input(input_file)

    def _parse_input(self, input_file: str) -> list[tuple]:
        robots = []
        for line in open(input_file).readlines():
            pos_x, pos_y, vel_x, vel_y = map(int, re.match(re_robots, line).groups())
            robots.append([pos_x, pos_y, vel_x, vel_y])
        return robots

    def _display_positions(self, positions: list[tuple], console: bool = True):
        pos_table = []
        pos_counts = Counter(positions)
        for y in range(self.space[1]):
            row = ''
            for x in range(self.space[0]):
                row += str(pos_counts.get((x, y), '.'))
            if console:
                print(row)
            else:
                pos_table.append(row)

        if console:
            return pos_table

    def _display_step_range(self, steps=5):
        """This is purely for dev/debugging, it allows us to manually verify the given example."""
        print(f"> Initial <")
        self._display_positions([(p0, p1) for p0, p1, v0, v1 in self.robots])
        for step in range(1, steps+1):
            print(f"> After {step} seconds <")
            step_positions = []
            for robot in self.robots:
                step_positions.append(self._update_position(robot[0:2], robot[2:], steps))
            self._display_positions(step_positions)

    def _update_position(self, position: tuple[int, int], velocity: tuple[int, int], steps) -> tuple[int, int]:
        # For each robot, apply their velocities
        distance = [
            velocity[0] * steps,
            velocity[1] * steps,
        ]
        new_pos = list(map(sum, zip(position, distance)))

        # If movement would take a robot out of bounds, teleport to the other side
        new_pos[0] = new_pos[0] % self.space[0]
        new_pos[1] = new_pos[1] % self.space[1]

        return tuple(new_pos)

    def _determine_quandrant(self, position: tuple[int, int]) -> str:
        left = position[0] in range(0, self.space[0] // 2)
        right = position[0] in range(self.space[0] - (self.space[0] // 2), self.space[0])
        top = position[1] in range(0, self.space[1] // 2)
        bottom = position[1] in range(self.space[1] - (self.space[1] // 2), self.space[1])

        if sum([left, right, top, bottom]) > 2:
            raise Exception("Invalid quadrants")

        match (left, right, top, bottom):
            case (True, False, True, False):
                return "TL"
            case (False, True, True, Right):
                return "TR"
            case (True, False, False, True):
                return "BL"
            case (False, True, False, True):
                return "BR"
            case _:
                return "Void"

    def calc_safety_factor(self, steps: int) -> int:
        # Update all robot positions for `steps` interations
        updated_positions = []
        for robot in self.robots:
            updated_positions.append(self._update_position(robot[0:2], robot[2:], 100))

        # Count up robots in each quadrant
        quandrant_counts = {
            "TL": 0,
            "TR": 0,
            "BL": 0,
            "BR": 0,
            "Void": 0,
        }
        for position in updated_positions:
            quandrant = self._determine_quandrant(position)
            quandrant_counts[quandrant] += 1
        
        safety_factor = math.prod([value for key, value in quandrant_counts.items() if key != "Void"])
        return safety_factor

    def _positions_grid_at_step(self, steps):
        # Get positions at timepoint
        positions = []
        for robot in self.robots:
            positions.append(self._update_position(robot[0:2], robot[2:], steps))
        
        # Convert to a grid
        pos_counts = Counter(positions)
        positions_table = []
        for y in range(self.space[1]):
            row = []
            for x in range(self.space[0]):
                row.append(pos_counts.get((x, y), 0))
            positions_table.append(row)
        
        return positions_table

    def search_for_xmas_tree(self, start_frame: int, total_steps: int, animate: bool = False):
        plt.style.use("mrdark.mplstyle")

        filename = "xmas_tree"

        if animate:
            # Produce gif
            fps = 1

            fig, ax = plt.subplots()
            ax.set_xlim(0, self.space[0])
            ax.set_ylim(0, self.space[1])
            ax.set_axis_off()
            title = ax.text(0.5,0.85, "", bbox={'facecolor':'w', 'alpha':0.5, 'pad':5}, transform=ax.transAxes, ha="center")
            fig.tight_layout(pad=0)

            initial_positions = partial(self._positions_grid_at_step)
            image = plt.imshow(initial_positions(start_frame), interpolation='none')
        
            def update(step):
                current_step = start_frame + step
                pos_table = self._positions_grid_at_step(current_step)
                image.set_array(pos_table)
                title.set_text(current_step)
                return [image]

            anim = FuncAnimation(
                fig,
                update,
                frames=total_steps,
                blit=True
            )

            writer = PillowWriter(
                fps=fps,
                metadata=dict(artist='Me'),
                bitrate=1800
            )
            anim.save(f"{filename}.gif", writer=writer)
            plt.close()
        else:
            # Produce pngs
            for step in range(start_frame, start_frame + total_steps):
                fig, ax = plt.subplots()
                ax.set_xlim(0, self.space[0])
                ax.set_ylim(0, self.space[1])
                ax.set_axis_off()
                title = ax.text(0.5,0.85, "", bbox={'facecolor':'w', 'alpha':0.5, 'pad':5}, transform=ax.transAxes, ha="center")
                fig.tight_layout(pad=0)

                positions = self._positions_grid_at_step(step)
                image = plt.imshow(positions, interpolation='none')
                title.set_text(step)

                plt.savefig(f"{filename}_{step}.png")
                plt.close()

# RobotRestroom("./test2.txt", space=(11,7))._display_step_range(5)
assert RobotRestroom("./test.txt", space=(11, 7)).calc_safety_factor(steps=100) == 12

solver = RobotRestroom('./input.txt')
print(f"A: {solver.calc_safety_factor(steps=100)}")
solver.search_for_xmas_tree(start_frame=6642, total_steps=3, animate=True)  # Found by manual review
