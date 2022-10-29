from pygame import Surface, sprite, mouse

        
class Plant(sprite.Sprite):
    def __init__(self, pos=(0, 0)):
        super().__init__()

        self.color = (255, 255, 255)
        self.health = 100
        self.image = Surface((50, 50))
        self.image.fill(self.color)
        self.rect = self.image.get_rect(center=pos)
        self.health = 50

    def recive_damage(self, damage):
        print(self.health)
        self.health -= damage

    def update(self):
        self.image.fill(self.color)
        self.destroy()
   
    def destroy(self):
        if self.health <= 0:    
            self.kill()

    


class Peashooter(Plant):
    def __init__(self, pos=(0, 0)):
        super().__init__(pos)

        self.color = (50, 168, 96)

        self.image.fill(self.color)
        self.plant_range = PlantRange(self.rect.center)
        self.range_sprite = sprite.GroupSingle(self.plant_range)
        self.shoot_delay = 0
        self.can_shoot = True

    
    def shoot(self):
        if self.shoot_delay >= 300:
            self.can_shoot = True
        if self.can_shoot:
            self.can_shoot = False
            self.shoot_delay = 0
            return Bullet(self.rect.center)
        self.shoot_delay += 5
        return None




class PlantRange(sprite.Sprite):
    def __init__(self, pos):
        super().__init__()

        self.image = Surface((1000, 1))
        self.image.fill('blue')
        self.rect = self.image.get_rect(topleft=pos)


class Bullet(sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = Surface((10, 10))
        self.image.fill("red")
        self.rect = self.image.get_rect(center=pos)
        
        self.damage = 5

    def give_damage(self, zombie):
        zombie.recive_damage(self.damage)
        self.destroy()

    def update(self):
        self.rect.x += 10
        if self.rect.x >= 1300:
            self.destroy()

    def destroy(self):
        self.kill()