"""
Game board UI component
"""
from constants import (
    GAME_WIDTH, GAME_HEIGHT,
    BACKGROUND_COLOR
)
from .base_component import BaseComponent

class GameBoard(BaseComponent):
    def __init__(self, parent):
        super().__init__(parent)
        self.snake_renderer = parent.snake_renderer
        self.marshmallow = parent.marshmallow
        self.tree_trunk = parent.tree_trunk

    def show(self):
        """Show the game board"""
        self.canvas.delete("all")
        self._draw_background()

    def update(self, game_state):
        """Update the game board display"""
        self.canvas.delete("all")
        self._draw_background()
        
        # Draw snake
        self.snake_renderer.draw_snake(
            game_state.snake_positions,
            game_state.snake_direction
        )
        
        # Draw all marshmallows
        for food_pos in game_state.food_positions:
            self.marshmallow.draw(food_pos[0], food_pos[1])
            
        # Draw all tree trunks
        for tree_pos in game_state.tree_positions:
            self.tree_trunk.draw(tree_pos[0], tree_pos[1])

    def _draw_background(self):
        """Draw the game board background"""
        self.canvas.create_rectangle(
            0, 0, GAME_WIDTH, GAME_HEIGHT,
            fill=BACKGROUND_COLOR,
            outline=BACKGROUND_COLOR
        ) 