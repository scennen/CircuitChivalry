class Knight:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.hp = 100
        self.armor = 50
        self.sword = "Чёрный меч с голубыми трещинами"
        self.neon_armor = False

    def take_damage(self, damage):
        if self.neon_armor:
            self.armor -= damage
            if self.armor < 0:
                self.hp += self.armor
                self.armor = 0
        else:
            self.hp -= damage

    def activate_neon_armor(self):
        self.neon_armor = True
        self.armor = 100
