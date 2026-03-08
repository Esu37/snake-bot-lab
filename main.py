import argparse
import pygame

from config import HUMAN_FPS, BOT_FPS, UP, DOWN, LEFT, RIGHT
from snake_env import SnakeEnv
from render import Renderer
from bots.hamiltonian_bot import HamiltonianBot
from bots.astar_bot import AStarBot
from bots.hybrid_bot import HybridBot
from bots.rl_agent import RLAgent


def get_human_action(current):
    keys = pygame.key.get_pressed()

    if keys[pygame.K_UP]:
        return UP
    if keys[pygame.K_DOWN]:
        return DOWN
    if keys[pygame.K_LEFT]:
        return LEFT
    if keys[pygame.K_RIGHT]:
        return RIGHT

    return current


def run_human():
    env = SnakeEnv()
    renderer = Renderer(env.rows, env.cols)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        action = get_human_action(env.direction)
        _, _, done, _ = env.step(action)
        renderer.draw(env, HUMAN_FPS)

        if done:
            print(f"Game over. Score: {env.score}, Steps: {env.steps}")
            running = False

    pygame.quit()


def run_bot(bot):
    env = SnakeEnv()
    renderer = Renderer(env.rows, env.cols)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        action = bot.get_action(env)
        _, _, done, _ = env.step(action)
        renderer.draw(env, BOT_FPS)

        if done:
            print(f"{bot.__class__.__name__} finished. Score: {env.score}, Steps: {env.steps}")
            running = False

    pygame.quit()


def benchmark_bot(bot_class, games=20, max_steps=None):
    scores = []
    steps_list = []

    for game_num in range(1, games + 1):
        env = SnakeEnv(max_steps=max_steps)
        bot = bot_class(env.rows, env.cols)

        while not env.done:
            action = bot.get_action(env)
            env.step(action)

        scores.append(env.score)
        steps_list.append(env.steps)

        print(
            f"{bot_class.__name__} | Game {game_num}/{games} | "
            f"Score: {env.score} | Steps: {env.steps}",
            flush=True
        )

    avg_score = sum(scores) / len(scores) if scores else 0
    best_score = max(scores) if scores else 0
    avg_steps = sum(steps_list) / len(steps_list) if steps_list else 0

    print("\n" + "=" * 50)
    print(f"{bot_class.__name__} Benchmark Summary")
    print(f"Games played: {games}")
    print(f"Average score: {avg_score:.2f}")
    print(f"Best score: {best_score}")
    print(f"Average steps survived: {avg_steps:.2f}")
    print(f"Step cap: {max_steps}")
    print("=" * 50 + "\n")


def train_rl(episodes=300):
    agent = RLAgent()
    record = 0

    for game_num in range(1, episodes + 1):
        env = SnakeEnv(max_steps=2000, max_idle_steps=None)

        while not env.done:
            state_old = agent.get_state(env)

            final_move = agent.get_action(state_old)
            direction = agent.action_to_direction(env.direction, final_move)

            old_score = env.score

            old_head = env.snake[0]
            old_food = env.food
            old_distance = abs(old_head[0] - old_food[0]) + abs(old_head[1] - old_food[1])

            _, _, done, _ = env.step(direction)
            state_new = agent.get_state(env)

            new_head = env.snake[0]
            new_food = env.food

            if new_food is not None:
                new_distance = abs(new_head[0] - new_food[0]) + abs(new_head[1] - new_food[1])
            else:
                new_distance = 0

            reward = -0.05

            if done:
                reward = -100
            elif env.score > old_score:
                reward = 40
            else:
                if new_distance < old_distance:
                    reward += 1
                elif new_distance > old_distance:
                    reward -= 1

                legal_count = len(env.legal_actions())
                if legal_count <= 1:
                    reward -= 2

            agent.train_short_memory(state_old, final_move, reward, state_new, done)
            agent.remember(state_old, final_move, reward, state_new, done)

        agent.n_games += 1
        agent.train_long_memory()

        if env.score > record:
            record = env.score
            agent.save()

        print(
            f"RLAgent | Game {game_num}/{episodes} | "
            f"Score: {env.score} | Steps: {env.steps} | Record: {record}",
            flush=True
        )

    print("\nTraining finished.")
    print(f"Best score reached: {record}")


