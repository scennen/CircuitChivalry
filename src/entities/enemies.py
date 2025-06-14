class Enemy:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.hp = 50
        self.damage = 10

    def attack(self, knight):
        knight.take_damage(self.damage)


class Shadow:
    def __init__(self, x: int, y: int, knight_hp: int):
        self.x = x
        self.y = y
        self.hp = knight_hp
        self.damage = 15

    def attack(self, knight):
        knight.take_damage(self.damage)


class Drone:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.hp = 20
        self.damage = 5

    def attack(self, knight):
        knight.take_damage(self.damage)


class CoreGuardian:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.hp = 200
        self.damage = 30
        self.arms = 4
        self.weapons = ["меч", "топор", "щит", "энергопушка"]

    def attack(self, knight):
        knight.take_damage(self.damage)

    def lose_arm(self):
        self.arms -= 1
        if self.arms == 0:
            self.hp = 0


class Boss:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.hp = 300
        self.damage = 40
        self.phase = 1

    def attack(self, knight):
        knight.take_damage(self.damage)

    def change_phase(self):
        self.phase += 1
        if self.phase == 2:
            self.damage = 60
