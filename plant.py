import pygame

class Plant(pygame.sprite.Sprite):
    color = (255, 255, 255)
    image = pygame.Surface((50, 50))

    def __init__(self, pos=(0, 0)):
        super().__init__()

        self.color = (255, 255, 255)
        self.health = 100

        self.image = pygame.Surface((50, 50))

        self.image.fill(self.color)

        self.rect = self.image.get_rect(center=pos)
        self.health = 50

        self.terrain = None

        self.price = 0

    def recive_damage(self, damage):
        print(self.health)
        self.health -= damage
        if (self.health <= 0): self.destroy()

    def update(self):
        self.destroy()

    def destroy(self):
        if self.health <= 0 and self.terrain is not None:
            self.terrain.has_plant = False
            self.kill()


class Wallnut(Plant):
    def __init__(self, pos=(0, 0)):
        super().__init__(pos)

        self.color = (143, 100, 16)
        self.shooter = False

        self.price = 50
        self.health = 500

        self.sprite_list = []
        for i in range(3):
            self.sprite_list.append(pygame.transform.smoothscale(pygame.image.load(f"graphics/wallnut/wallnut_{i}.png").convert_alpha(),(64, 64)))

        self.spr_index = 0
        self.image  = self.sprite_list[int(self.spr_index)]
    
    def update(self):
        self.change_state()
    

    def change_state(self):
        if self.spr_index == 0 and self.health <= 350:
            self.spr_index = 1
        elif self.spr_index == 1 and self.health <= 100:
            self.spr_index = 2
        
        self.image = self.sprite_list[int(self.spr_index)]


class Sunflower(Plant):
    def __init__(self, pos=(0, 0)):
        super().__init__(pos)

        # self.color = (252, 186, 3)
        # self.image.fill(self.color)
        self.shooter = False

        self.sprite_list = []
        for i in range(8):
            self.sprite_list.append(pygame.transform.scale2x(pygame.image.load(f"graphics/sunflower/sunflower_{i}.png").convert_alpha()))

        self.spr_index = 0
        self.image = self.sprite_list[int(self.spr_index)]

        self.price = 50
        self.sun_delay = 0

    def update(self):
        self.animation_state()

    def drop_sun(self):
        if self.sun_delay >= 2000:
            # drop sun
            self.sun_delay = 0
            return True
        self.sun_delay += 5
        return False

    def animation_state(self):
        self.spr_index += 0.09
        if self.spr_index >= len(self.sprite_list) : self.spr_index = 0
        self.image  = self.sprite_list[int(self.spr_index)]


class Peashooter(Plant):
    def __init__(self, pos=(0, 0)):
        super().__init__(pos)

        self.color = (50, 168, 96)

        self.image.fill(self.color)
        self.plant_range = PlantRange(self.rect.center)
        self.range_sprite = pygame.sprite.GroupSingle(self.plant_range)
        self.shoot_delay = 0
        self.shooter = True
        self.can_shoot = True
        self.price = 100


        self.sprite_list = []
        for i in range(8):
            self.sprite_list.append(pygame.transform.scale2x(pygame.image.load(f"graphics/peashooter/pea_{i}.png").convert_alpha()))

        self.spr_index = 0
        self.image  = self.sprite_list[int(self.spr_index)]

    def animation_state(self):
        self.spr_index += 0.1
        if self.spr_index >= len(self.sprite_list) : self.spr_index = 0
        self.image = self.sprite_list[int(self.spr_index)]

    def shoot(self):
        if self.shoot_delay >= 300:
            self.can_shoot = True
        if self.can_shoot:
            self.can_shoot = False
            self.shoot_delay = 0
            return Bullet(self.rect.center)
        self.shoot_delay += 5
        return None
    
    def update(self):
        self.animation_state()



class PlantRange(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()

        self.image = pygame.Surface((1200 - pos[0], 1))
        self.image.fill('blue')
        self.rect = self.image.get_rect(topleft=pos)


class Bullet(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = pygame.transform.smoothscale(pygame.image.load("graphics/tiros/tiro.png").convert_alpha(), (15, 15))
        self.rect = self.image.get_rect(center=pos)
        self.rect.x += 40
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
