"""
Base class for UI components
"""
import tkinter as tk

class BaseComponent:
    def __init__(self, parent):
        self.parent = parent
        self.canvas = parent.canvas if hasattr(parent, 'canvas') else None
        self.window = parent.window if hasattr(parent, 'window') else None

    def show(self):
        """Show the component"""
        pass

    def hide(self):
        """Hide the component"""
        pass

    def update(self):
        """Update the component state"""
        pass 