"""
Handles food spawning and tracking
"""
import random
from constants import (
    GRID_WIDTH, GRID_HEIGHT, SPACE_SIZE,
    BONUS_MARSHMALLOW_MIN, BONUS_MARSHMALLOW_MAX,
    SUPER_MARSHMALLOW_CHANCE, SUPER_MARSHMALLOW_POINTS,
    SUPER_MARSHMALLOW_GROWTH
)

BONUS_GOAL_POINTS = 10  # Points awarded for reaching marshmallow goal

class FoodManager:
    def __init__(self):
        self.food_positions = []
        self.super_food_positions = []  # Track super marshmallows separately
        self.marshmallows_eaten = 0
        self.next_bonus_target = random.randint(BONUS_MARSHMALLOW_MIN, BONUS_MARSHMALLOW_MAX)
        print(f"Frank needs to eat {self.next_bonus_target} marshmallows for a bonus!")
        print(f"Super marshmallow spawn chance: {SUPER_MARSHMALLOW_CHANCE * 100}%")

    def reset(self):
        """Reset food state"""
        self.food_positions = []
        self.super_food_positions = []
        self.marshmallows_eaten = 0
        self.next_bonus_target = random.randint(BONUS_MARSHMALLOW_MIN, BONUS_MARSHMALLOW_MAX)
        print(f"Food state reset. New bonus target: {self.next_bonus_target}")
        print(f"Super marshmallow spawn chance: {SUPER_MARSHMALLOW_CHANCE * 100}%")

    def spawn_food(self, snake_positions, tree_positions):
        """Spawn a marshmallow in an empty spot"""
        while True:
            x = random.randint(0, GRID_WIDTH - 1) * SPACE_SIZE
            y = random.randint(0, GRID_HEIGHT - 1) * SPACE_SIZE
            
            # Check if position is empty (no snake, food, or trees)
            if (x, y) not in snake_positions and (x, y) not in self.food_positions and (x, y) not in self.super_food_positions and (x, y) not in tree_positions:
                # Determine if this should be a super marshmallow
                if random.random() < SUPER_MARSHMALLOW_CHANCE:
                    self.super_food_positions.append((x, y))
                    print(f"🎯 Spawned SUPER marshmallow at: ({x}, {y})")
                    print(f"   Current super marshmallows: {len(self.super_food_positions)}")
                else:
                    self.food_positions.append((x, y))
                    print(f"Spawned regular marshmallow at: ({x}, {y})")
                break

    def check_food_eaten(self, position):
        """Check if food was eaten at the given position"""
        if position in self.food_positions:
            self.food_positions.remove(position)
            self.marshmallows_eaten += 1
            return True, False, 1, 1  # Regular marshmallow: 1 point, 1 growth
        elif position in self.super_food_positions:
            self.super_food_positions.remove(position)
            self.marshmallows_eaten += 1
            print(f"🌟 Frank ate a SUPER marshmallow! {len(self.super_food_positions)} super marshmallows remaining")
            return True, True, SUPER_MARSHMALLOW_POINTS, SUPER_MARSHMALLOW_GROWTH
        return False, False, 0, 0

    def should_spawn_bonus(self):
        """Check if we should spawn a bonus marshmallow"""
        return self.marshmallows_eaten >= self.next_bonus_target

    def spawn_bonus_marshmallows(self, snake_positions, tree_positions):
        """Handle bonus marshmallow spawning"""
        print(f"🎉 Frank ate {self.next_bonus_target} marshmallows! +{BONUS_GOAL_POINTS} bonus points!")
        self.spawn_food(snake_positions, tree_positions)
        self.marshmallows_eaten = 0
        self.next_bonus_target = random.randint(BONUS_MARSHMALLOW_MIN, BONUS_MARSHMALLOW_MAX)
        print(f"New target: Eat {self.next_bonus_target} more marshmallows for another bonus!")
        return BONUS_GOAL_POINTS  # Return bonus points to be added to score

    @property
    def all_food_positions(self):
        """Get all food positions (regular and super)"""
        return self.food_positions + self.super_food_positions 