"""
Handles scoring and game state
"""
class ScoreManager:
    def __init__(self):
        self.score = 0
        self.game_running = True
        self.death_cause = None

    def reset(self):
        """Reset score and game state"""
        self.score = 0
        self.game_running = True
        self.death_cause = None

    def increment_score(self):
        """Increment the score"""
        self.score += 1

    def get_score(self):
        """Get current score"""
        return self.score

    def game_over(self, cause):
        """End the game with a specific cause"""
        self.game_running = False
        self.death_cause = cause

    def is_game_running(self):
        """Check if the game is still running"""
        return self.game_running

    def get_death_cause(self):
        """Get the cause of death"""
        return self.death_cause 