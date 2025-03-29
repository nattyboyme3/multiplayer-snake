"""
Handles snake state and movement logic
"""
from constants import SPACE_SIZE

class SnakeState:
    def __init__(self, grid_width, grid_height):
        self.GRID_WIDTH = grid_width
        self.GRID_HEIGHT = grid_height
        self.snake_direction = "right"
        self.next_direction = "right"
        self.snake_positions = []
        self.direction_buffer = []
        self.max_buffer_size = 2

    def reset(self):
        """Reset snake to initial state"""
        center_x = self.GRID_WIDTH // 2
        center_y = self.GRID_HEIGHT // 2
        self.snake_positions = [
            (center_x * SPACE_SIZE, center_y * SPACE_SIZE),
            ((center_x - 1) * SPACE_SIZE, center_y * SPACE_SIZE),
            ((center_x - 2) * SPACE_SIZE, center_y * SPACE_SIZE)
        ]
        self.snake_direction = "right"
        self.direction_buffer = []

    def init_game(self):
        """Initialize snake for new game"""
        start_x = 5 * SPACE_SIZE
        start_y = (self.GRID_HEIGHT // 2) * SPACE_SIZE
        
        self.snake_positions = [
            (start_x, start_y),
            (start_x - SPACE_SIZE, start_y),
            (start_x - (2 * SPACE_SIZE), start_y)
        ]
        
        print("Initial snake positions:")
        for i, pos in enumerate(self.snake_positions):
            print(f"Segment {i}: {pos}")

    def change_direction(self, new_direction):
        """Add new direction to buffer if it's not full"""
        if len(self.direction_buffer) < self.max_buffer_size:
            if not self.direction_buffer or self.direction_buffer[-1] != new_direction:
                self.direction_buffer.append(new_direction)

    def process_direction_buffer(self):
        """Process the next direction in the buffer if available"""
        if self.direction_buffer:
            next_direction = self.direction_buffer.pop(0)
            if (next_direction == "left" and self.snake_direction != "right") or \
               (next_direction == "right" and self.snake_direction != "left") or \
               (next_direction == "up" and self.snake_direction != "down") or \
               (next_direction == "down" and self.snake_direction != "up"):
                self.snake_direction = next_direction

    def get_next_head_position(self):
        """Calculate the next head position based on current direction"""
        current_head = self.snake_positions[0]
        x, y = current_head
        
        if self.snake_direction == "left":
            return (x - SPACE_SIZE, y)
        elif self.snake_direction == "right":
            return (x + SPACE_SIZE, y)
        elif self.snake_direction == "up":
            return (x, y - SPACE_SIZE)
        else:  # down
            return (x, y + SPACE_SIZE)

    def move(self, grow=False):
        """Move the snake, optionally growing it"""
        new_head = self.get_next_head_position()
        self.snake_positions.insert(0, new_head)
        if not grow:
            self.snake_positions.pop()

    def check_self_collision(self, position):
        """Check if the given position collides with the snake's body"""
        return position in self.snake_positions[1:] 