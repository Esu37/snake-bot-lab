import random
import copy

from config import ROWS, COLS, RIGHT, ACTIONS


class SnakeEnv:
    def __init__(self, rows=ROWS, cols=COLS, max_steps=None, max_idle_steps=None):
        self.rows = rows
        self.cols = cols
        self.max_steps = max_steps
        self.max_idle_steps = max_idle_steps
        self.reset()

    def reset(self):
        center = (self.rows // 2, self.cols // 2)
        self.direction = RIGHT
        self.snake = [
            center,
            (center[0], center[1] - 1),
            (center[0], center[1] - 2),
        ]
        self.score = 0
        self.done = False
        self.steps = 0
        self.idle_steps = 0
        self.food = None
        self._place_food()
        return self.get_state()

    def clone(self):
        return copy.deepcopy(self)

    def _place_food(self):
        empty = [
            (r, c)
            for r in range(self.rows)
            for c in range(self.cols)
            if (r, c) not in self.snake
        ]
        self.food = random.choice(empty) if empty else None

    def in_bounds(self, pos):
        r, c = pos
        return 0 <= r < self.rows and 0 <= c < self.cols

    def is_collision(self, pos):
        if not self.in_bounds(pos):
            return True
        return pos in self.snake[:-1]

    def legal_actions(self):
        head = self.snake[0]
        valid = []
        for action in ACTIONS:
            nr = head[0] + action[0]
            nc = head[1] + action[1]
            nxt = (nr, nc)
            if not self.is_collision(nxt):
                valid.append(action)
        return valid

    def step(self, action):
        if self.done:
            return self.get_state(), 0, True, {"score": self.score}

        self.direction = action
        head = self.snake[0]
        new_head = (head[0] + action[0], head[1] + action[1])

        self.steps += 1
        self.idle_steps += 1

        if self.is_collision(new_head):
            self.done = True
            return self.get_state(), -10, True, {"score": self.score}

        self.snake.insert(0, new_head)

        reward = 0
        if new_head == self.food:
            self.score += 1
            reward = 10
            self.idle_steps = 0
            self._place_food()
        else:
            self.snake.pop()

        if self.food is None:
            self.done = True

        if self.max_steps is not None and self.steps >= self.max_steps and not self.done:
            self.done = True

        if self.max_idle_steps is not None and self.idle_steps >= self.max_idle_steps and not self.done:
            self.done = True

        return self.get_state(), reward, self.done, {"score": self.score}

    def get_state(self):
        return {
            "rows": self.rows,
            "cols": self.cols,
            "snake": self.snake[:],
            "food": self.food,
            "direction": self.direction,
            "score": self.score,
            "done": self.done,
            "steps": self.steps,
            "idle_steps": self.idle_steps,
        }