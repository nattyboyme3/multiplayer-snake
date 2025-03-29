"""
Handles tree spawning and collision detection
"""
import random
from constants import (
    GRID_WIDTH, GRID_HEIGHT, SPACE_SIZE,
    INITIAL_TREES_MIN, INITIAL_TREES_MAX,
    TREE_SPAWN_CHANCE
)

class TreeManager:
    def __init__(self):
        self.tree_positions = []

    def reset(self):
        """Reset tree state"""
        self.tree_positions = []

    def spawn_tree(self, snake_positions, food_positions):
        """Spawn a tree trunk in an empty spot"""
        while True:
            x = random.randint(0, GRID_WIDTH - 1) * SPACE_SIZE
            y = random.randint(0, GRID_HEIGHT - 1) * SPACE_SIZE
            
            # Check if position is empty (no snake, food, or trees)
            if (x, y) not in snake_positions and (x, y) not in food_positions and (x, y) not in self.tree_positions:
                self.tree_positions.append((x, y))
                print(f"Spawned tree trunk at: ({x}, {y})")
                break

    def spawn_initial_trees(self, snake_positions, food_positions):
        """Spawn initial trees at game start"""
        num_initial_trees = random.randint(INITIAL_TREES_MIN, INITIAL_TREES_MAX)
        print(f"Spawning {num_initial_trees} initial trees...")
        for _ in range(num_initial_trees):
            self.spawn_tree(snake_positions, food_positions)

    def check_tree_collision(self, position):
        """Check if the given position collides with a tree"""
        return position in self.tree_positions

    def should_spawn_tree(self):
        """Check if we should spawn a new tree"""
        return random.random() < TREE_SPAWN_CHANCE 