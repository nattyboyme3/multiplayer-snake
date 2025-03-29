import random
from constants import (
    GRID_WIDTH, GRID_HEIGHT, SPACE_SIZE, GAME_WIDTH, GAME_HEIGHT,
    INITIAL_TREES_MIN, INITIAL_TREES_MAX, TREE_SPAWN_CHANCE,
    BONUS_MARSHMALLOW_MIN, BONUS_MARSHMALLOW_MAX, MAX_DIRECTION_BUFFER
)

class GameLogic:
    def __init__(self, grid_width, grid_height, space_size):
        # Game constants
        self.GRID_WIDTH = grid_width
        self.GRID_HEIGHT = grid_height
        self.SPACE_SIZE = space_size
        self.GAME_WIDTH = GAME_WIDTH
        self.GAME_HEIGHT = GAME_HEIGHT
        
        # Game variables
        self.snake_direction = "right"
        self.next_direction = "right"  # Track the next direction to prevent 180-degree turns
        self.score = 0
        self.snake_positions = []
        self.food_positions = []  # Now a list to store multiple food positions
        self.tree_positions = []  # List to store tree trunk positions
        self.game_running = True
        self.death_cause = None  # Track how Frank died
        
        # Marshmallow tracking
        self.marshmallows_eaten = 0
        self.next_bonus_target = random.randint(BONUS_MARSHMALLOW_MIN, BONUS_MARSHMALLOW_MAX)
        print(f"Frank needs to eat {self.next_bonus_target} marshmallows for a bonus!")
        
        self.direction_buffer = []  # Buffer for storing pending direction changes
        self.max_buffer_size = MAX_DIRECTION_BUFFER    # Maximum number of buffered inputs
        
    def reset_game(self):
        # Initialize snake at the center
        center_x = self.GRID_WIDTH // 2
        center_y = self.GRID_HEIGHT // 2
        self.snake_positions = [
            (center_x * self.SPACE_SIZE, center_y * self.SPACE_SIZE),
            ((center_x - 1) * self.SPACE_SIZE, center_y * self.SPACE_SIZE),
            ((center_x - 2) * self.SPACE_SIZE, center_y * self.SPACE_SIZE)
        ]
        self.snake_direction = "right"
        self.food_positions = []
        self.tree_positions = []
        self.score = 0
        self.game_running = True
        self.death_cause = None
        self.marshmallows_eaten = 0
        self.direction_buffer = []  # Reset buffer when game resets
        
    def init_game(self):
        # Create snake in the middle of the screen
        start_x = 5 * self.SPACE_SIZE  # Start at the 5th grid position
        start_y = (self.GRID_HEIGHT // 2) * self.SPACE_SIZE
        
        self.snake_positions = [
            (start_x, start_y),
            (start_x - self.SPACE_SIZE, start_y),
            (start_x - (2 * self.SPACE_SIZE), start_y)
        ]
        
        print("Initial snake positions:")
        for i, pos in enumerate(self.snake_positions):
            print(f"Segment {i}: {pos}")
        
        # Create initial food and trees
        self.food_positions = []
        self.tree_positions = []
        self.spawn_food()
        
        # Spawn initial trees
        num_initial_trees = random.randint(INITIAL_TREES_MIN, INITIAL_TREES_MAX)
        print(f"Spawning {num_initial_trees} initial trees...")
        for _ in range(num_initial_trees):
            self.spawn_tree()
        
    def spawn_food(self):
        """Spawn a single marshmallow in an empty spot"""
        while True:
            x = random.randint(0, self.GRID_WIDTH - 1) * self.SPACE_SIZE
            y = random.randint(0, self.GRID_HEIGHT - 1) * self.SPACE_SIZE
            
            # Check if position is empty (no snake, food, or trees)
            if (x, y) not in self.snake_positions and (x, y) not in self.food_positions and (x, y) not in self.tree_positions:
                self.food_positions.append((x, y))  # Store as tuple
                print(f"Spawned marshmallow at: ({x}, {y})")
                break
                
    def spawn_tree(self):
        """Spawn a tree trunk in an empty spot"""
        while True:
            x = random.randint(0, self.GRID_WIDTH - 1) * self.SPACE_SIZE
            y = random.randint(0, self.GRID_HEIGHT - 1) * self.SPACE_SIZE
            
            # Check if position is empty (no snake, food, or trees)
            if (x, y) not in self.snake_positions and [x, y] not in self.food_positions and (x, y) not in self.tree_positions:
                self.tree_positions.append((x, y))  # Store as tuple
                print(f"Spawned tree trunk at: ({x}, {y})")
                break
                
    def change_direction(self, new_direction):
        # Add new direction to buffer if it's not full
        if len(self.direction_buffer) < self.max_buffer_size:
            # Don't add if it's the same as the last buffered direction
            if not self.direction_buffer or self.direction_buffer[-1] != new_direction:
                self.direction_buffer.append(new_direction)

    def process_direction_buffer(self):
        # Process the next direction in the buffer if available
        if self.direction_buffer:
            next_direction = self.direction_buffer.pop(0)
            # Only change direction if it's not opposite to current direction
            if (next_direction == "left" and self.snake_direction != "right") or \
               (next_direction == "right" and self.snake_direction != "left") or \
               (next_direction == "up" and self.snake_direction != "down") or \
               (next_direction == "down" and self.snake_direction != "up"):
                self.snake_direction = next_direction

    def next_turn(self):
        # Process any buffered direction changes
        self.process_direction_buffer()
        
        # Get current head position
        current_head = self.snake_positions[0]
        x, y = current_head
        
        # Calculate new head position based on direction
        if self.snake_direction == "left":
            new_head = (x - self.SPACE_SIZE, y)
        elif self.snake_direction == "right":
            new_head = (x + self.SPACE_SIZE, y)
        elif self.snake_direction == "up":
            new_head = (x, y - self.SPACE_SIZE)
        else:  # down
            new_head = (x, y + self.SPACE_SIZE)
            
        # Check for collisions
        if self.check_collision(new_head):
            self.game_running = False
            return False
            
        # Move snake
        self.snake_positions.insert(0, new_head)
        
        # Check if food was eaten
        food_eaten = False
        if new_head in self.food_positions:
            self.food_positions.remove(new_head)
            self.score += 1
            self.marshmallows_eaten += 1
            food_eaten = True
            
            # Spawn new food
            self.spawn_food()
            
            # Chance to spawn a tree when eating food
            if random.random() < TREE_SPAWN_CHANCE:
                self.spawn_tree()
            
            # Check for bonus marshmallows
            if self.marshmallows_eaten >= self.next_bonus_target:
                self.spawn_bonus_marshmallows()
                self.marshmallows_eaten = 0
                self.next_bonus_target = random.randint(BONUS_MARSHMALLOW_MIN, BONUS_MARSHMALLOW_MAX)
        else:
            self.snake_positions.pop()
            
        return food_eaten
            
    def check_collision(self, head_position):
        """Check if the snake has collided with anything"""
        # Check wall collision
        if (head_position[0] < 0 or head_position[0] >= self.GAME_WIDTH or
            head_position[1] < 0 or head_position[1] >= self.GAME_HEIGHT):
            self.death_cause = "wall"
            return True
            
        # Check tree collision
        if head_position in self.tree_positions:
            self.death_cause = "tree"
            return True
            
        # Check self collision
        if head_position in self.snake_positions[1:]:
            self.death_cause = "self"
            return True
            
        return False
        
    def game_over(self):
        self.game_running = False
        
    def spawn_bonus_marshmallows(self):
        print(f"Frank ate {self.next_bonus_target} marshmallows! Spawning a bonus marshmallow!")
        self.spawn_food()  # Spawn bonus marshmallow
        self.spawn_tree()  # Always spawn a tree with bonus marshmallow
        self.marshmallows_eaten = 0  # Reset counter
        self.next_bonus_target = random.randint(BONUS_MARSHMALLOW_MIN, BONUS_MARSHMALLOW_MAX)  # New random target
        print(f"New target: Eat {self.next_bonus_target} more marshmallows for another bonus!") 