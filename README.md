
# Snake Bot Lab

A multi-phase Snake AI project comparing deterministic, search-based, learning-based, and hybrid control strategies.

---

## Goal

Build a Snake Bot Lab with 4 phases:

1. Hamiltonian bot
2. A* + survival-check bot
3. RL self-improving bot
4. Hybrid bot that uses A* when safe and Hamiltonian when risky

---

## Current Progress

### Phase 1: Hamiltonian baseline
- [x] Project structure
- [x] Snake environment
- [x] Renderer
- [x] Hamiltonian baseline bot
- [x] Generated Hamiltonian cycle version

### Phase 2: A* survival bot
- [x] Pathfinding helper
- [x] A* path to food
- [x] Simulate path
- [x] Tail reachability check
- [x] Tail-chasing fallback
- [ ] Benchmark Hamilton vs A*
- [ ] Improve crowded-board safety further if needed

### Phase 3: RL self-improving bot
- [ ] RL state design
- [ ] RL agent
- [ ] Model
- [ ] Trainer
- [ ] Single-environment training
- [ ] Parallel/vector environments
- [ ] Evaluation mode

### Phase 4: Hybrid bot
- [ ] Decision engine
- [ ] Use A* when safe
- [ ] Use Hamiltonian when risky
- [ ] Tail fallback
- [ ] Efficiency vs safety comparison

---

## Current State

Working now:
- Human mode
- Hamiltonian bot
- A* bot
- Improved renderer/UI for visibility

Current focus:
- Add benchmark mode without rendering
- Print:
  - average score
  - best score
  - average steps survived

---

## Next Immediate Tasks

1. Add benchmark mode to `main.py`
2. Run Hamiltonian benchmark
3. Run A* benchmark
4. Compare results
5. Start Phase 3 RL implementation

---

## Project Structure

snake_lab/
├── main.py
├── config.py
├── snake_env.py
├── render.py
├── bots/
│   ├── hamiltonian_bot.py
│   ├── astar_bot.py
│   ├── hybrid_bot.py
│   └── rl_agent.py
├── rl/
│   ├── model.py
│   ├── trainer.py
│   └── vector_env.py
├── utils/
│   ├── grid.py
│   ├── pathfinding.py
│   └── metrics.py
├── saves/
└── PROJECT_STATUS.md

---

## Notes

- Hamiltonian bot is the safety baseline.
- A* bot is the efficient/search baseline.
- RL will be the actual self-improving bot.
- Hybrid bot is the final “best practical” controller.

### Benchmark Result: AStarBot (step cap = 3200)
- Games played: 20
- Average score: 117.45
- Best score: 143
- Average steps survived: 3200.00

Conclusion:
- Strong short-horizon food efficiency
- Clearly outperforms Hamiltonian under strict step cap
- Can become overly conservative in uncapped mode and stall instead of collecting food
- Strong evidence for a future hybrid strategy

Benchmark takeaway:
- A* is better for fast food collection
- Hamiltonian is better for guaranteed eventual completion
- Hybrid controller is justified
