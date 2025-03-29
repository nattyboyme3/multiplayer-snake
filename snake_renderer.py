import tkinter as tk
import random  # For random tongue flicking

class SnakeRenderer:
    def __init__(self, canvas, space_size):
        self.canvas = canvas
        self.SPACE_SIZE = space_size
        self.SNAKE_COLOR = "#008000"  # Darker green for Frank's body
        self.EYE_COLOR = "#FFFFFF"  # White color for Frank's eyes
        self.PUPIL_COLOR = "#000000"  # Black color for Frank's pupils
        self.TONGUE_COLOR = "#FF3366"  # Pinkish-red for Frank's tongue
        self.TONGUE_CHANCE = 0.20  # 20% chance to show tongue
        
    def draw_rounded_rectangle(self, x1, y1, x2, y2, radius, **kwargs):
        points = [
            x1 + radius, y1,
            x2 - radius, y1,
            x2, y1,
            x2, y1 + radius,
            x2, y2 - radius,
            x2, y2,
            x2 - radius, y2,
            x1 + radius, y2,
            x1, y2,
            x1, y2 - radius,
            x1, y1 + radius,
            x1, y1
        ]
        return self.canvas.create_polygon(points, smooth=True, **kwargs)

    def draw_tail(self, pos_x, pos_y, direction, prev_x, prev_y, **kwargs):
        # Calculate the tail direction based on the previous segment
        dx = pos_x - prev_x
        dy = pos_y - prev_y
        
        # Size of the tail base (slightly wider than body)
        base = self.SPACE_SIZE
        extra_width = base * 0.2  # Make base 20% wider than body
        
        # Points for the triangle based on movement direction
        if abs(dx) > abs(dy):  # Horizontal movement
            if dx > 0:  # Moving right
                points = [
                    pos_x + base, pos_y + base/2,  # Middle right (point)
                    pos_x, pos_y - extra_width,  # Top left (wide base)
                    pos_x, pos_y + base + extra_width,  # Bottom left (wide base)
                ]
            else:  # Moving left
                points = [
                    pos_x, pos_y + base/2,  # Middle left (point)
                    pos_x + base, pos_y - extra_width,  # Top right (wide base)
                    pos_x + base, pos_y + base + extra_width,  # Bottom right (wide base)
                ]
        else:  # Vertical movement
            if dy > 0:  # Moving down
                points = [
                    pos_x + base/2, pos_y + base,  # Middle bottom (point)
                    pos_x - extra_width, pos_y,  # Top left (wide base)
                    pos_x + base + extra_width, pos_y,  # Top right (wide base)
                ]
            else:  # Moving up
                points = [
                    pos_x + base/2, pos_y,  # Middle top (point)
                    pos_x - extra_width, pos_y + base,  # Bottom left (wide base)
                    pos_x + base + extra_width, pos_y + base,  # Bottom right (wide base)
                ]
        
        return self.canvas.create_polygon(points, smooth=True, **kwargs)
        
    def draw_snake(self, snake_positions, snake_direction):
        # Draw all Frank's segments
        self.canvas.delete("snake")
        
        # Draw Frank's body segments (except tail)
        for i in range(len(snake_positions) - 1):
            pos_x, pos_y = snake_positions[i]
            # Draw Frank's segment with rounded corners
            self.draw_rounded_rectangle(
                pos_x, pos_y,
                pos_x + self.SPACE_SIZE, pos_y + self.SPACE_SIZE,
                radius=10,  # Rounded corners
                fill=self.SNAKE_COLOR,
                tag="snake"
            )
            
            # Add eyes and maybe tongue to Frank's head
            if i == 0:
                self._draw_eyes(pos_x, pos_y, snake_direction)
                # Random chance to show tongue
                if random.random() < self.TONGUE_CHANCE:
                    self._draw_tongue(pos_x, pos_y, snake_direction)
        
        # Draw Frank's tail
        if len(snake_positions) >= 2:
            tail_x, tail_y = snake_positions[-1]
            prev_x, prev_y = snake_positions[-2]
            self.draw_tail(
                tail_x, tail_y,
                snake_direction,
                prev_x, prev_y,
                fill=self.SNAKE_COLOR,
                tag="snake"
            )
                
    def _draw_eyes(self, pos_x, pos_y, direction):
        eye_size = 6  # Size of Frank's eyes
        pupil_size = 3  # Size of Frank's pupils
        eye_spacing = int(self.SPACE_SIZE * 0.3)  # 20% further apart from original position
        pupil_offset = 2  # Offset for pupils to move them forward
        
        # Base positions for eyes
        left_x = pos_x + eye_spacing
        right_x = pos_x + self.SPACE_SIZE - eye_spacing
        top_y = pos_y + eye_spacing
        bottom_y = pos_y + self.SPACE_SIZE - eye_spacing
        
        # Calculate eye positions based on direction
        if direction == "right":
            left_eye_x, right_eye_x = right_x, right_x
            left_eye_y, right_eye_y = top_y, bottom_y
            # Move pupils right
            left_pupil_x = left_eye_x + pupil_offset
            right_pupil_x = right_eye_x + pupil_offset
            left_pupil_y = left_eye_y
            right_pupil_y = right_eye_y
        elif direction == "left":
            left_eye_x, right_eye_x = left_x, left_x
            left_eye_y, right_eye_y = top_y, bottom_y
            # Move pupils left
            left_pupil_x = left_eye_x - pupil_offset
            right_pupil_x = right_eye_x - pupil_offset
            left_pupil_y = left_eye_y
            right_pupil_y = right_eye_y
        elif direction == "up":
            left_eye_x, right_eye_x = left_x, right_x
            left_eye_y = right_eye_y = top_y
            # Move pupils up
            left_pupil_x = left_eye_x
            right_pupil_x = right_eye_x
            left_pupil_y = left_eye_y - pupil_offset
            right_pupil_y = right_eye_y - pupil_offset
        else:  # down
            left_eye_x, right_eye_x = left_x, right_x
            left_eye_y = right_eye_y = bottom_y
            # Move pupils down
            left_pupil_x = left_eye_x
            right_pupil_x = right_eye_x
            left_pupil_y = left_eye_y + pupil_offset
            right_pupil_y = right_eye_y + pupil_offset
        
        # Draw Frank's white eyes
        self.canvas.create_oval(
            left_eye_x - eye_size, left_eye_y - eye_size,
            left_eye_x + eye_size, left_eye_y + eye_size,
            fill=self.EYE_COLOR,
            tag="snake"
        )
        self.canvas.create_oval(
            right_eye_x - eye_size, right_eye_y - eye_size,
            right_eye_x + eye_size, right_eye_y + eye_size,
            fill=self.EYE_COLOR,
            tag="snake"
        )
        
        # Draw Frank's black pupils
        self.canvas.create_oval(
            left_pupil_x - pupil_size, left_pupil_y - pupil_size,
            left_pupil_x + pupil_size, left_pupil_y + pupil_size,
            fill=self.PUPIL_COLOR,
            tag="snake"
        )
        self.canvas.create_oval(
            right_pupil_x - pupil_size, right_pupil_y - pupil_size,
            right_pupil_x + pupil_size, right_pupil_y + pupil_size,
            fill=self.PUPIL_COLOR,
            tag="snake"
        )

    def _draw_tongue(self, pos_x, pos_y, direction):
        """Draw Frank's forked tongue extending from his head."""
        tongue_width = 2  # Width of the tongue
        tongue_length = self.SPACE_SIZE * 0.6  # Length of the main tongue
        fork_length = self.SPACE_SIZE * 0.3  # Length of the fork tips
        fork_angle = 20  # Angle of the fork tips in degrees
        
        # Calculate tongue base position (middle of the head's edge)
        if direction == "right":
            base_x = pos_x + self.SPACE_SIZE
            base_y = pos_y + self.SPACE_SIZE/2
            tip_x = base_x + tongue_length
            tip_y = base_y
        elif direction == "left":
            base_x = pos_x
            base_y = pos_y + self.SPACE_SIZE/2
            tip_x = base_x - tongue_length
            tip_y = base_y
        elif direction == "up":
            base_x = pos_x + self.SPACE_SIZE/2
            base_y = pos_y
            tip_x = base_x
            tip_y = base_y - tongue_length
        else:  # down
            base_x = pos_x + self.SPACE_SIZE/2
            base_y = pos_y + self.SPACE_SIZE
            tip_x = base_x
            tip_y = base_y + tongue_length
            
        # Draw main tongue
        self.canvas.create_line(
            base_x, base_y,
            tip_x, tip_y,
            fill=self.TONGUE_COLOR,
            width=tongue_width,
            tag="snake"
        )
        
        # Calculate fork tip positions
        if direction in ["left", "right"]:
            fork1_x = tip_x + (fork_length * (-1 if direction == "left" else 1))
            fork1_y = tip_y - fork_length * 0.5
            fork2_x = tip_x + (fork_length * (-1 if direction == "left" else 1))
            fork2_y = tip_y + fork_length * 0.5
        else:
            fork1_x = tip_x - fork_length * 0.5
            fork1_y = tip_y + (fork_length * (-1 if direction == "up" else 1))
            fork2_x = tip_x + fork_length * 0.5
            fork2_y = tip_y + (fork_length * (-1 if direction == "up" else 1))
            
        # Draw fork tips
        self.canvas.create_line(
            tip_x, tip_y,
            fork1_x, fork1_y,
            fill=self.TONGUE_COLOR,
            width=tongue_width,
            tag="snake"
        )
        self.canvas.create_line(
            tip_x, tip_y,
            fork2_x, fork2_y,
            fill=self.TONGUE_COLOR,
            width=tongue_width,
            tag="snake"
        ) 