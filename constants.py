"""
Game constants for Frank's Marshmallow Adventure
"""

# Game Dimensions
SPACE_SIZE = 25
GRID_WIDTH = 28  # Makes the game 700 pixels wide
GRID_HEIGHT = 28  # Makes the game 700 pixels high
GAME_WIDTH = GRID_WIDTH * SPACE_SIZE
GAME_HEIGHT = GRID_HEIGHT * SPACE_SIZE

# Game Speed
INITIAL_SPEED = 150  # Frank starts slower (was 100)
SPEED_INCREASE = 0.95  # 5% faster (multiply by 0.95)

# Colors
FOOD_COLOR = "#FFFFFF"  # White for marshmallow
MARSHMALLOW_SHADOW = "#E0E0E0"  # Light gray for shadow
BACKGROUND_COLOR = "#7A4E2B"  # Desaturated burnt orange (20% less saturation)
TEXT_COLOR = "#FFFFFF"
SCORE_BACKGROUND = "#5C3D21"  # Darker version of background for contrast
SCORE_TEXT_COLOR = "#FFE4B5"  # Warm cream color for better harmony
SUPER_MARSHMALLOW_COLOR = "#9370DB"  # Medium purple for super marshmallow (more vibrant)

# Game Mechanics
INITIAL_TREES_MIN = 5
INITIAL_TREES_MAX = 8
TREE_SPAWN_CHANCE = 0.3  # 30% chance to spawn a tree when eating food
BONUS_MARSHMALLOW_MIN = 8
BONUS_MARSHMALLOW_MAX = 14
MAX_DIRECTION_BUFFER = 2
SUPER_MARSHMALLOW_CHANCE = 0.2  # 20% chance for super marshmallow (increased from 8%)
SUPER_MARSHMALLOW_POINTS = 10
SUPER_MARSHMALLOW_GROWTH = 3

# Fonts
TITLE_FONT = ("consolas", 36, "bold")
WELCOME_FONT = ("consolas", 18)
SCORE_FONT = ("Helvetica", 24, "bold")
BUTTON_FONT = ("consolas", 20)
GAME_OVER_FONT = ("consolas", 16)

# Button Properties
BUTTON_WIDTH = 15
BUTTON_HEIGHT = 2

# Flash Effect Colors
FLASH_COLORS = [
    "#FF6B6B",  # Coral Red
    "#4ECDC4",  # Turquoise
    "#45B7D1",  # Sky Blue
    "#96CEB4",  # Sage Green
    "#FFEEAD",  # Cream Yellow
    "#D4A5A5",  # Dusty Rose
    "#9B59B6",  # Purple
    "#3498DB",  # Blue
    "#2ECC71",  # Green
    "#F1C40F",  # Yellow
]
FLASH_DURATION = 6  # Number of moves the flash effect lasts (increased from 4) 