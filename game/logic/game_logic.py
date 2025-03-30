"""
Main game logic class that coordinates all game components
"""
from constants import GAME_WIDTH, GAME_HEIGHT, FLASH_DURATION
from .snake_state import SnakeState
from .food_manager import FoodManager
from .tree_manager import TreeManager
from .score_manager import ScoreManager

class GameLogic:
    def __init__(self, grid_width, grid_height, space_size):
        # Initialize all managers
        self.snake = SnakeState(grid_width, grid_height)
        self.food = FoodManager()
        self.trees = TreeManager()
        self._score_manager = ScoreManager()
        self.last_food_eaten = None
        self.last_super_eaten = False
        self.FLASH_DURATION = FLASH_DURATION

    def reset_game(self):
        """Reset all game components"""
        self.snake.reset()
        self.food.reset()
        self.trees.reset()
        self._score_manager.reset()
        self.last_food_eaten = None
        self.last_super_eaten = False

    def init_game(self):
        """Initialize the game"""
        self.snake.init_game()
        self.food.spawn_food(self.snake.snake_positions, self.trees.tree_positions)
        self.trees.spawn_initial_trees(self.snake.snake_positions, self.food.all_food_positions)

    def change_direction(self, new_direction):
        """Change snake direction"""
        self.snake.change_direction(new_direction)

    def next_turn(self):
        """Process one game turn"""
        # Process any buffered direction changes
        self.snake.process_direction_buffer()
        
        # Get next head position
        new_head = self.snake.get_next_head_position()
        
        # Check for collisions
        if self.check_collision(new_head):
            return False
            
        # Move snake
        food_eaten, is_super, points, growth = self.food.check_food_eaten(new_head)
        self.snake.move(grow=food_eaten)
        
        if food_eaten:
            # Store the eaten food position and type
            self.last_food_eaten = new_head
            self.last_super_eaten = is_super
            
            # Add points
            for _ in range(points):
                self._score_manager.increment_score()
            
            # Grow snake if needed
            if growth > 1:
                for _ in range(growth - 1):
                    self.snake.move(grow=True)
            
            # Spawn new food
            self.food.spawn_food(self.snake.snake_positions, self.trees.tree_positions)
            
            # Chance to spawn a tree when eating food
            if self.trees.should_spawn_tree():
                self.trees.spawn_tree(self.snake.snake_positions, self.food.all_food_positions)
            
            # Check for bonus marshmallows
            if self.food.should_spawn_bonus():
                bonus_points = self.food.spawn_bonus_marshmallows(self.snake.snake_positions, self.trees.tree_positions)
                # Add bonus points for reaching the goal
                for _ in range(bonus_points):
                    self._score_manager.increment_score()
                self.trees.spawn_tree(self.snake.snake_positions, self.food.all_food_positions)
        else:
            # Clear last food eaten if no food was eaten this turn
            self.last_food_eaten = None
            self.last_super_eaten = False
            
        return food_eaten

    def check_collision(self, head_position):
        """Check for any collisions"""
        # Check wall collision
        if (head_position[0] < 0 or head_position[0] >= GAME_WIDTH or
            head_position[1] < 0 or head_position[1] >= GAME_HEIGHT):
            self._score_manager.game_over("wall")
            return True
            
        # Check tree collision
        if self.trees.check_tree_collision(head_position):
            self._score_manager.game_over("tree")
            return True
            
        # Check self collision
        if self.snake.check_self_collision(head_position):
            self._score_manager.game_over("self")
            return True
            
        return False

    def game_over(self):
        """End the game"""
        self._score_manager.game_over(None)

    @property
    def snake_positions(self):
        return self.snake.snake_positions

    @property
    def snake_direction(self):
        return self.snake.snake_direction

    @property
    def food_positions(self):
        return self.food.all_food_positions

    @property
    def super_food_positions(self):
        return self.food.super_food_positions

    @property
    def tree_positions(self):
        return self.trees.tree_positions

    @property
    def score(self):
        return self._score_manager.get_score()

    @property
    def game_running(self):
        return self._score_manager.is_game_running()

    @property
    def death_cause(self):
        return self._score_manager.get_death_cause()