import pandas as pd
import numpy as np

from collections import defaultdict
from typing import Dict, List, Union


# class SimpleBox:
#     def __init__(self, balls: List[Dict[str, Union[str, int]]]):
#         self.data = pd.DataFrame(balls)
#         self.color_probs = {"red": 0.5, "green": 0.3, "blue": 0.2}
#         self.texture_probs = {"smooth": 0.35, "non-smooth": 0.65}
#
#     def get_ball(self):
#         color = np.random.choice(list(self.color_probs.keys()), p=list(self.color_probs.values()))
#         texture = np.random.choice(list(self.texture_probs.keys()), p=list(self.texture_probs.values()))
#
#         return \
#             self.data[(self.data["color"] == color) & (self.data["texture"] == texture)].sample().to_dict(
#                 orient="records")[
#                 0]
#
#     def add_ball(self, ball: Dict[str, Union[str, int]]):
#         self.data.append(ball)
#
#
# class PandasBox:
#     def __init__(self, balls: List[Dict[str, Union[str, int]]]):
#         self.data = pd.DataFrame(balls)
#         self.color_probs = {"red": 0.5, "green": 0.3, "blue": 0.2}
#         self.colors = list(self.color_probs.keys())
#         self.c_probs = list(self.color_probs.values())
#
#         self.texture_probs = {"smooth": 0.35, "non-smooth": 0.65}
#         self.textures = list(self.texture_probs.keys())
#         self.t_probs = list(self.texture_probs.values())
#
#         self.joint_indexes = defaultdict(lambda: defaultdict(list))
#
#         for color in self.color_probs.keys():
#             for texture in self.texture_probs.keys():
#                 self.joint_indexes[color][texture] = self.data.index[
#                     (self.data["color"] == color) & (self.data["texture"] == texture)]
#
#     def get_ball(self):
#
#         color = np.random.choice(self.colors, p=self.c_probs)
#         texture = np.random.choice(self.textures, p=self.t_probs)
#
#         idx = np.random.choice(self.joint_indexes[color][texture])
#
#         return self.data.iloc[idx].to_dict()
#
#     def add_ball(self, ball: Dict[str, Union[str, int]]):
#         self.data.append(ball)


class Box:
    def __init__(self, balls: List[Dict[str, Union[str, int]]], alloc_size=10000):
        self.data = balls
        self.color_probs = {"red": 0.5, "green": 0.3, "blue": 0.2}
        self.colors = list(self.color_probs.keys())
        self.c_probs = list(self.color_probs.values())

        self.texture_probs = {"smooth": 0.35, "non-smooth": 0.65}
        self.textures = list(self.texture_probs.keys())
        self.t_probs = list(self.texture_probs.values())

        self.joint_indexes = defaultdict(lambda: defaultdict(list))

        for i, ball in enumerate(self.data):
            self.joint_indexes[ball["color"]][ball["texture"]].append(i)

        self.pointer = 0
        self.alloc_colors = None
        self.alloc_textures = None
        self.alloc_idx = None
        self.alloc_size = alloc_size

        self._allocate_random_vars()

    def _allocate_random_vars(self):
        self.pointer = 0
        self.alloc_colors = np.random.choice(self.colors, size=self.alloc_size, p=self.c_probs)
        self.alloc_textures = np.random.choice(self.textures, size=self.alloc_size, p=self.t_probs)
        # np.random.choice(self.joint_indexes[self.alloc_colors[i]][self.alloc_textures[i]])
        self.alloc_idx = [self.joint_indexes[self.alloc_colors[i]][self.alloc_textures[i]][np.random.randint(0, len(
            self.joint_indexes[self.alloc_colors[i]][self.alloc_textures[i]]))] for i in
                          range(self.alloc_size)]

    def get_ball(self):

        idx = self.alloc_idx[self.pointer]

        self.pointer += 1

        if self.pointer >= self.alloc_size:
            self._allocate_random_vars()

        return self.data[idx]

    def add_ball(self, ball: Dict[str, Union[str, int]]):
        self.joint_indexes[ball["color"]][ball["texture"]].append(len(self.data))

        self.data.append(ball)
