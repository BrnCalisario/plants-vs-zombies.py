from pygame import Surface, sprite, mouse


class Shovel(sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.initial_pos = (1000, 20)
        self.image = Surface((50, 50))
        self.image.fill("gold")
        self.rect = self.image.get_rect(topleft=self.initial_pos)
        self.isDragging = False

        self.selected_plant = None

    def update(self):
        if self.isDragging:
            self.rect.center = mouse.get_pos()
        else:
            self.rect.topleft = self.initial_pos

        if self.selected_plant is not None:
            self.selected_plant.image.fill("brown")

    def collide_logic(self, plant):
        self.selected_plant = plant

    def collide_detach(self):
        if self.selected_plant is not None:
            self.selected_plant.image.fill("white")
        self.selected_plant = None


class PlantRange(sprite.Sprite):
    def __init__(self, pos):
        super().__init__()

        self.image = Surface((1000, 1))
        self.image.fill('blue')
        self.rect = self.image.get_rect(topleft=pos)


class Grass(sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = Surface((25, 25))
        self.image.fill('blue')
        self.rect = self.image.get_rect(center=pos)
        self.is_dragging = False
        self.has_plant = False

    def check_click(self, mouse):
        if self.rect.colliderect(mouse):
            return True
        
        
class Plant(sprite.Sprite):
    def __init__(self, pos=(0, 0)):
        super().__init__()

        self.health = 100
        self.image = Surface((50, 50))
        self.image.fill("white")
        self.rect = self.image.get_rect(center=pos)

        self.plant_range = PlantRange(self.rect.center)
        self.range_sprite = sprite.GroupSingle(self.plant_range)

        self.shoot_delay = 0
        self.can_shoot = True

        self.health = 50


    def recive_damage(self, damage):
        print(self.health)
        self.health -= damage

    def update(self):
        self.image.fill("white")
        self.destroy()

    
    def update_bullets(self, zombies):
        pass        

    def destroy(self):
        if self.health <= 0:
            self.kill()

    def shoot(self):
        if self.shoot_delay >= 300:
            self.can_shoot = True
        if self.can_shoot:
            self.can_shoot = False
            self.shoot_delay = 0
            return Bullet(self.rect.center)
        self.shoot_delay += 5
        return None


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