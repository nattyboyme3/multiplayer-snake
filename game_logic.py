import random

class GameLogic:
    def __init__(self, grid_width, grid_height, space_size):
        # Game constants
        self.GRID_WIDTH = grid_width
        self.GRID_HEIGHT = grid_height
        self.SPACE_SIZE = space_size
        self.GAME_WIDTH = self.GRID_WIDTH * self.SPACE_SIZE
        self.GAME_HEIGHT = self.GRID_HEIGHT * self.SPACE_SIZE
        
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
        self.marshmallow_target = random.randint(8, 14)  # Random target between 8 and 14
        print(f"Frank needs to eat {self.marshmallow_target} marshmallows for a bonus!")
        
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
        
        # Spawn 5-8 initial trees
        num_initial_trees = random.randint(5, 8)
        print(f"Spawning {num_initial_trees} initial trees...")
        for _ in range(num_initial_trees):
            self.spawn_tree()
        
    def spawn_food(self):
        """Spawn a single marshmallow in an empty spot"""
        while True:
            x = random.randint(0, self.GRID_WIDTH - 1) * self.SPACE_SIZE
            y = random.randint(0, self.GRID_HEIGHT - 1) * self.SPACE_SIZE
            
            # Check if position is empty (no snake, food, or trees)
            if (x, y) not in self.snake_positions and [x, y] not in self.food_positions and [x, y] not in self.tree_positions:
                self.food_positions.append([x, y])
                print(f"Spawned marshmallow at: ({x}, {y})")
                break
                
    def spawn_tree(self):
        """Spawn a tree trunk in an empty spot"""
        while True:
            x = random.randint(0, self.GRID_WIDTH - 1) * self.SPACE_SIZE
            y = random.randint(0, self.GRID_HEIGHT - 1) * self.SPACE_SIZE
            
            # Check if position is empty (no snake, food, or trees)
            if (x, y) not in self.snake_positions and [x, y] not in self.food_positions and [x, y] not in self.tree_positions:
                self.tree_positions.append([x, y])
                print(f"Spawned tree trunk at: ({x}, {y})")
                break
                
    def next_turn(self):
        if not self.game_running:
            return False
            
        # Update direction from next_direction
        self.snake_direction = self.next_direction
            
        # Get current snake head position
        x, y = self.snake_positions[0]
        print(f"\nCurrent head position: ({x}, {y})")
        print(f"Current direction: {self.snake_direction}")
        
        # Update snake head position based on direction
        if self.snake_direction == "left":
            x -= self.SPACE_SIZE
        elif self.snake_direction == "right":
            x += self.SPACE_SIZE
        elif self.snake_direction == "up":
            y -= self.SPACE_SIZE
        elif self.snake_direction == "down":
            y += self.SPACE_SIZE
            
        print(f"New head position: ({x}, {y})")
        print(f"Game bounds: 0 <= x < {self.GAME_WIDTH}, 0 <= y < {self.GAME_HEIGHT}")
            
        # Update snake positions
        self.snake_positions.insert(0, (x, y))
        
        # Check for collisions first
        if self.check_collision((x, y)):
            self.game_over()
            return False
            
        # Check if food is eaten and handle tree spawning
        food_eaten = self.eat_food()
            
        if not food_eaten:
            # Remove tail if no food eaten
            del self.snake_positions[-1]
            
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
        
    def change_direction(self, new_direction):
        # Prevent 180-degree turns
        if (new_direction == "left" and self.snake_direction != "right") or \
           (new_direction == "right" and self.snake_direction != "left") or \
           (new_direction == "up" and self.snake_direction != "down") or \
           (new_direction == "down" and self.snake_direction != "up"):
            print(f"Changing direction from {self.snake_direction} to {new_direction}")
            self.next_direction = new_direction 

    def eat_food(self):
        """Handle food eating and return True if food was eaten"""
        food_eaten = False
        x, y = self.snake_positions[0]
        
        # Check for collisions first
        if self.check_collision((x, y)):
            self.game_over()
            return False
            
        # Check if snake ate any food
        for food_pos in self.food_positions[:]:
            if x == food_pos[0] and y == food_pos[1]:
                self.food_positions.remove(food_pos)
                self.score += 1
                self.marshmallows_eaten += 1
                food_eaten = True
                
                # 30% chance to spawn a tree when eating
                if random.random() < 0.3:
                    self.spawn_tree()
                
                # Spawn new food
                self.spawn_food()
                
                # Check if we've reached the marshmallow target
                if self.marshmallows_eaten >= self.marshmallow_target:
                    print(f"Frank ate {self.marshmallow_target} marshmallows! Spawning a bonus marshmallow!")
                    self.spawn_food()  # Spawn bonus marshmallow
                    self.spawn_tree()  # Always spawn a tree with bonus marshmallow
                    self.marshmallows_eaten = 0  # Reset counter
                    self.marshmallow_target = random.randint(8, 14)  # New random target
                    print(f"New target: Eat {self.marshmallow_target} more marshmallows for another bonus!")
                
                break
                
        return food_eaten 