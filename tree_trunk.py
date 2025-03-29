class TreeTrunk:
    def __init__(self, canvas, space_size):
        self.canvas = canvas
        self.SPACE_SIZE = space_size
        self.TRUNK_COLOR = "#4A2F10"  # Dark brown
        self.BARK_COLOR = "#2A1A0A"   # Darker brown for bark lines
        
    def draw(self, x, y):
        # Draw the main trunk body (slightly smaller than a full space for padding)
        padding = 2
        self.canvas.create_rectangle(
            x + padding,
            y + padding,
            x + self.SPACE_SIZE - padding,
            y + self.SPACE_SIZE - padding,
            fill=self.TRUNK_COLOR,
            outline=self.BARK_COLOR
        )
        
        # Draw bark lines (squiggly vertical lines)
        # Left side
        self.canvas.create_line(
            x + 5, y + 5,
            x + 5, y + self.SPACE_SIZE - 5,
            fill=self.BARK_COLOR,
            width=2,
            smooth=True
        )
        # Middle
        self.canvas.create_line(
            x + self.SPACE_SIZE//2, y + 5,
            x + self.SPACE_SIZE//2, y + self.SPACE_SIZE - 5,
            fill=self.BARK_COLOR,
            width=2,
            smooth=True
        )
        # Right side
        self.canvas.create_line(
            x + self.SPACE_SIZE - 5, y + 5,
            x + self.SPACE_SIZE - 5, y + self.SPACE_SIZE - 5,
            fill=self.BARK_COLOR,
            width=2,
            smooth=True
        ) 