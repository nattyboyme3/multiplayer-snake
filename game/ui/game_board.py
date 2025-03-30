"""
Game board UI component
"""
import random
from constants import (
    GAME_WIDTH, GAME_HEIGHT,
    BACKGROUND_COLOR, FLASH_COLORS
)
from .base_component import BaseComponent

class GameBoard(BaseComponent):
    def __init__(self, parent):
        super().__init__(parent)
        self.snake_renderer = parent.snake_renderer
        self.marshmallow = parent.marshmallow
        self.tree_trunk = parent.tree_trunk
        self.flash_remaining = 0
        self.last_food_eaten = None

    def show(self):
        """Show the game board"""
        self.canvas.delete("all")
        self._draw_background()

    def update(self, game_state):
        """Update the game board display"""
        self.canvas.delete("all")
        
        # Check if a super marshmallow was just eaten
        if game_state.last_food_eaten and game_state.last_super_eaten:
            self.flash_remaining = game_state.FLASH_DURATION
            self.last_food_eaten = game_state.last_food_eaten
        elif self.flash_remaining > 0:
            self.flash_remaining -= 1
        
        # Draw background with flash effect if active
        if self.flash_remaining > 0:
            self._draw_flash_background()
        else:
            self._draw_background()
        
        # Draw snake
        self.snake_renderer.draw_snake(
            game_state.snake_positions,
            game_state.snake_direction
        )
        
        # Draw all marshmallows
        for food_pos in game_state.food_positions:
            is_super = food_pos in game_state.super_food_positions
            self.marshmallow.draw(food_pos[0], food_pos[1], is_super)
            
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

    def _draw_flash_background(self):
        """Draw a flashing background with random colors"""
        # Create a gradient effect with random colors
        color1 = random.choice(FLASH_COLORS)
        color2 = random.choice(FLASH_COLORS)
        
        # Draw the background with the gradient
        self.canvas.create_rectangle(
            0, 0, GAME_WIDTH, GAME_HEIGHT,
            fill=color1,
            outline=color1
        )
        
        # Add some visual interest with diagonal stripes
        stripe_width = 50
        for x in range(0, GAME_WIDTH, stripe_width):
            self.canvas.create_rectangle(
                x, 0,
                x + stripe_width, GAME_HEIGHT,
                fill=color2,
                outline=color2,
                stipple="gray50"  # Makes it semi-transparent
            ) 