from search import SearchEngine



class Env:

    def __init__(self) -> None:
        self.actions = ["RIGHT", "UP"]
        self.start_state = [0, 0]
        self.state = self.start_state
        self.final_state = [3, 5]

    def __hash__(self) -> int:
        return hash(tuple(self.state))

    def get_actions(self):
        return self.actions

    def do_action(self, action):
        if action == "RIGHT":
            self.state[0] += 1
        elif action == "UP":
            self.state[1] += 1
        return 1

    def is_final(self):
        return self.state == self.final_state

    def fitness(self):
        return abs(self.state[0] - self.final_state[0]) + \
               abs(self.state[1] - self.final_state[1])


if __name__ == "__main__":

    se =  SearchEngine("random_walk")

    my_env = Env()

    print(se.search(my_env))