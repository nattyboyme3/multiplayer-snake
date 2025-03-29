import tkinter as tk
from tkinter import messagebox
import random
from game_logic import GameLogic
from snake_renderer import SnakeRenderer
from game_over_messages import WALL_COLLISION_MESSAGES, TREE_COLLISION_MESSAGES, SELF_COLLISION_MESSAGES
from marshmallow import Marshmallow
from tree_trunk import TreeTrunk

class SnakeGame:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Snake Game")
        self.window.resizable(False, False)
        
        # Game constants
        self.SPACE_SIZE = 25
        self.GRID_WIDTH = 28  # Makes the game 700 pixels wide
        self.GRID_HEIGHT = 28  # Makes the game 700 pixels high
        self.GAME_WIDTH = self.GRID_WIDTH * self.SPACE_SIZE
        self.GAME_HEIGHT = self.GRID_HEIGHT * self.SPACE_SIZE
        self.INITIAL_SPEED = 150  # Frank starts slower (was 100)
        self.SPEED = self.INITIAL_SPEED
        self.SPEED_INCREASE = 0.95  # 5% faster (multiply by 0.95)
        self.FOOD_COLOR = "#FFFFFF"  # White for marshmallow
        self.MARSHMALLOW_SHADOW = "#E0E0E0"  # Light gray for shadow
        self.BACKGROUND_COLOR = "#8B4513"  # Saddle Brown (desaturated burnt orange)
        self.TEXT_COLOR = "#FFFFFF"
        
        print(f"Game dimensions: {self.GAME_WIDTH}x{self.GAME_HEIGHT}")
        print(f"Grid dimensions: {self.GRID_WIDTH}x{self.GRID_HEIGHT}")
        
        # Create game logic instance
        self.game_logic = GameLogic(self.GRID_WIDTH, self.GRID_HEIGHT, self.SPACE_SIZE)
        
        # Create game elements
        self.canvas = tk.Canvas(
            self.window,
            bg=self.BACKGROUND_COLOR,
            height=self.GAME_HEIGHT,
            width=self.GAME_WIDTH
        )
        self.canvas.pack()
        
        # Create snake renderer, marshmallow, and tree trunk
        self.snake_renderer = SnakeRenderer(self.canvas, self.SPACE_SIZE)
        self.marshmallow = Marshmallow(self.canvas, self.SPACE_SIZE)
        self.tree_trunk = TreeTrunk(self.canvas, self.SPACE_SIZE)
        
        # Create score display (initially hidden)
        self.score_label = tk.Label(
            self.window,
            text="Snake Game",
            font=("consolas", 40, "bold"),
            bg=self.BACKGROUND_COLOR,
            fg=self.TEXT_COLOR
        )
        
        # Create game over text
        self.game_over_text = tk.Label(
            self.window,
            text="",
            font=("consolas", 16),
            bg=self.BACKGROUND_COLOR,
            fg=self.TEXT_COLOR,
            wraplength=self.GAME_WIDTH - 40
        )
        
        # Create play again button (initially hidden)
        self.play_again_button = tk.Button(
            self.window,
            text="Play Again",
            font=("consolas", 20),
            bg="#008000",
            fg="black",
            command=self.start_game,
            width=15,
            height=2
        )
        
        # Create quit button (initially hidden)
        self.quit_button = tk.Button(
            self.window,
            text="Quit",
            font=("consolas", 20),
            bg="#FF0000",
            fg="black",
            command=self.window.quit,
            width=15,
            height=2
        )
        
        # Bind controls
        self.window.bind("<Left>", lambda event: self.change_direction("left"))
        self.window.bind("<Right>", lambda event: self.change_direction("right"))
        self.window.bind("<Up>", lambda event: self.change_direction("up"))
        self.window.bind("<Down>", lambda event: self.change_direction("down"))
        
        # Show the start screen
        self.show_start_screen()

    def show_start_screen(self):
        # Clear the canvas
        self.canvas.delete("all")
        
        # Calculate center positions
        center_x = self.GAME_WIDTH // 2
        center_y = self.GAME_HEIGHT // 2
        
        # Draw title with more space at the top
        self.canvas.create_text(
            center_x, center_y - 150,  # Moved up from -100 to -150
            text="Frank's Marshmallow Adventure",
            fill=self.TEXT_COLOR,
            font=("consolas", 36, "bold")
        )
        
        # Draw welcome message with story
        welcome_message = (
            "Frank is a snake who's convinced himself that\n"
            "marshmallows are the key to happiness.\n\n"
            "Despite having no hands or ability to make s'mores,\n"
            "he's determined to collect them anyway.\n\n"
            "Use arrow keys to help Frank in his quest.\n"
            "Each marshmallow makes him slightly faster\n"
            "and marginally more delusional."
        )
        self.canvas.create_text(
            center_x, center_y - 20,  # Moved up from center_y to center_y - 20
            text=welcome_message,
            fill=self.TEXT_COLOR,
            font=("consolas", 18),
            justify="center"
        )
        
        # Create start button with more space from the story
        button_y = center_y + 120  # Moved down from +80 to +120
        self.start_button = tk.Button(
            self.window,
            text="Start Adventure",
            font=("consolas", 20),
            bg="#008000",
            fg="black",
            command=self.start_game,
            width=15,
            height=2
        )
        self.canvas.create_window(center_x, button_y, window=self.start_button)
        
        # Draw a small snake icon with more space from the button
        snake_y = center_y + 220  # Moved down from +180 to +220
        self.canvas.create_oval(
            center_x - 40, snake_y - 10,
            center_x - 20, snake_y + 10,
            fill="#008000"
        )
        self.canvas.create_oval(
            center_x - 20, snake_y - 10,
            center_x, snake_y + 10,
            fill="#008000"
        )
        self.canvas.create_oval(
            center_x, snake_y - 10,
            center_x + 20, snake_y + 10,
            fill="#008000"
        )
        
        # Draw a small marshmallow icon
        self.marshmallow.draw(center_x + 40, snake_y)

    def start_game(self):
        # Hide game over elements if they exist
        self.game_over_text.pack_forget()
        self.play_again_button.pack_forget()
        self.quit_button.pack_forget()
        
        # Clear the canvas
        self.canvas.delete("all")
        
        # Show and reset score label
        self.score_label.pack(pady=20)
        self.score_label.config(text="Score: 0", font=("consolas", 20))
        
        # Reset speed to initial value
        self.SPEED = self.INITIAL_SPEED
        
        # Reset game logic completely
        self.game_logic = GameLogic(self.GRID_WIDTH, self.GRID_HEIGHT, self.SPACE_SIZE)
        
        # Initialize game
        self.init_game()
        
    def init_game(self):
        # Clear the canvas
        self.canvas.delete("all")
        
        # Initialize game logic
        self.game_logic.init_game()
        
        # Draw background with desaturated burnt orange color
        self.canvas.create_rectangle(0, 0, self.GAME_WIDTH, self.GAME_HEIGHT, 
                                   fill=self.BACKGROUND_COLOR, outline=self.BACKGROUND_COLOR)
        
        # Draw snake
        self.snake_renderer.draw_snake(self.game_logic.snake_positions, self.game_logic.snake_direction)
        
        # Draw all marshmallows
        for food_pos in self.game_logic.food_positions:
            self.marshmallow.draw(food_pos[0], food_pos[1])
            
        # Draw all tree trunks
        for tree_pos in self.game_logic.tree_positions:
            self.tree_trunk.draw(tree_pos[0], tree_pos[1])
        
        # Start the game loop
        self.next_turn()
        
    def next_turn(self):
        # Update game state
        food_eaten = self.game_logic.next_turn()
        
        # Clear canvas
        self.canvas.delete("all")
        
        # Draw snake
        self.snake_renderer.draw_snake(self.game_logic.snake_positions, self.game_logic.snake_direction)
        
        # Draw all food
        for food_pos in self.game_logic.food_positions:
            self.marshmallow.draw(food_pos[0], food_pos[1])
            
        # Draw all trees
        for tree_pos in self.game_logic.tree_positions:
            self.tree_trunk.draw(tree_pos[0], tree_pos[1])
        
        # Update score
        self.score_label.config(text=f"Score: {self.game_logic.score}")
        
        # If food was eaten, increase speed
        if food_eaten:
            self.SPEED = int(self.SPEED * self.SPEED_INCREASE)
            print(f"Frank got faster! New speed: {self.SPEED}ms")
        
        # Schedule next turn
        if self.game_logic.game_running:
            self.window.after(self.SPEED, self.next_turn)
        else:
            self.game_over()
            
    def game_over(self):
        # Clear the canvas but keep it
        self.canvas.delete("all")
        
        # Hide the score label
        self.score_label.pack_forget()
        
        # Get the appropriate message based on death cause
        if self.game_logic.death_cause == "wall":
            game_over_message = random.choice(WALL_COLLISION_MESSAGES)
        elif self.game_logic.death_cause == "tree":
            game_over_message = random.choice(TREE_COLLISION_MESSAGES)
        else:  # self collision
            game_over_message = random.choice(SELF_COLLISION_MESSAGES)
        
        # Calculate center positions
        center_x = self.GAME_WIDTH // 2
        center_y = self.GAME_HEIGHT // 2
        
        # Draw game over text
        self.canvas.create_text(
            center_x, center_y - 100,
            text="Game Over!",
            fill=self.TEXT_COLOR,
            font=("consolas", 36, "bold")
        )
        
        # Draw score
        self.canvas.create_text(
            center_x, center_y - 40,
            text=f"Final Score: {self.game_logic.score}",
            fill=self.TEXT_COLOR,
            font=("consolas", 24)
        )
        
        # Draw funny message
        self.canvas.create_text(
            center_x, center_y + 20,
            text=game_over_message,
            fill=self.TEXT_COLOR,
            font=("consolas", 18),
            width=self.GAME_WIDTH - 100  # Wrap text if too long
        )
        
        # Create buttons directly on canvas
        button_y = center_y + 100
        
        # Play Again button
        play_again_x = center_x - 150
        self.canvas.create_window(play_again_x, button_y, window=self.play_again_button)
        
        # Quit button
        quit_x = center_x + 150
        self.canvas.create_window(quit_x, button_y, window=self.quit_button)
        
    def change_direction(self, new_direction):
        self.game_logic.change_direction(new_direction)
            
    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    game = SnakeGame()
    game.run() 