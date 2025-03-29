"""
Main game logic class that coordinates all game components
"""
from constants import GAME_WIDTH, GAME_HEIGHT
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

    def reset_game(self):
        """Reset all game components"""
        self.snake.reset()
        self.food.reset()
        self.trees.reset()
        self._score_manager.reset()

    def init_game(self):
        """Initialize the game"""
        self.snake.init_game()
        self.food.spawn_food(self.snake.snake_positions, self.trees.tree_positions)
        self.trees.spawn_initial_trees(self.snake.snake_positions, self.food.food_positions)

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
        food_eaten = self.food.check_food_eaten(new_head)
        self.snake.move(grow=food_eaten)
        
        if food_eaten:
            self._score_manager.increment_score()
            self.food.spawn_food(self.snake.snake_positions, self.trees.tree_positions)
            
            # Chance to spawn a tree when eating food
            if self.trees.should_spawn_tree():
                self.trees.spawn_tree(self.snake.snake_positions, self.food.food_positions)
            
            # Check for bonus marshmallows
            if self.food.should_spawn_bonus():
                self.food.spawn_bonus_marshmallows(self.snake.snake_positions, self.trees.tree_positions)
                self.trees.spawn_tree(self.snake.snake_positions, self.food.food_positions)
            
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
        return self.food.food_positions

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