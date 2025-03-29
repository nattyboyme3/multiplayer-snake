"""
Handles food spawning and tracking
"""
import random
from constants import (
    GRID_WIDTH, GRID_HEIGHT, SPACE_SIZE,
    BONUS_MARSHMALLOW_MIN, BONUS_MARSHMALLOW_MAX
)

class FoodManager:
    def __init__(self):
        self.food_positions = []
        self.marshmallows_eaten = 0
        self.next_bonus_target = random.randint(BONUS_MARSHMALLOW_MIN, BONUS_MARSHMALLOW_MAX)
        print(f"Frank needs to eat {self.next_bonus_target} marshmallows for a bonus!")

    def reset(self):
        """Reset food state"""
        self.food_positions = []
        self.marshmallows_eaten = 0
        self.next_bonus_target = random.randint(BONUS_MARSHMALLOW_MIN, BONUS_MARSHMALLOW_MAX)

    def spawn_food(self, snake_positions, tree_positions):
        """Spawn a single marshmallow in an empty spot"""
        while True:
            x = random.randint(0, GRID_WIDTH - 1) * SPACE_SIZE
            y = random.randint(0, GRID_HEIGHT - 1) * SPACE_SIZE
            
            # Check if position is empty (no snake, food, or trees)
            if (x, y) not in snake_positions and (x, y) not in self.food_positions and (x, y) not in tree_positions:
                self.food_positions.append((x, y))
                print(f"Spawned marshmallow at: ({x}, {y})")
                break

    def check_food_eaten(self, position):
        """Check if food was eaten at the given position"""
        if position in self.food_positions:
            self.food_positions.remove(position)
            self.marshmallows_eaten += 1
            return True
        return False

    def should_spawn_bonus(self):
        """Check if we should spawn a bonus marshmallow"""
        return self.marshmallows_eaten >= self.next_bonus_target

    def spawn_bonus_marshmallows(self, snake_positions, tree_positions):
        """Handle bonus marshmallow spawning"""
        print(f"Frank ate {self.next_bonus_target} marshmallows! Spawning a bonus marshmallow!")
        self.spawn_food(snake_positions, tree_positions)
        self.marshmallows_eaten = 0
        self.next_bonus_target = random.randint(BONUS_MARSHMALLOW_MIN, BONUS_MARSHMALLOW_MAX)
        print(f"New target: Eat {self.next_bonus_target} more marshmallows for another bonus!") 