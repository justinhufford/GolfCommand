# player.py

class Player:
    def __init__(self, health=100):
        self.health = health

    def get_health(self):
        return self.health

    def set_health(self, new_health):
        self.health = max(0, new_health)  # Ensure health does not drop below 0

    def modify_health(self, amount):
        self.health = max(0, self.health + amount)  # Modify health by a given amount
        return self.health

    def __str__(self):
        return f"Player(health={self.health})"
