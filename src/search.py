import copy as cp
import random as rd
from typing import Callable


class SearchEngine:

    def __init__(self,
                 algorithm=None,
                 max_depth=float('inf'),
                 max_iterations=float('inf'),
                 is_functional=False) -> None:
        
        self.algorithm_dict = {
            'astar': self.algo_astar,
            'dijkstra': self.algo_dijkstra,
            'double_dijkstra': self.algo_double_dijkstra,
            'random_walk': self.algo_random_walk,
        }
        
        if algorithm in self.algorithm_dict:
            self.algorithm = algorithm
        else:
            self.algorithm = 'astar'

        self.max_depth = max_depth
        self.max_iterations = max_iterations

        self.env_is_functional = is_functional  # if true, uses optimizations to run the search faster
        self.do_action: Callable = self.do_action_by_copy
        if self.env_is_functional:
            self.do_action = lambda env, action: env.do_action(action)

        # self.env requires the following functions:
        # - self.env.get_actions() -> list of available actions
        # - self.env.do_action() -> env after the action was done
        # - self.env.is_final() -> boolean whether the env is in a final state
        # - self.env.fitness() -> fitness score of the current env
        self.env = None

    def do_action_by_copy(self, env, action):
        new_env = cp.deepcopy(env)
        new_env.do_action(action)
        return new_env

    def search(self, env) -> tuple[list, float]:
        path, fitness = self.algorithm_dict[self.algorithm](env)
        return path, fitness

    def algo_astar(self, env):
        raise NotImplementedError("Algorithm " + self.algorithm + " is not implemented yet!")

    def algo_dijkstra(self, env):
        raise NotImplementedError("Algorithm " + self.algorithm + " is not implemented yet!")

    def algo_double_dijkstra(self, env):
        raise NotImplementedError("Algorithm " + self.algorithm + " is not implemented yet!")

    def algo_random_walk(self, env):
        raise NotImplementedError("Algorithm " + self.algorithm + " is not implemented yet!")


class Node:

    def __init__(self) -> None:
        self.value = None
        self.children = []

    def set_value(self, value):
        self.value = value

    def get_value(self):
        return self.value

    def add_child(self, child):
        self.children.append(child)
    