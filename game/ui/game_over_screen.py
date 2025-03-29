"""
Game over screen UI component
"""
import tkinter as tk
import random
from constants import (
    GAME_WIDTH, GAME_HEIGHT, TEXT_COLOR,
    GAME_OVER_FONT, SCORE_FONT, WELCOME_FONT,
    BUTTON_FONT, BUTTON_WIDTH, BUTTON_HEIGHT
)
from game_over_messages import (
    WALL_COLLISION_MESSAGES,
    TREE_COLLISION_MESSAGES,
    SELF_COLLISION_MESSAGES
)
from .base_component import BaseComponent

class GameOverScreen(BaseComponent):
    def __init__(self, parent):
        super().__init__(parent)
        self.play_again_button = tk.Button(
            self.window,
            text="Play Again",
            font=BUTTON_FONT,
            bg="#008000",
            fg="black",
            command=self.parent.start_game,
            width=BUTTON_WIDTH,
            height=BUTTON_HEIGHT
        )
        
        self.quit_button = tk.Button(
            self.window,
            text="Quit",
            font=BUTTON_FONT,
            bg="#FF0000",
            fg="black",
            command=self.window.quit,
            width=BUTTON_WIDTH,
            height=BUTTON_HEIGHT
        )

    def show(self, score, death_cause):
        """Display the game over screen"""
        self.canvas.delete("all")
        
        # Get appropriate message based on death cause
        if death_cause == "wall":
            game_over_message = random.choice(WALL_COLLISION_MESSAGES)
        elif death_cause == "tree":
            game_over_message = random.choice(TREE_COLLISION_MESSAGES)
        else:  # self collision
            game_over_message = random.choice(SELF_COLLISION_MESSAGES)
        
        # Calculate center positions
        center_x = GAME_WIDTH // 2
        center_y = GAME_HEIGHT // 2
        
        # Draw game over text
        self.canvas.create_text(
            center_x, center_y - 100,
            text="Game Over!",
            fill=TEXT_COLOR,
            font=GAME_OVER_FONT
        )
        
        # Draw score
        self.canvas.create_text(
            center_x, center_y - 40,
            text=f"Final Score: {score}",
            fill=TEXT_COLOR,
            font=SCORE_FONT
        )
        
        # Draw funny message
        self.canvas.create_text(
            center_x, center_y + 20,
            text=game_over_message,
            fill=TEXT_COLOR,
            font=WELCOME_FONT,
            width=GAME_WIDTH - 100
        )
        
        # Create buttons
        button_y = center_y + 100
        self.canvas.create_window(center_x - 150, button_y, window=self.play_again_button)
        self.canvas.create_window(center_x + 150, button_y, window=self.quit_button)

    def hide(self):
        """Hide the game over screen"""
        self.play_again_button.pack_forget()
        self.quit_button.pack_forget() 