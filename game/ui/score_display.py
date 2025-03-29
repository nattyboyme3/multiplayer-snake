"""
Score display UI component
"""
import tkinter as tk
from constants import (
    SCORE_BACKGROUND, SCORE_TEXT_COLOR,
    SCORE_FONT
)
from .base_component import BaseComponent

class ScoreDisplay(BaseComponent):
    def __init__(self, parent):
        super().__init__(parent)
        self.frame = tk.Frame(
            self.window,
            bg=SCORE_BACKGROUND,
            bd=2,
            relief="raised"
        )
        
        self.label = tk.Label(
            self.frame,
            text="Score: 0",
            font=SCORE_FONT,
            bg=SCORE_BACKGROUND,
            fg=SCORE_TEXT_COLOR,
            padx=20,
            pady=10
        )
        self.label.pack()

    def show(self):
        """Show the score display"""
        self.frame.pack(pady=10)

    def hide(self):
        """Hide the score display"""
        self.frame.pack_forget()

    def update(self, score):
        """Update the displayed score"""
        self.label.config(text=f"Score: {score}")

    def reset(self):
        """Reset the score display"""
        self.label.config(text="Score: 0") 