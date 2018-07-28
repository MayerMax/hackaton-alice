import copy
from src.settings.settings import *
from src.tools.tools import *
from src.tools.parser import *
import numpy as np
import os

class TaskCreator():
    def __init__(self, graph, east_or_west_level=True):
        self.graph = copy.copy(graph)
        self.probs = copy.copy(self.graph)
        self.used_num = 0
        self.dir_path = []
        self.blocks_num = count_ones(self.graph)
        self.east_or_west_level = east_or_west_level
        self.step = 0

    def _dfs(self, x, y):
        print(x, y)
        self.step += 1
        if self.step > MAX_STEPS:
            return self.dir_path
        if self.probs[x][y] == 1:
            self.used_num += 1
            if self.used_num >= self.blocks_num:
                return self.dir_path
        self.probs[x][y] *= DECREASING_COEF
        directions_probs = [self.probs[x + direction[0]][y + direction[1]] for direction in DIRECTIONS]
        sum_prob = np.sum(directions_probs)
        if sum_prob == 0:
            return self.dir_path
        directions_probs = list(map(lambda x: x / sum_prob, directions_probs))
        choice = np.random.choice(list(np.arange(0, 4)), p=directions_probs)
        self.dir_path.append(choice)
        self._dfs(x + DIRECTIONS[choice][0], y + DIRECTIONS[choice][1])

    def _create_initial_point(self):
        width = len(self.graph)
        height = len(self.graph[0])
        y = np.random.randint(0, height)
        x = np.random.randint(0, width)
        while (self.graph[x][y] == 0):
            y = np.random.randint(0, height)
            x = np.random.randint(0, width)
        return x, y

    def _convert_to_directions(self):
        return self.dir_path

    def create_task(self):
        x, y = self._create_initial_point()
        path = self._dfs(x, y)
        if self.east_or_west_level:
            return GAP.join(list(map(lambda x: DIRECTIONS_NAME[x], self.dir_path))).strip()
        else:
            return self._convert_to_directions()

def generate_task(word):
    parser = WordParser(os.path.join('src', 'img'))
    tasks = []
    imgs = parser.parse_word(word)
    for img in imgs:
        task_creator = TaskCreator(img)
        tasks.append(task_creator.create_task())
    return tasks

if __name__ == "__main__":
    print(generate_task("00"))