def watch_rl():
    env = SnakeEnv(max_steps=5000, max_idle_steps=None)
    renderer = Renderer(env.rows, env.cols)
    agent = RLAgent()

    loaded = agent.load()
    if not loaded:
        print("No saved RL model found in saves/rl_model.pth")
        pygame.quit()
        return

    running = True
    while running and not env.done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        state = agent.get_state(env)
        final_move = agent.get_action(state, training=False)
        direction = agent.action_to_direction(env.direction, final_move)

        env.step(direction)
        renderer.draw(env, BOT_FPS)

    print(f"RLAgent finished. Score: {env.score}, Steps: {env.steps}")
    pygame.quit()


def benchmark_rl(games=20, max_steps=None):
    scores = []
    steps_list = []

    agent = RLAgent()
    loaded = agent.load()
    if not loaded:
        print("No saved RL model found in saves/rl_model.pth")
        return

    for game_num in range(1, games + 1):
        env = SnakeEnv(max_steps=max_steps, max_idle_steps=None)

        while not env.done:
            state = agent.get_state(env)
            final_move = agent.get_action(state, training=False)
            direction = agent.action_to_direction(env.direction, final_move)
            env.step(direction)

        scores.append(env.score)
        steps_list.append(env.steps)

        print(
            f"RLAgent | Game {game_num}/{games} | "
            f"Score: {env.score} | Steps: {env.steps}",
            flush=True
        )

    avg_score = sum(scores) / len(scores) if scores else 0
    best_score = max(scores) if scores else 0
    avg_steps = sum(steps_list) / len(steps_list) if steps_list else 0

    print("\n" + "=" * 50)
    print("RLAgent Benchmark Summary")
    print(f"Games played: {games}")
    print(f"Average score: {avg_score:.2f}")
    print(f"Best score: {best_score}")
    print(f"Average steps survived: {avg_steps:.2f}")
    print(f"Step cap: {max_steps}")
    print("=" * 50 + "\n")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--bot",
        choices=["human", "hamilton", "astar", "hybrid", "rl"],
        default="hamilton"
    )
    parser.add_argument(
        "--benchmark",
        action="store_true"
    )
    parser.add_argument(
        "--games",
        type=int,
        default=20
    )
    parser.add_argument(
        "--max-steps",
        type=int,
        default=None
    )
    parser.add_argument(
        "--train-rl",
        action="store_true"
    )
    parser.add_argument(
        "--episodes",
        type=int,
        default=300
    )
    args = parser.parse_args()

    if args.train_rl:
        train_rl(args.episodes)
        return

    if args.benchmark:
        if args.bot == "hamilton":
            benchmark_bot(HamiltonianBot, args.games, args.max_steps)
        elif args.bot == "astar":
            benchmark_bot(AStarBot, args.games, args.max_steps)
        elif args.bot == "hybrid":
            benchmark_bot(HybridBot, args.games, args.max_steps)
        elif args.bot == "rl":
            benchmark_rl(args.games, args.max_steps)
        else:
            print("Use --bot hamilton, --bot astar, --bot hybrid, or --bot rl with --benchmark")
        return

    if args.bot == "human":
        run_human()
    elif args.bot == "hamilton":
        run_bot(HamiltonianBot(20, 20))
    elif args.bot == "astar":
        run_bot(AStarBot(20, 20))
    elif args.bot == "hybrid":
        run_bot(HybridBot(20, 20))
    else:
        watch_rl()


if __name__ == "__main__":
    main()