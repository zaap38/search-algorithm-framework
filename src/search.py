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
        # - self.env.__hash__()    ->   hash of the environment
        # - self.env.get_actions() ->   list of available actions
        # - self.env.do_action()   ->   env and transition cost after the action was done
        # - self.env.is_final()    ->   boolean whether the env is in a final state
        # - self.env.fitness()     ->   fitness score of the current env
        self.env = None

    def do_action_by_copy(self, env, action):
        new_env = cp.deepcopy(env)
        cost = new_env.do_action(action)
        return new_env, cost

    def search(self, env) -> list:
        path = []
        queue = [Node(env)]
        visited = dict()
        iteration = 0

        ptr = self.select_ptr(queue, visited)

        while not ptr.get_value().is_final():  # type: ignore
            ptr = self.select_ptr(queue, visited)
            iteration += 1
            if iteration > self.max_iterations:
                break

        if ptr.get_value().is_final():  # type: ignore
            path = []
            while ptr.pred is not None:
                path.append(ptr.last_action)
                ptr = ptr.pred
            return path

        return path

    def select_ptr(self, queue, visited):

        new_index: int = self.algorithm_dict[self.algorithm](queue)

        new_ptr: Node = queue[new_index]
        visited[new_ptr] = True
        queue.pop(new_index)

        for action in new_ptr.get_value().get_actions():  # type: ignore
            new_env, cost = self.do_action(new_ptr.get_value(), action)

            child = Node(new_env)
            child.pred = new_ptr  # type: ignore
            child.last_action = action

            child.cost = new_ptr.cost + cost
            child.depth = new_ptr.depth + 1
            pred_total_fitness = 0
            if new_ptr.total_fitness is not None:
                pred_total_fitness = new_ptr.total_fitness
            child.total_fitness = pred_total_fitness + child.get_fitness()
            new_ptr.add_child(child)

            if child not in visited and child.depth <= self.max_depth:
                queue.append(child)

        return new_ptr



    def algo_astar(self, queue) -> int:
        raise NotImplementedError("Algorithm " + self.algorithm + " is not implemented yet!")

    def algo_dijkstra(self, queue) -> int:
        raise NotImplementedError("Algorithm " + self.algorithm + " is not implemented yet!")

    def algo_double_dijkstra(self, queue) -> int:
        raise NotImplementedError("Algorithm " + self.algorithm + " is not implemented yet!")

    def algo_random_walk(self, queue) -> int:
        return rd.randint(0, len(queue) - 1)


class Node:

    def __init__(self, value=None) -> None:
        self.value: object = value
        self.children = []
        self.pred = None
        self.last_action = None

        self.fitness = None
        self.total_fitness = None
        self.cost = 0
        self.depth = 0

    def __eq__(self, value: object) -> bool:
        return id(self) == id(value)

    def __id__(self) -> int:
        return hash(self)

    def __hash__(self) -> int:
        return hash(self.value)

    def set_value(self, value):
        self.value = value

    def get_value(self):
        return self.value

    def add_child(self, child):
        self.children.append(child)

    def get_fitness(self):
        if self.fitness is None:
            self.fitness = self.get_value().fitness()  # type: ignore
        return self.fitness
    