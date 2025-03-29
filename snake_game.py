"""
Main game file for Frank's Marshmallow Adventure
"""
import tkinter as tk
from game.logic import GameLogic
from game.ui import (
    StartScreen,
    ScoreDisplay,
    GameOverScreen,
    GameBoard
)
from snake_renderer import SnakeRenderer
from marshmallow import Marshmallow
from tree_trunk import TreeTrunk
from constants import (
    SPACE_SIZE, GRID_WIDTH, GRID_HEIGHT,
    GAME_WIDTH, GAME_HEIGHT, BACKGROUND_COLOR,
    INITIAL_SPEED, SPEED_INCREASE
)

class SnakeGame:
    def __init__(self):
        # Create main window
        self.window = tk.Tk()
        self.window.title("Snake Game")
        self.window.resizable(False, False)
        
        # Create game canvas
        self.canvas = tk.Canvas(
            self.window,
            bg=BACKGROUND_COLOR,
            height=GAME_HEIGHT,
            width=GAME_WIDTH
        )
        self.canvas.pack()
        
        # Initialize game speed
        self.speed = INITIAL_SPEED
        
        # Create game renderers
        self.snake_renderer = SnakeRenderer(self.canvas, SPACE_SIZE)
        self.marshmallow = Marshmallow(self.canvas, SPACE_SIZE)
        self.tree_trunk = TreeTrunk(self.canvas, SPACE_SIZE)
        
        # Create UI components
        self.start_screen = StartScreen(self)
        self.score_display = ScoreDisplay(self)
        self.game_over_screen = GameOverScreen(self)
        self.game_board = GameBoard(self)
        
        # Create game logic
        self.game_logic = None
        
        # Bind controls
        self.window.bind("<Left>", lambda event: self.change_direction("left"))
        self.window.bind("<Right>", lambda event: self.change_direction("right"))
        self.window.bind("<Up>", lambda event: self.change_direction("up"))
        self.window.bind("<Down>", lambda event: self.change_direction("down"))
        
        # Show start screen
        self.start_screen.show()

    def start_game(self):
        """Start a new game"""
        # Hide other screens
        self.start_screen.hide()
        self.game_over_screen.hide()
        
        # Reset game state
        self.speed = INITIAL_SPEED
        self.game_logic = GameLogic(GRID_WIDTH, GRID_HEIGHT, SPACE_SIZE)
        
        # Show game components
        self.score_display.show()
        self.game_board.show()
        
        # Initialize game
        self.game_logic.init_game()
        self.game_board.update(self.game_logic)
        
        # Start game loop
        self.next_turn()

    def next_turn(self):
        """Process the next game turn"""
        # Update game state
        food_eaten = self.game_logic.next_turn()
        
        # Update UI
        self.game_board.update(self.game_logic)
        self.score_display.update(self.game_logic.score)
        
        # Handle food eaten
        if food_eaten:
            self.speed = int(self.speed * SPEED_INCREASE)
            print(f"Frank got faster! New speed: {self.speed}ms")
        
        # Continue game or show game over
        if self.game_logic.game_running:
            self.window.after(self.speed, self.next_turn)
        else:
            self.game_over()

    def game_over(self):
        """Handle game over state"""
        self.score_display.hide()
        self.game_over_screen.show(
            self.game_logic.score,
            self.game_logic.death_cause
        )

    def change_direction(self, new_direction):
        """Change snake direction"""
        if self.game_logic:
            self.game_logic.change_direction(new_direction)

    def run(self):
        """Start the game"""
        self.window.mainloop()

if __name__ == "__main__":
    game = SnakeGame()
    game.run() 