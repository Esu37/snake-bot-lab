import pygame

from config import CELL_SIZE


class Renderer:
    def __init__(self, rows, cols):
        pygame.init()
        self.rows = rows
        self.cols = cols
        self.width = cols * CELL_SIZE
        self.height = rows * CELL_SIZE
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Snake Lab")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 28)

    def draw(self, env, fps):
        self.screen.fill((18, 18, 18))

        # Grid
        for r in range(env.rows):
            for c in range(env.cols):
                rect = pygame.Rect(
                    c * CELL_SIZE,
                    r * CELL_SIZE,
                    CELL_SIZE,
                    CELL_SIZE,
                )
                pygame.draw.rect(self.screen, (35, 35, 35), rect, 1)

        # Food
        if env.food is not None:
            fr, fc = env.food
            food_rect = pygame.Rect(
                fc * CELL_SIZE,
                fr * CELL_SIZE,
                CELL_SIZE,
                CELL_SIZE,
            )
            pygame.draw.rect(self.screen, (255, 80, 80), food_rect)
            pygame.draw.rect(self.screen, (255, 220, 220), food_rect, 2)

        # Snake
        for i, (r, c) in enumerate(env.snake):
            outer = pygame.Rect(
                c * CELL_SIZE,
                r * CELL_SIZE,
                CELL_SIZE,
                CELL_SIZE,
            )
            inner = outer.inflate(-4, -4)

            if i == 0:
                fill_color = (110, 240, 140)
                border_color = (245, 255, 245)
            else:
                fill_color = (40, 180, 90)
                border_color = (15, 80, 35)

            pygame.draw.rect(self.screen, border_color, outer)
            pygame.draw.rect(self.screen, fill_color, inner)

        # Score
        text = self.font.render(f"Score: {env.score}", True, (240, 240, 240))
        self.screen.blit(text, (10, 10))

        pygame.display.flip()
        self.clock.tick(fps)