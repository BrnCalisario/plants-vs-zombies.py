from pygame import sprite, Surface

class Enemy(sprite.Sprite):
    def __init__(self, pos=(0, 0)):
        super().__init__()
        self.image = Surface((50, 50))
        self.image.fill("green")
        self.rect = self.image.get_rect(topleft=pos)
        
        self.damage_delay = 0
        self.speed = 0

        self.health = 50
        self.damage = 5

    def update(self):
        self.rect.x -= self.speed
        self.destroy()

    def destroy(self):
        if self.rect.x <= 0:
            self.kill()

    def recive_damage(self, damage):
        self.health -= damage
        print(self.health)
        if (self.health <= 0):
            self.kill()

    def give_damage(self, plant):
        if self.damage_delay == 200:
            self.damage_delay = 0
            plant.recive_damage(self.damage)
        else: self.damage_delay += 5
    
