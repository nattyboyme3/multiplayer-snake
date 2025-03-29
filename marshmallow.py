class Marshmallow:
    def __init__(self, canvas, space_size):
        self.canvas = canvas
        self.SPACE_SIZE = space_size
        self.FOOD_COLOR = "#FFFFFF"  # White for marshmallow
        self.MARSHMALLOW_SHADOW = "#E0E0E0"  # Light gray for shadow
        
    def draw(self, x, y):
        """Draw a cute kawaii marshmallow at the specified position."""
        padding = 2
        
        # Draw main marshmallow body (white rectangle)
        self.canvas.create_rectangle(
            x + padding, y + padding + 4,  # Add extra padding top/bottom
            x + self.SPACE_SIZE - padding, y + self.SPACE_SIZE - padding - 4,  # Reduce height
            fill=self.FOOD_COLOR,
            outline=self.MARSHMALLOW_SHADOW,
            width=2,
            tag="food"
        )
        
        # Draw curved top
        self.canvas.create_arc(
            x + padding, y + padding,
            x + self.SPACE_SIZE - padding, y + padding + 8,
            start=0, extent=180,
            fill=self.FOOD_COLOR,
            outline=self.MARSHMALLOW_SHADOW,
            width=2,
            tag="food"
        )
        
        # Draw curved bottom
        self.canvas.create_arc(
            x + padding, y + self.SPACE_SIZE - padding - 8,
            x + self.SPACE_SIZE - padding, y + self.SPACE_SIZE - padding,
            start=180, extent=180,
            fill=self.FOOD_COLOR,
            outline=self.MARSHMALLOW_SHADOW,
            width=2,
            tag="food"
        )
        
        # Draw kawaii face
        face_offset_y = 2  # Move face up slightly
        
        # Draw eyes (black dots)
        eye_size = 3
        eye_spacing = 8
        center_x = x + self.SPACE_SIZE // 2
        left_eye_x = center_x - eye_spacing
        right_eye_x = center_x + eye_spacing - eye_size
        eyes_y = y + 10 - face_offset_y
        
        self.canvas.create_oval(
            left_eye_x, eyes_y,
            left_eye_x + eye_size, eyes_y + eye_size,
            fill="black",
            outline="black",
            tag="food"
        )
        
        self.canvas.create_oval(
            right_eye_x, eyes_y,
            right_eye_x + eye_size, eyes_y + eye_size,
            fill="black",
            outline="black",
            tag="food"
        )
        
        # Draw cute smile (small 'w' shape)
        smile_y = y + 15 - face_offset_y
        smile_width = 6
        self.canvas.create_line(
            center_x - smile_width, smile_y,
            center_x - smile_width//2, smile_y + 2,
            center_x, smile_y,
            center_x + smile_width//2, smile_y + 2,
            center_x + smile_width, smile_y,
            fill="black",
            width=1,
            smooth=True,
            tag="food"
        ) 