
import copy
from settings/settings import *
from tools/tools import *
import numpy as np


class TaskCreator():
    def __init__(self, kontur):
        self.graph = kontur
        self.probs = copy.copy(self.graph)
        self.used_num = 0
        self.dir_path = []
        self.blocks_num = count_blocks(self.graph)

    def _dfs(self, x, y):
        if self.probs[x][y] == 1:
            self.used_num += 1
            if self.used_num >= self.blocks_num:
                return self.dir_path
        self.probs[x][y] *= DECREASING_COEF
        directions_probs = [self.probs[x + direction[0]][y + direction[1]] for direction in DIRECTIONS]
        sum_prob = np.sum(directions_probs)
        directions_probs = list(map(lambda x: x / sum_prob, directions_probs))
        choice = np.random.choice(list(np.arange(0, 4)), p=directions_probs)
        self.dir_path.append(choice)
        self._dfs(x + DIRECTIONS[choice][0], y + DIRECTIONS[choice][1])

    def _create_initial_point(self):
        return 1, 1

    def create_task(self, mode="EastOrWest"):
        x, y = self._create_initial_point()
        path = self._dfs(x, y)
        if mode == "EastOrWest":
            return list(map(lambda x: DIRECTIONS_NAME[x], self.dir_path))


if __name__ == "__main__":
    kontur_test = [[0, 0, 0, 0], [0, 1, 0, 0], [0, 1, 0, 0], [0, 1, 0, 0], [0, 1, 1, 0], [0, 0, 1, 0], [0, 0, 0, 0]]
    test = TaskCreator(kontur_test)
    print(test.create_task())
