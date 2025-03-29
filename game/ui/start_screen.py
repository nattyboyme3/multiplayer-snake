"""
Start screen UI component
"""
import tkinter as tk
from constants import (
    GAME_WIDTH, GAME_HEIGHT, TEXT_COLOR,
    TITLE_FONT, WELCOME_FONT, BUTTON_FONT,
    BUTTON_WIDTH, BUTTON_HEIGHT
)
from .base_component import BaseComponent

class StartScreen(BaseComponent):
    def __init__(self, parent):
        super().__init__(parent)
        self.welcome_message = (
            "Frank is a snake who's convinced himself that\n"
            "marshmallows are the key to happiness.\n\n"
            "Despite having no hands or ability to make s'mores,\n"
            "he's determined to collect them anyway.\n\n"
            "Use arrow keys to help Frank in his quest.\n"
            "Each marshmallow makes him slightly faster\n"
            "and marginally more delusional."
        )
        self.start_button = None

    def show(self):
        """Display the start screen"""
        self.canvas.delete("all")
        
        # Calculate center positions
        center_x = GAME_WIDTH // 2
        center_y = GAME_HEIGHT // 2
        
        # Draw title
        self.canvas.create_text(
            center_x, center_y - 150,
            text="Frank's Marshmallow Adventure",
            fill=TEXT_COLOR,
            font=TITLE_FONT
        )
        
        # Draw welcome message
        self.canvas.create_text(
            center_x, center_y - 20,
            text=self.welcome_message,
            fill=TEXT_COLOR,
            font=WELCOME_FONT,
            justify="center"
        )
        
        # Create start button
        button_y = center_y + 120
        self.start_button = tk.Button(
            self.window,
            text="Start Adventure",
            font=BUTTON_FONT,
            bg="#008000",
            fg="black",
            command=self.parent.start_game,
            width=BUTTON_WIDTH,
            height=BUTTON_HEIGHT
        )
        self.canvas.create_window(center_x, button_y, window=self.start_button)
        
        # Draw decorative snake
        snake_y = center_y + 220
        self._draw_decorative_snake(center_x, snake_y)
        
        # Draw decorative marshmallow
        self.parent.marshmallow.draw(center_x + 40, snake_y)

    def _draw_decorative_snake(self, center_x, y):
        """Draw a small decorative snake"""
        for i in range(3):
            x_offset = (i - 1) * 20
            self.canvas.create_oval(
                center_x - 40 + x_offset, y - 10,
                center_x - 20 + x_offset, y + 10,
                fill="#008000"
            )

    def hide(self):
        """Hide the start screen"""
        if self.start_button:
            self.start_button.destroy()
            self.start_button = None 